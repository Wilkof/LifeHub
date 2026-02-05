"""Dashboard API router - aggregated data for Today view."""
from datetime import date, datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from app.database import get_db
from app.models.task import Task, TaskStatus
from app.models.calendar_event import CalendarEvent
from app.models.habit import Habit, HabitLog, HabitFrequency
from app.models.health import HealthLog
from app.models.finance import Transaction, TransactionType
from app.models.goal import Goal, GoalStatus

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/today")
def get_today_dashboard(db: Session = Depends(get_db)):
    """Get all data for Today dashboard view."""
    today = date.today()
    today_start = datetime.combine(today, datetime.min.time())
    today_end = datetime.combine(today, datetime.max.time())
    weekday = today.weekday()
    
    # MIT (Most Important Tasks)
    mit_tasks = db.query(Task).filter(
        Task.is_mit == True,
        Task.status.in_([TaskStatus.TODO, TaskStatus.IN_PROGRESS])
    ).order_by(Task.priority.desc()).limit(3).all()
    
    # Today's tasks
    today_tasks = db.query(Task).filter(
        Task.status.in_([TaskStatus.TODO, TaskStatus.IN_PROGRESS]),
        Task.is_mit == False
    ).order_by(Task.priority.desc(), Task.due_date.asc().nullslast()).limit(10).all()
    
    # Today's events
    today_events = db.query(CalendarEvent).filter(
        and_(
            CalendarEvent.start_time >= today_start,
            CalendarEvent.start_time <= today_end
        )
    ).order_by(CalendarEvent.start_time.asc()).all()
    
    # Today's habits
    habits = db.query(Habit).filter(Habit.is_active == True).all()
    today_habits = []
    for habit in habits:
        # Check if scheduled for today
        should_track = False
        if habit.frequency == HabitFrequency.DAILY:
            should_track = True
        elif habit.frequency == HabitFrequency.WEEKDAYS:
            should_track = weekday < 5
        elif habit.frequency == HabitFrequency.WEEKENDS:
            should_track = weekday >= 5
        elif habit.frequency == HabitFrequency.CUSTOM:
            should_track = weekday in (habit.custom_days or [])
        else:
            should_track = True
        
        if should_track:
            log = db.query(HabitLog).filter(
                and_(
                    HabitLog.habit_id == habit.id,
                    HabitLog.log_date == today
                )
            ).first()
            
            today_habits.append({
                "id": habit.id,
                "name": habit.name,
                "icon": habit.icon,
                "color": habit.color,
                "completed": log.completed if log else False,
                "streak": habit.current_streak
            })
    
    # Today's health
    health_log = db.query(HealthLog).filter(HealthLog.log_date == today).first()
    
    # Active goals progress
    active_goals = db.query(Goal).filter(
        Goal.status.in_([GoalStatus.NOT_STARTED, GoalStatus.IN_PROGRESS])
    ).order_by(Goal.priority.desc()).limit(5).all()
    
    # Tasks stats
    completed_today = db.query(Task).filter(
        and_(
            Task.status == TaskStatus.DONE,
            Task.completed_at >= today_start,
            Task.completed_at <= today_end
        )
    ).count()
    
    total_pending = db.query(Task).filter(
        Task.status.in_([TaskStatus.TODO, TaskStatus.IN_PROGRESS])
    ).count()
    
    return {
        "date": today.isoformat(),
        "weekday": today.strftime("%A"),
        
        "mit_tasks": [
            {
                "id": t.id,
                "title": t.title,
                "priority": t.priority.value,
                "status": t.status.value
            }
            for t in mit_tasks
        ],
        
        "today_tasks": [
            {
                "id": t.id,
                "title": t.title,
                "priority": t.priority.value,
                "status": t.status.value,
                "due_date": t.due_date.isoformat() if t.due_date else None
            }
            for t in today_tasks
        ],
        
        "events": [
            {
                "id": e.id,
                "title": e.title,
                "start_time": e.start_time.isoformat(),
                "end_time": e.end_time.isoformat() if e.end_time else None,
                "color": e.color,
                "all_day": e.all_day
            }
            for e in today_events
        ],
        
        "habits": today_habits,
        
        "health": {
            "water_glasses": health_log.water_glasses if health_log else 0,
            "sleep_hours": float(health_log.sleep_hours) if health_log and health_log.sleep_hours else None,
            "mood": health_log.mood.value if health_log and health_log.mood else None,
            "energy": health_log.energy_level if health_log else None
        },
        
        "goals": [
            {
                "id": g.id,
                "title": g.title,
                "progress": float(g.progress_percent),
                "icon": g.icon,
                "color": g.color
            }
            for g in active_goals
        ],
        
        "stats": {
            "completed_today": completed_today,
            "total_pending": total_pending,
            "habits_completed": sum(1 for h in today_habits if h["completed"]),
            "habits_total": len(today_habits)
        }
    }


@router.get("/weekly-overview")
def get_weekly_overview(db: Session = Depends(get_db)):
    """Get weekly overview data."""
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    # Tasks completed this week
    tasks_completed = db.query(Task).filter(
        and_(
            Task.status == TaskStatus.DONE,
            Task.completed_at >= datetime.combine(start_of_week, datetime.min.time()),
            Task.completed_at <= datetime.combine(end_of_week, datetime.max.time())
        )
    ).count()
    
    # Health data for week
    health_logs = db.query(HealthLog).filter(
        and_(
            HealthLog.log_date >= start_of_week,
            HealthLog.log_date <= end_of_week
        )
    ).all()
    
    # Habits completion rate
    habits = db.query(Habit).filter(Habit.is_active == True).all()
    total_habit_checks = 0
    completed_habits = 0
    for habit in habits:
        logs = db.query(HabitLog).filter(
            and_(
                HabitLog.habit_id == habit.id,
                HabitLog.log_date >= start_of_week,
                HabitLog.log_date <= end_of_week
            )
        ).all()
        total_habit_checks += 7  # Simplified - assuming daily
        completed_habits += sum(1 for l in logs if l.completed)
    
    # Expenses this week
    week_expenses = db.query(func.sum(Transaction.amount)).filter(
        and_(
            Transaction.type == TransactionType.EXPENSE,
            Transaction.date >= datetime.combine(start_of_week, datetime.min.time()),
            Transaction.date <= datetime.combine(end_of_week, datetime.max.time())
        )
    ).scalar() or 0
    
    return {
        "week_start": start_of_week.isoformat(),
        "week_end": end_of_week.isoformat(),
        "tasks_completed": tasks_completed,
        "health": {
            "avg_sleep": round(sum(float(h.sleep_hours) for h in health_logs if h.sleep_hours) / max(len([h for h in health_logs if h.sleep_hours]), 1), 1) if health_logs else None,
            "avg_mood": round(sum(h.mood.value for h in health_logs if h.mood) / max(len([h for h in health_logs if h.mood]), 1), 1) if health_logs else None,
            "total_water": sum(h.water_glasses or 0 for h in health_logs),
            "days_logged": len(health_logs)
        },
        "habits": {
            "completion_rate": round(completed_habits / max(total_habit_checks, 1) * 100, 1),
            "completed": completed_habits,
            "total": total_habit_checks
        },
        "expenses": float(week_expenses)
    }
