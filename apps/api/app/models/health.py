"""Health tracking model."""
from datetime import date
from sqlalchemy import Column, Integer, Date, Numeric, Enum, Text, DateTime
from sqlalchemy.sql import func
import enum

from app.database import Base


class MoodLevel(int, enum.Enum):
    """Mood level 1-5."""
    TERRIBLE = 1
    BAD = 2
    OKAY = 3
    GOOD = 4
    GREAT = 5


class SleepQuality(int, enum.Enum):
    """Sleep quality 1-5."""
    VERY_POOR = 1
    POOR = 2
    FAIR = 3
    GOOD = 4
    EXCELLENT = 5


class HealthLog(Base):
    """Daily health log entry."""
    __tablename__ = "health_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Date (one entry per day)
    log_date = Column(Date, nullable=False, unique=True, index=True)
    
    # Sleep
    sleep_hours = Column(Numeric(4, 2), nullable=True)  # e.g., 7.5
    sleep_quality = Column(Enum(SleepQuality), nullable=True)
    sleep_notes = Column(Text, nullable=True)
    
    # Water intake
    water_glasses = Column(Integer, default=0)  # Number of glasses (250ml each)
    
    # Mood
    mood = Column(Enum(MoodLevel), nullable=True)
    mood_notes = Column(Text, nullable=True)
    
    # Weight (optional, v2)
    weight_kg = Column(Numeric(5, 2), nullable=True)
    
    # Steps (optional, v2)
    steps = Column(Integer, nullable=True)
    
    # Energy level (1-5)
    energy_level = Column(Integer, nullable=True)
    
    # General notes
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<HealthLog {self.log_date}>"
