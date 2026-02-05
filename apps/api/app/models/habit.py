"""Habit tracking models."""
from datetime import date, datetime
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Enum, Boolean, JSON
from sqlalchemy.sql import func
import enum

from app.database import Base


class HabitFrequency(str, enum.Enum):
    """Habit frequency enum."""
    DAILY = "daily"
    WEEKDAYS = "weekdays"  # Mon-Fri
    WEEKENDS = "weekends"  # Sat-Sun
    WEEKLY = "weekly"  # X times per week
    CUSTOM = "custom"  # Specific days


class Habit(Base):
    """Habit definition model."""
    __tablename__ = "habits"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic info
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String(50), default="✓")  # Emoji or icon name
    color = Column(String(20), default="#10b981")  # Hex color
    
    # Frequency
    frequency = Column(Enum(HabitFrequency), default=HabitFrequency.DAILY)
    target_per_week = Column(Integer, default=7)  # For WEEKLY frequency
    custom_days = Column(JSON, default=list)  # [0, 1, 2, 3, 4] for Mon-Fri
    
    # Streak tracking
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    
    # Time of day (optional)
    preferred_time = Column(String(5), nullable=True)  # "08:00"
    
    # Status
    is_active = Column(Boolean, default=True)
    
    # Order for display
    display_order = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Habit {self.id}: {self.name}>"


class HabitLog(Base):
    """Daily habit completion log."""
    __tablename__ = "habit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    
    habit_id = Column(Integer, nullable=False, index=True)
    log_date = Column(Date, nullable=False, index=True)
    
    # Completion
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Notes
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    class Config:
        # Unique constraint on habit_id + log_date
        pass
    
    def __repr__(self):
        return f"<HabitLog {self.habit_id} @ {self.log_date}: {self.completed}>"
