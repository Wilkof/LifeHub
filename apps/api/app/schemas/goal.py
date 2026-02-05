"""Goal schemas."""
from datetime import date, datetime
from decimal import Decimal
from typing import Optional, List, Any
from pydantic import BaseModel, Field

from app.models.goal import GoalType, GoalStatus, GoalCategory


class GoalBase(BaseModel):
    """Base goal schema."""
    title: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None
    motivation: Optional[str] = None
    type: GoalType = GoalType.SHORT_TERM
    category: GoalCategory = GoalCategory.PERSONAL
    status: GoalStatus = GoalStatus.NOT_STARTED
    parent_id: Optional[int] = None
    start_date: Optional[date] = None
    target_date: Optional[date] = None
    progress_percent: Decimal = Field(0, ge=0, le=100)
    progress_notes: Optional[str] = None
    milestones: List[Any] = []
    key_results: List[Any] = []
    color: str = "#8b5cf6"
    icon: str = "🎯"
    priority: int = 0


class GoalCreate(GoalBase):
    """Schema for creating a goal."""
    pass


class GoalUpdate(BaseModel):
    """Schema for updating a goal."""
    title: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = None
    motivation: Optional[str] = None
    type: Optional[GoalType] = None
    category: Optional[GoalCategory] = None
    status: Optional[GoalStatus] = None
    parent_id: Optional[int] = None
    start_date: Optional[date] = None
    target_date: Optional[date] = None
    completed_date: Optional[date] = None
    progress_percent: Optional[Decimal] = Field(None, ge=0, le=100)
    progress_notes: Optional[str] = None
    milestones: Optional[List[Any]] = None
    key_results: Optional[List[Any]] = None
    color: Optional[str] = None
    icon: Optional[str] = None
    priority: Optional[int] = None


class GoalResponse(GoalBase):
    """Goal response schema."""
    id: int
    completed_date: Optional[date] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
