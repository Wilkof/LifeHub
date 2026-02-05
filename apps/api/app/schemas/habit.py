"""Habit schemas."""
from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field

from app.models.habit import HabitFrequency


class HabitBase(BaseModel):
    """Base habit schema."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    icon: str = "✓"
    color: str = "#10b981"
    frequency: HabitFrequency = HabitFrequency.DAILY
    target_per_week: int = Field(7, ge=1, le=7)
    custom_days: List[int] = []
    preferred_time: Optional[str] = None
    is_active: bool = True
    display_order: int = 0


class HabitCreate(HabitBase):
    """Schema for creating a habit."""
    pass


class HabitUpdate(BaseModel):
    """Schema for updating a habit."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    frequency: Optional[HabitFrequency] = None
    target_per_week: Optional[int] = Field(None, ge=1, le=7)
    custom_days: Optional[List[int]] = None
    preferred_time: Optional[str] = None
    is_active: Optional[bool] = None
    display_order: Optional[int] = None


class HabitResponse(HabitBase):
    """Habit response schema."""
    id: int
    current_streak: int
    longest_streak: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Habit log schemas
class HabitLogCreate(BaseModel):
    """Schema for logging habit completion."""
    habit_id: int
    log_date: date
    completed: bool = True
    notes: Optional[str] = None


class HabitLogResponse(BaseModel):
    """Habit log response schema."""
    id: int
    habit_id: int
    log_date: date
    completed: bool
    completed_at: Optional[datetime] = None
    notes: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
