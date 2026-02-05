"""Telegram bot service."""
from datetime import date, datetime
from typing import Optional
import httpx
from sqlalchemy.orm import Session

from app.config import settings
from app.models.settings import UserSettings
from app.models.task import Task, TaskStatus


class TelegramService:
    """Service for Telegram bot interactions."""
    
    BASE_URL = "https://api.telegram.org/bot"
    
    def __init__(self, db: Session):
        self.db = db
        self.token = settings.telegram_bot_token
        self.api_url = f"{self.BASE_URL}{self.token}"
    
    def _get_chat_id(self) -> Optional[str]:
        """Get registered chat ID from settings."""
        user_settings = self.db.query(UserSettings).first()
        if user_settings and user_settings.telegram_chat_id:
            return user_settings.telegram_chat_id
        return settings.telegram_chat_id
    
    async def send_message(
        self,
        text: str,
        chat_id: Optional[str] = None,
        parse_mode: str = "HTML"
    ) -> bool:
        """Send a message to Telegram."""
        if not self.token:
            print("Telegram bot token not configured")
            return False
        
        chat_id = chat_id or self._get_chat_id()
        if not chat_id:
            print("No chat ID configured")
            return False
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/sendMessage",
                    json={
                        "chat_id": chat_id,
                        "text": text,
                        "parse_mode": parse_mode
                    }
                )
                response.raise_for_status()
                return True
        except Exception as e:
            print(f"Telegram send error: {e}")
            return False
    
    async def handle_update(self, update: dict):
        """Handle incoming Telegram update."""
        if "message" not in update:
            return
        
        message = update["message"]
        chat_id = str(message["chat"]["id"])
        text = message.get("text", "")
        
        # Process commands
        if text.startswith("/"):
            await self._handle_command(chat_id, text)
    
    async def _handle_command(self, chat_id: str, text: str):
        """Handle bot commands."""
        parts = text.split(maxsplit=1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        if command == "/start":
            await self._cmd_start(chat_id)
        elif command == "/help":
            await self._cmd_help(chat_id)
        elif command == "/today":
            await self._cmd_today(chat_id)
        elif command == "/add":
            await self._cmd_add(chat_id, args)
        elif command == "/done":
            await self._cmd_done(chat_id, args)
        elif command == "/week":
            await self._cmd_week(chat_id)
        elif command == "/water":
            await self._cmd_water(chat_id)
        else:
            await self.send_message("Невідома команда. Напиши /help для списку команд.", chat_id)
    
    async def _cmd_start(self, chat_id: str):
        """Handle /start command - register chat."""
        # Save chat ID to settings
        user_settings = self.db.query(UserSettings).first()
        if not user_settings:
            user_settings = UserSettings(id=1)
            self.db.add(user_settings)
        
        user_settings.telegram_chat_id = chat_id
        self.db.commit()
        
        await self.send_message(
            "👋 <b>Вітаю у LifeHub!</b>\n\n"
            "✅ Твій Telegram зареєстровано для сповіщень.\n\n"
            "Тепер ти будеш отримувати:\n"
            "• Ранкові брифінги\n"
            "• Нагадування про задачі\n"
            "• Вечірні чек-іни\n\n"
            "Напиши /help для списку команд.",
            chat_id
        )
    
    async def _cmd_help(self, chat_id: str):
        """Handle /help command."""
        await self.send_message(
            "📚 <b>Команди LifeHub:</b>\n\n"
            "/today - Задачі на сьогодні\n"
            "/add &lt;текст&gt; - Додати задачу\n"
            "/done &lt;id&gt; - Завершити задачу\n"
            "/week - Огляд тижня\n"
            "/water - Додати склянку води\n"
            "/help - Ця довідка",
            chat_id
        )
    
    async def _cmd_today(self, chat_id: str):
        """Handle /today command - show today's tasks."""
        tasks = self.db.query(Task).filter(
            Task.status.in_([TaskStatus.TODO, TaskStatus.IN_PROGRESS])
        ).order_by(Task.is_mit.desc(), Task.priority.desc()).limit(10).all()
        
        if not tasks:
            await self.send_message("✨ Немає активних задач! Час відпочити або додати нові.", chat_id)
            return
        
        # Format tasks
        mit_tasks = [t for t in tasks if t.is_mit]
        other_tasks = [t for t in tasks if not t.is_mit]
        
        text = "📋 <b>Задачі на сьогодні:</b>\n\n"
        
        if mit_tasks:
            text += "🎯 <b>MIT (Найважливіші):</b>\n"
            for t in mit_tasks:
                status = "⏳" if t.status == TaskStatus.IN_PROGRESS else "⬜"
                text += f"{status} [{t.id}] {t.title}\n"
            text += "\n"
        
        if other_tasks:
            text += "📝 <b>Інші задачі:</b>\n"
            for t in other_tasks[:7]:
                status = "⏳" if t.status == TaskStatus.IN_PROGRESS else "⬜"
                text += f"{status} [{t.id}] {t.title}\n"
        
        await self.send_message(text, chat_id)
    
    async def _cmd_add(self, chat_id: str, args: str):
        """Handle /add command - add a new task."""
        if not args:
            await self.send_message("❌ Вкажи текст задачі: /add Назва задачі", chat_id)
            return
        
        task = Task(title=args.strip(), status=TaskStatus.TODO)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        
        await self.send_message(
            f"✅ Задачу додано!\n\n"
            f"<b>{task.title}</b>\n"
            f"ID: {task.id}",
            chat_id
        )
    
    async def _cmd_done(self, chat_id: str, args: str):
        """Handle /done command - complete a task."""
        if not args:
            await self.send_message("❌ Вкажи ID задачі: /done 123", chat_id)
            return
        
        try:
            task_id = int(args.strip())
        except ValueError:
            await self.send_message("❌ Невірний ID задачі", chat_id)
            return
        
        task = self.db.query(Task).filter(Task.id == task_id).first()
        if not task:
            await self.send_message("❌ Задачу не знайдено", chat_id)
            return
        
        task.status = TaskStatus.DONE
        task.completed_at = datetime.utcnow()
        self.db.commit()
        
        await self.send_message(
            f"🎉 <b>Задачу виконано!</b>\n\n"
            f"✅ {task.title}",
            chat_id
        )
    
    async def _cmd_week(self, chat_id: str):
        """Handle /week command - weekly summary."""
        from datetime import timedelta
        from sqlalchemy import and_
        
        today = date.today()
        week_ago = today - timedelta(days=7)
        
        # Completed tasks
        completed = self.db.query(Task).filter(
            and_(
                Task.status == TaskStatus.DONE,
                Task.completed_at >= datetime.combine(week_ago, datetime.min.time())
            )
        ).count()
        
        # Pending tasks
        pending = self.db.query(Task).filter(
            Task.status.in_([TaskStatus.TODO, TaskStatus.IN_PROGRESS])
        ).count()
        
        text = (
            f"📊 <b>Огляд тижня:</b>\n\n"
            f"✅ Виконано задач: {completed}\n"
            f"⏳ Залишилось: {pending}\n"
        )
        
        await self.send_message(text, chat_id)
    
    async def _cmd_water(self, chat_id: str):
        """Handle /water command - add water intake."""
        from app.models.health import HealthLog
        
        today = date.today()
        log = self.db.query(HealthLog).filter(HealthLog.log_date == today).first()
        
        if not log:
            log = HealthLog(log_date=today, water_glasses=1)
            self.db.add(log)
        else:
            log.water_glasses = (log.water_glasses or 0) + 1
        
        self.db.commit()
        
        glasses = log.water_glasses
        progress = "💧" * min(glasses, 8) + "⚪" * max(0, 8 - glasses)
        
        await self.send_message(
            f"💧 <b>Воду додано!</b>\n\n"
            f"{progress}\n"
            f"Сьогодні: {glasses} склянок",
            chat_id
        )


# Functions for scheduled notifications
async def send_morning_briefing(db: Session):
    """Send morning briefing notification."""
    from app.services.openai_service import OpenAIService
    from app.services.weather_service import WeatherService
    
    telegram = TelegramService(db)
    
    # Get weather
    weather_service = WeatherService()
    user_settings = db.query(UserSettings).first()
    city = user_settings.weather_city if user_settings else settings.default_city
    weather = await weather_service.get_current_weather(city)
    
    # Get MIT tasks
    mit_tasks = db.query(Task).filter(
        Task.is_mit == True,
        Task.status.in_([TaskStatus.TODO, TaskStatus.IN_PROGRESS])
    ).limit(3).all()
    
    # Get other tasks
    other_tasks = db.query(Task).filter(
        Task.status.in_([TaskStatus.TODO, TaskStatus.IN_PROGRESS]),
        Task.is_mit == False
    ).order_by(Task.priority.desc()).limit(3).all()
    
    # Build message
    text = f"☀️ <b>Доброго ранку!</b>\n\n"
    text += f"🌤 {weather['city']}: {weather['temperature']}°C, {weather['description']}\n\n"
    
    if mit_tasks:
        text += "🎯 <b>Твої пріоритети:</b>\n"
        for i, t in enumerate(mit_tasks, 1):
            text += f"{i}. {t.title}\n"
        text += "\n"
    
    if other_tasks:
        text += "📝 <b>Також на сьогодні:</b>\n"
        for t in other_tasks:
            text += f"• {t.title}\n"
        text += "\n"
    
    text += "💧 Не забудь випити склянку води!\n"
    text += "💪 Вперед до продуктивного дня!"
    
    await telegram.send_message(text)


async def send_midday_reminder(db: Session):
    """Send midday reminder."""
    telegram = TelegramService(db)
    
    # Check completed tasks today
    today = date.today()
    completed = db.query(Task).filter(
        and_(
            Task.status == TaskStatus.DONE,
            Task.completed_at >= datetime.combine(today, datetime.min.time())
        )
    ).count()
    
    if completed == 0:
        text = (
            "⏰ <b>Час для маленького кроку!</b>\n\n"
            "Ще жодної задачі сьогодні. "
            "Почни з найпростішої на 10 хвилин.\n\n"
            "💧 І не забудь про воду!"
        )
    else:
        text = (
            f"👍 <b>Молодець!</b>\n\n"
            f"Вже виконано задач: {completed}\n"
            f"Продовжуй у тому ж дусі!\n\n"
            "💧 Час для склянки води."
        )
    
    await telegram.send_message(text)


async def send_evening_checkin(db: Session):
    """Send evening check-in."""
    telegram = TelegramService(db)
    
    today = date.today()
    
    # Get today's stats
    completed = db.query(Task).filter(
        and_(
            Task.status == TaskStatus.DONE,
            Task.completed_at >= datetime.combine(today, datetime.min.time())
        )
    ).count()
    
    pending = db.query(Task).filter(
        Task.status.in_([TaskStatus.TODO, TaskStatus.IN_PROGRESS])
    ).count()
    
    text = (
        f"🌙 <b>Вечірній підсумок</b>\n\n"
        f"✅ Виконано сьогодні: {completed}\n"
        f"⏳ Залишилось: {pending}\n\n"
    )
    
    if completed > 0:
        text += "👏 Гарна робота сьогодні!\n\n"
    
    text += "Подумай:\n"
    text += "• Що вдалось сьогодні?\n"
    text += "• Який один крок зробити завтра?\n\n"
    text += "😴 Час для відпочинку!"
    
    await telegram.send_message(text)
