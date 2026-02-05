"""User settings model."""
from sqlalchemy import Column, Integer, String, Boolean, JSON, DateTime
from sqlalchemy.sql import func

from app.database import Base


class UserSettings(Base):
    """User settings (single-user app, so just one row)."""
    __tablename__ = "user_settings"
    
    id = Column(Integer, primary_key=True, default=1)
    
    # Profile
    name = Column(String(255), default="User")
    language = Column(String(5), default="ua")  # 'ua' or 'pl'
    timezone = Column(String(50), default="Europe/Warsaw")
    
    # Weather
    weather_city = Column(String(255), default="Warsaw")
    weather_country = Column(String(5), default="PL")
    
    # Telegram
    telegram_chat_id = Column(String(50), nullable=True)
    telegram_notifications_enabled = Column(Boolean, default=True)
    
    # Notification schedule (times in HH:MM format)
    morning_briefing_time = Column(String(5), default="08:00")
    midday_reminder_time = Column(String(5), default="13:00")
    evening_checkin_time = Column(String(5), default="21:30")
    weekly_review_day = Column(Integer, default=6)  # 0=Mon, 6=Sun
    weekly_review_time = Column(String(5), default="18:00")
    
    # Notification toggles
    enable_morning_briefing = Column(Boolean, default=True)
    enable_midday_reminder = Column(Boolean, default=True)
    enable_evening_checkin = Column(Boolean, default=True)
    enable_weekly_review = Column(Boolean, default=True)
    enable_deadline_reminders = Column(Boolean, default=True)
    enable_habit_reminders = Column(Boolean, default=True)
    enable_finance_alerts = Column(Boolean, default=True)
    enable_health_alerts = Column(Boolean, default=True)
    
    # Dashboard preferences
    dashboard_widgets = Column(JSON, default=lambda: [
        "weather", "tasks", "habits", "calendar", "health", "finances"
    ])
    
    # Theme (for future)
    theme = Column(String(20), default="light")
    accent_color = Column(String(20), default="#c8e972")  # Lime green from screenshot
    
    # Health targets
    target_sleep_hours = Column(Integer, default=8)
    target_water_glasses = Column(Integer, default=8)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
