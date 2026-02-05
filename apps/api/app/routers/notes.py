"""Notes API router."""
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database import get_db
from app.models.note import Note, NoteType
from app.schemas.note import NoteCreate, NoteUpdate, NoteResponse

router = APIRouter(prefix="/notes", tags=["Notes"])


@router.get("", response_model=List[NoteResponse])
def get_notes(
    type: Optional[NoteType] = None,
    folder: Optional[str] = None,
    tag: Optional[str] = None,
    search: Optional[str] = None,
    pinned_only: bool = False,
    starred_only: bool = False,
    include_archived: bool = False,
    limit: int = Query(50, le=200),
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """Get notes with filters."""
    query = db.query(Note)
    
    if type:
        query = query.filter(Note.type == type)
    if folder:
        query = query.filter(Note.folder == folder)
    if tag:
        query = query.filter(Note.tags.contains([tag]))
    if search:
        query = query.filter(
            or_(
                Note.title.ilike(f"%{search}%"),
                Note.content.ilike(f"%{search}%")
            )
        )
    if pinned_only:
        query = query.filter(Note.is_pinned == True)
    if starred_only:
        query = query.filter(Note.is_starred == True)
    if not include_archived:
        query = query.filter(Note.is_archived == False)
    
    # Order: pinned first, then by updated_at
    query = query.order_by(Note.is_pinned.desc(), Note.updated_at.desc())
    
    return query.offset(offset).limit(limit).all()


@router.get("/inbox", response_model=List[NoteResponse])
def get_inbox(db: Session = Depends(get_db)):
    """Get inbox notes (quick captures)."""
    return db.query(Note).filter(
        Note.type == NoteType.INBOX,
        Note.is_archived == False
    ).order_by(Note.created_at.desc()).limit(20).all()


@router.get("/journal", response_model=List[NoteResponse])
def get_journal_entries(
    limit: int = Query(30, le=100),
    db: Session = Depends(get_db)
):
    """Get journal entries."""
    return db.query(Note).filter(
        Note.type == NoteType.JOURNAL,
        Note.is_archived == False
    ).order_by(Note.created_at.desc()).limit(limit).all()


@router.get("/folders")
def get_folders(db: Session = Depends(get_db)):
    """Get list of folders."""
    folders = db.query(Note.folder).filter(
        Note.folder.isnot(None),
        Note.is_archived == False
    ).distinct().all()
    
    return [f[0] for f in folders if f[0]]


@router.get("/tags")
def get_tags(db: Session = Depends(get_db)):
    """Get list of all tags."""
    notes = db.query(Note.tags).filter(Note.is_archived == False).all()
    
    all_tags = set()
    for (tags,) in notes:
        if tags:
            all_tags.update(tags)
    
    return sorted(list(all_tags))


@router.get("/{note_id}", response_model=NoteResponse)
def get_note(note_id: int, db: Session = Depends(get_db)):
    """Get a specific note."""
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.post("", response_model=NoteResponse)
def create_note(data: NoteCreate, db: Session = Depends(get_db)):
    """Create a new note."""
    note = Note(**data.model_dump())
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


@router.post("/quick", response_model=NoteResponse)
def quick_note(content: str, db: Session = Depends(get_db)):
    """Create a quick inbox note."""
    note = Note(
        content=content,
        type=NoteType.INBOX
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


@router.put("/{note_id}", response_model=NoteResponse)
def update_note(note_id: int, data: NoteUpdate, db: Session = Depends(get_db)):
    """Update a note."""
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(note, field, value)
    
    db.commit()
    db.refresh(note)
    return note


@router.delete("/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    """Delete a note."""
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    db.delete(note)
    db.commit()
    return {"message": "Note deleted"}


@router.post("/{note_id}/pin", response_model=NoteResponse)
def toggle_pin(note_id: int, db: Session = Depends(get_db)):
    """Toggle pin status."""
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    note.is_pinned = not note.is_pinned
    db.commit()
    db.refresh(note)
    return note


@router.post("/{note_id}/star", response_model=NoteResponse)
def toggle_star(note_id: int, db: Session = Depends(get_db)):
    """Toggle star status."""
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    note.is_starred = not note.is_starred
    db.commit()
    db.refresh(note)
    return note


@router.post("/{note_id}/archive", response_model=NoteResponse)
def toggle_archive(note_id: int, db: Session = Depends(get_db)):
    """Toggle archive status."""
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    note.is_archived = not note.is_archived
    db.commit()
    db.refresh(note)
    return note
