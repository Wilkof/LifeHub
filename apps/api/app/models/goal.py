"""Goal tracking model."""
from datetime import date, datetime
from sqlalchemy import Column, Integer, String, Text, Date, DateTime, Enum, Boolean, Numeric, JSON
from sqlalchemy.sql import func
import enum

from app.database import Base


class GoalType(str, enum.Enum):
    """Goal type enum."""
    SHORT_TERM = "short_term"  # Days to weeks
    MEDIUM_TERM = "medium_term"  # Weeks to months
    LONG_TERM = "long_term"  # Months to years
    LIFE = "life"  # Life goals


class GoalStatus(str, enum.Enum):
    """Goal status enum."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class GoalCategory(str, enum.Enum):
    """Goal category enum."""
    CAREER = "career"
    FINANCE = "finance"
    HEALTH = "health"
    EDUCATION = "education"
    RELATIONSHIPS = "relationships"
    PERSONAL = "personal"
    TRAVEL = "travel"
    CREATIVE = "creative"
    OTHER = "other"


class Goal(Base):
    """Goal model with progress tracking."""
    __tablename__ = "goals"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic info
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    motivation = Column(Text, nullable=True)  # Why this goal matters
    
    # Classification
    type = Column(Enum(GoalType), default=GoalType.SHORT_TERM)
    category = Column(Enum(GoalCategory), default=GoalCategory.PERSONAL)
    status = Column(Enum(GoalStatus), default=GoalStatus.NOT_STARTED)
    
    # Hierarchy (for sub-goals)
    parent_id = Column(Integer, nullable=True)  # Reference to parent goal
    
    # Timeline
    start_date = Column(Date, nullable=True)
    target_date = Column(Date, nullable=True)
    completed_date = Column(Date, nullable=True)
    
    # Progress
    progress_percent = Column(Numeric(5, 2), default=0)  # 0-100
    progress_notes = Column(Text, nullable=True)
    
    # Milestones/Subgoals as JSON
    milestones = Column(JSON, default=list)  # [{title, completed, date}]
    
    # Key results (OKR style)
    key_results = Column(JSON, default=list)  # [{title, target, current, unit}]
    
    # Display
    color = Column(String(20), default="#8b5cf6")
    icon = Column(String(50), default="🎯")
    
    # Priority
    priority = Column(Integer, default=0)  # Higher = more important
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<Goal {self.id}: {self.title[:30]}>"
