"""Note schemas."""
from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, Field

from app.models.note import NoteType


class NoteBase(BaseModel):
    """Base note schema."""
    title: Optional[str] = Field(None, max_length=500)
    content: str = Field(..., min_length=1)
    type: NoteType = NoteType.NOTE
    tags: List[str] = []
    folder: Optional[str] = None
    is_pinned: bool = False
    is_starred: bool = False
    attachments: List[Any] = []
    url: Optional[str] = None
    mood: Optional[int] = Field(None, ge=1, le=5)


class NoteCreate(NoteBase):
    """Schema for creating a note."""
    pass


class NoteUpdate(BaseModel):
    """Schema for updating a note."""
    title: Optional[str] = Field(None, max_length=500)
    content: Optional[str] = Field(None, min_length=1)
    type: Optional[NoteType] = None
    tags: Optional[List[str]] = None
    folder: Optional[str] = None
    is_pinned: Optional[bool] = None
    is_starred: Optional[bool] = None
    attachments: Optional[List[Any]] = None
    url: Optional[str] = None
    mood: Optional[int] = Field(None, ge=1, le=5)
    is_archived: Optional[bool] = None


class NoteResponse(NoteBase):
    """Note response schema."""
    id: int
    is_archived: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
