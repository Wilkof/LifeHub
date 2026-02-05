"""Notes and journal model."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, Boolean, JSON
from sqlalchemy.sql import func
import enum

from app.database import Base


class NoteType(str, enum.Enum):
    """Note type enum."""
    NOTE = "note"
    JOURNAL = "journal"
    INBOX = "inbox"  # Quick capture / inbox thoughts
    IDEA = "idea"
    MEETING = "meeting"
    BOOKMARK = "bookmark"


class Note(Base):
    """Note/journal entry model."""
    __tablename__ = "notes"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic info
    title = Column(String(500), nullable=True)
    content = Column(Text, nullable=False)
    
    # Type
    type = Column(Enum(NoteType), default=NoteType.NOTE)
    
    # Organization
    tags = Column(JSON, default=list)
    folder = Column(String(255), nullable=True)
    
    # Pinned/Starred
    is_pinned = Column(Boolean, default=False)
    is_starred = Column(Boolean, default=False)
    
    # Attachments (v2)
    attachments = Column(JSON, default=list)  # [{name, url, type}]
    
    # Links (for bookmarks)
    url = Column(String(1000), nullable=True)
    
    # For journal entries
    mood = Column(Integer, nullable=True)  # 1-5
    
    # Search
    is_archived = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        title = self.title or self.content[:30]
        return f"<Note {self.id}: {title}>"
