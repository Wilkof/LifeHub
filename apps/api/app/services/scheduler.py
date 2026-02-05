"""Scheduler service for automated notifications."""
import asyncio
from datetime import datetime, time
from typing import Callable
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from app.config import settings
from app.database import SessionLocal


class SchedulerService:
    """Service for scheduling automated tasks."""
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler(timezone=settings.timezone)
        self._jobs = {}
    
    def start(self):
        """Start the scheduler."""
        if not self.scheduler.running:
            self.scheduler.start()
            print(f"Scheduler started with timezone: {settings.timezone}")
    
    def stop(self):
        """Stop the scheduler."""
        if self.scheduler.running:
            self.scheduler.shutdown()
            print("Scheduler stopped")
    
    async def _run_with_db(self, func: Callable):
        """Run async function with database session."""
        db = SessionLocal()
        try:
            await func(db)
        except Exception as e:
            print(f"Scheduler job error: {e}")
        finally:
            db.close()
    
    def setup_notifications(self):
        """Set up all notification jobs based on user settings."""
        from app.services.telegram_service import (
            send_morning_briefing,
            send_midday_reminder,
            send_evening_checkin
        )
        
        # Get settings from database
        db = SessionLocal()
        try:
            from app.models.settings import UserSettings
            user_settings = db.query(UserSettings).first()
            
            if not user_settings:
                # Use defaults
                morning_time = "08:00"
                midday_time = "13:00"
                evening_time = "21:30"
                weekly_day = 6  # Sunday
                weekly_time = "18:00"
            else:
                morning_time = user_settings.morning_briefing_time
                midday_time = user_settings.midday_reminder_time
                evening_time = user_settings.evening_checkin_time
                weekly_day = user_settings.weekly_review_day
                weekly_time = user_settings.weekly_review_time
            
            # Parse times
            morning_h, morning_m = map(int, morning_time.split(":"))
            midday_h, midday_m = map(int, midday_time.split(":"))
            evening_h, evening_m = map(int, evening_time.split(":"))
            weekly_h, weekly_m = map(int, weekly_time.split(":"))
            
            # Morning briefing
            if not user_settings or user_settings.enable_morning_briefing:
                self.scheduler.add_job(
                    lambda: asyncio.create_task(self._run_with_db(send_morning_briefing)),
                    CronTrigger(hour=morning_h, minute=morning_m),
                    id="morning_briefing",
                    replace_existing=True
                )
                print(f"Morning briefing scheduled at {morning_time}")
            
            # Midday reminder
            if not user_settings or user_settings.enable_midday_reminder:
                self.scheduler.add_job(
                    lambda: asyncio.create_task(self._run_with_db(send_midday_reminder)),
                    CronTrigger(hour=midday_h, minute=midday_m),
                    id="midday_reminder",
                    replace_existing=True
                )
                print(f"Midday reminder scheduled at {midday_time}")
            
            # Evening check-in
            if not user_settings or user_settings.enable_evening_checkin:
                self.scheduler.add_job(
                    lambda: asyncio.create_task(self._run_with_db(send_evening_checkin)),
                    CronTrigger(hour=evening_h, minute=evening_m),
                    id="evening_checkin",
                    replace_existing=True
                )
                print(f"Evening check-in scheduled at {evening_time}")
            
            # Weekly review (Sunday by default)
            if not user_settings or user_settings.enable_weekly_review:
                self.scheduler.add_job(
                    lambda: asyncio.create_task(self._run_with_db(self._weekly_review)),
                    CronTrigger(day_of_week=weekly_day, hour=weekly_h, minute=weekly_m),
                    id="weekly_review",
                    replace_existing=True
                )
                print(f"Weekly review scheduled for day {weekly_day} at {weekly_time}")
            
            # Deadline reminders - check every hour
            if not user_settings or user_settings.enable_deadline_reminders:
                self.scheduler.add_job(
                    lambda: asyncio.create_task(self._run_with_db(self._check_deadlines)),
                    CronTrigger(minute=0),  # Every hour at :00
                    id="deadline_check",
                    replace_existing=True
                )
                print("Deadline checker scheduled (hourly)")
            
        finally:
            db.close()
    
    async def _weekly_review(self, db):
        """Send weekly review notification."""
        from app.services.telegram_service import TelegramService
        from app.services.openai_service import OpenAIService
        from app.models.task import Task, TaskStatus
        from app.models.habit import Habit, HabitLog
        from datetime import date, timedelta
        from sqlalchemy import and_
        
        telegram = TelegramService(db)
        
        today = date.today()
        week_ago = today - timedelta(days=7)
        
        # Tasks completed
        completed = db.query(Task).filter(
            and_(
                Task.status == TaskStatus.DONE,
                Task.completed_at >= datetime.combine(week_ago, datetime.min.time())
            )
        ).count()
        
        # Habits completion
        habits = db.query(Habit).filter(Habit.is_active == True).all()
        habit_completions = 0
        habit_total = 0
        for habit in habits:
            logs = db.query(HabitLog).filter(
                and_(
                    HabitLog.habit_id == habit.id,
                    HabitLog.log_date >= week_ago,
                    HabitLog.completed == True
                )
            ).count()
            habit_completions += logs
            habit_total += 7
        
        completion_rate = round(habit_completions / max(habit_total, 1) * 100)
        
        text = (
            f"📊 <b>Підсумок тижня</b>\n\n"
            f"✅ Виконано задач: {completed}\n"
            f"🎯 Звички: {completion_rate}%\n\n"
        )
        
        if completion_rate >= 70:
            text += "🎉 Чудовий тиждень! Так тримати!\n"
        elif completion_rate >= 50:
            text += "👍 Непогано! Є над чим працювати.\n"
        else:
            text += "💪 Наступний тиждень буде кращим!\n"
        
        text += "\n🎯 Плануй наступний тиждень зараз!"
        
        await telegram.send_message(text)
    
    async def _check_deadlines(self, db):
        """Check for upcoming deadlines and send reminders."""
        from app.services.telegram_service import TelegramService
        from app.models.task import Task, TaskStatus
        from datetime import timedelta
        
        telegram = TelegramService(db)
        now = datetime.now()
        
        # Tasks due in 24 hours
        in_24h = now + timedelta(hours=24)
        tasks_24h = db.query(Task).filter(
            and_(
                Task.status.in_([TaskStatus.TODO, TaskStatus.IN_PROGRESS]),
                Task.due_date >= now,
                Task.due_date <= in_24h
            )
        ).all()
        
        for task in tasks_24h:
            await telegram.send_message(
                f"⏰ <b>Нагадування про дедлайн</b>\n\n"
                f"Задача: {task.title}\n"
                f"Дедлайн: завтра\n\n"
                f"Час діяти!"
            )
        
        # Tasks due in 2 hours
        in_2h = now + timedelta(hours=2)
        tasks_2h = db.query(Task).filter(
            and_(
                Task.status.in_([TaskStatus.TODO, TaskStatus.IN_PROGRESS]),
                Task.due_date >= now,
                Task.due_date <= in_2h
            )
        ).all()
        
        for task in tasks_2h:
            await telegram.send_message(
                f"🚨 <b>ТЕРМІНОВО!</b>\n\n"
                f"Задача: {task.title}\n"
                f"Дедлайн: через 2 години!\n\n"
                f"Зроби це ЗАРАЗ!"
            )


# Global scheduler instance
scheduler_service = SchedulerService()
