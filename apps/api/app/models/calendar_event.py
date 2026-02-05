"""Calendar event model."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum, JSON
from sqlalchemy.sql import func
import enum

from app.database import Base


class EventType(str, enum.Enum):
    """Event type enum."""
    MEETING = "meeting"
    APPOINTMENT = "appointment"
    REMINDER = "reminder"
    DEADLINE = "deadline"
    PERSONAL = "personal"
    WORK = "work"
    HEALTH = "health"
    OTHER = "other"


class RecurrenceType(str, enum.Enum):
    """Recurrence type enum."""
    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    BIWEEKLY = "biweekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


class CalendarEvent(Base):
    """Calendar event model."""
    __tablename__ = "calendar_events"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    location = Column(String(500), nullable=True)
    
    # Type and color
    event_type = Column(Enum(EventType), default=EventType.PERSONAL, nullable=False)
    color = Column(String(20), default="#3b82f6")  # Hex color
    
    # Timing
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=True)
    all_day = Column(Boolean, default=False)
    
    # Recurrence
    recurrence_type = Column(Enum(RecurrenceType), default=RecurrenceType.NONE)
    recurrence_end_date = Column(DateTime(timezone=True), nullable=True)
    recurrence_days = Column(JSON, default=list)  # For weekly: [0, 2, 4] = Mon, Wed, Fri
    
    # Reminders (minutes before)
    reminders = Column(JSON, default=lambda: [30])  # Default: 30 min before
    
    # External sync
    external_id = Column(String(255), nullable=True)  # For Google Calendar sync
    ical_uid = Column(String(255), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<CalendarEvent {self.id}: {self.title[:30]}>"
