"""Settings schemas."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class SettingsUpdate(BaseModel):
    """Schema for updating settings."""
    name: Optional[str] = Field(None, max_length=255)
    language: Optional[str] = Field(None, pattern="^(ua|pl)$")
    timezone: Optional[str] = None
    
    # Weather
    weather_city: Optional[str] = None
    weather_country: Optional[str] = None
    
    # Telegram
    telegram_chat_id: Optional[str] = None
    telegram_notifications_enabled: Optional[bool] = None
    
    # Notification schedule
    morning_briefing_time: Optional[str] = Field(None, pattern="^[0-2][0-9]:[0-5][0-9]$")
    midday_reminder_time: Optional[str] = Field(None, pattern="^[0-2][0-9]:[0-5][0-9]$")
    evening_checkin_time: Optional[str] = Field(None, pattern="^[0-2][0-9]:[0-5][0-9]$")
    weekly_review_day: Optional[int] = Field(None, ge=0, le=6)
    weekly_review_time: Optional[str] = Field(None, pattern="^[0-2][0-9]:[0-5][0-9]$")
    
    # Notification toggles
    enable_morning_briefing: Optional[bool] = None
    enable_midday_reminder: Optional[bool] = None
    enable_evening_checkin: Optional[bool] = None
    enable_weekly_review: Optional[bool] = None
    enable_deadline_reminders: Optional[bool] = None
    enable_habit_reminders: Optional[bool] = None
    enable_finance_alerts: Optional[bool] = None
    enable_health_alerts: Optional[bool] = None
    
    # Dashboard
    dashboard_widgets: Optional[List[str]] = None
    
    # Theme
    theme: Optional[str] = None
    accent_color: Optional[str] = None
    
    # Health targets
    target_sleep_hours: Optional[int] = Field(None, ge=4, le=12)
    target_water_glasses: Optional[int] = Field(None, ge=1, le=20)


class SettingsResponse(BaseModel):
    """Settings response schema."""
    id: int
    name: str
    language: str
    timezone: str
    
    # Weather
    weather_city: str
    weather_country: str
    
    # Telegram
    telegram_chat_id: Optional[str]
    telegram_notifications_enabled: bool
    
    # Notification schedule
    morning_briefing_time: str
    midday_reminder_time: str
    evening_checkin_time: str
    weekly_review_day: int
    weekly_review_time: str
    
    # Notification toggles
    enable_morning_briefing: bool
    enable_midday_reminder: bool
    enable_evening_checkin: bool
    enable_weekly_review: bool
    enable_deadline_reminders: bool
    enable_habit_reminders: bool
    enable_finance_alerts: bool
    enable_health_alerts: bool
    
    # Dashboard
    dashboard_widgets: List[str]
    
    # Theme
    theme: str
    accent_color: str
    
    # Health targets
    target_sleep_hours: int
    target_water_glasses: int
    
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
