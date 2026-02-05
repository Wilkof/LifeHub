"""Health schemas."""
from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field

from app.models.health import MoodLevel, SleepQuality


class HealthLogBase(BaseModel):
    """Base health log schema."""
    log_date: date
    sleep_hours: Optional[Decimal] = Field(None, ge=0, le=24)
    sleep_quality: Optional[SleepQuality] = None
    sleep_notes: Optional[str] = None
    water_glasses: int = Field(0, ge=0, le=50)
    mood: Optional[MoodLevel] = None
    mood_notes: Optional[str] = None
    weight_kg: Optional[Decimal] = Field(None, ge=20, le=500)
    steps: Optional[int] = Field(None, ge=0)
    energy_level: Optional[int] = Field(None, ge=1, le=5)
    notes: Optional[str] = None


class HealthLogCreate(HealthLogBase):
    """Schema for creating a health log."""
    pass


class HealthLogUpdate(BaseModel):
    """Schema for updating a health log."""
    sleep_hours: Optional[Decimal] = Field(None, ge=0, le=24)
    sleep_quality: Optional[SleepQuality] = None
    sleep_notes: Optional[str] = None
    water_glasses: Optional[int] = Field(None, ge=0, le=50)
    mood: Optional[MoodLevel] = None
    mood_notes: Optional[str] = None
    weight_kg: Optional[Decimal] = Field(None, ge=20, le=500)
    steps: Optional[int] = Field(None, ge=0)
    energy_level: Optional[int] = Field(None, ge=1, le=5)
    notes: Optional[str] = None


class HealthLogResponse(HealthLogBase):
    """Health log response schema."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
