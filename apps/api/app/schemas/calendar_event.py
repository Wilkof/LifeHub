"""Calendar event schemas."""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

from app.models.calendar_event import EventType, RecurrenceType


class EventBase(BaseModel):
    """Base event schema."""
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    location: Optional[str] = None
    event_type: EventType = EventType.PERSONAL
    color: str = "#3b82f6"
    start_time: datetime
    end_time: Optional[datetime] = None
    all_day: bool = False
    recurrence_type: RecurrenceType = RecurrenceType.NONE
    recurrence_end_date: Optional[datetime] = None
    recurrence_days: List[int] = []
    reminders: List[int] = [30]


class EventCreate(EventBase):
    """Schema for creating an event."""
    pass


class EventUpdate(BaseModel):
    """Schema for updating an event."""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = None
    location: Optional[str] = None
    event_type: Optional[EventType] = None
    color: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    all_day: Optional[bool] = None
    recurrence_type: Optional[RecurrenceType] = None
    recurrence_end_date: Optional[datetime] = None
    recurrence_days: Optional[List[int]] = None
    reminders: Optional[List[int]] = None


class EventResponse(EventBase):
    """Event response schema."""
    id: int
    external_id: Optional[str] = None
    ical_uid: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
