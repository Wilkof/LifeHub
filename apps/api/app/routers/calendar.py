"""Calendar API router."""
from datetime import datetime, date, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.database import get_db
from app.models.calendar_event import CalendarEvent, EventType
from app.schemas.calendar_event import EventCreate, EventUpdate, EventResponse

router = APIRouter(prefix="/calendar", tags=["Calendar"])


@router.get("/events", response_model=List[EventResponse])
def get_events(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    event_type: Optional[EventType] = None,
    db: Session = Depends(get_db)
):
    """Get calendar events with optional date range filter."""
    query = db.query(CalendarEvent)
    
    # Default to current month if no dates provided
    if not start_date:
        start_date = date.today().replace(day=1)
    if not end_date:
        # End of current month
        next_month = start_date.replace(day=28) + timedelta(days=4)
        end_date = next_month - timedelta(days=next_month.day)
    
    start_datetime = datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.combine(end_date, datetime.max.time())
    
    query = query.filter(
        and_(
            CalendarEvent.start_time >= start_datetime,
            CalendarEvent.start_time <= end_datetime
        )
    )
    
    if event_type:
        query = query.filter(CalendarEvent.event_type == event_type)
    
    query = query.order_by(CalendarEvent.start_time.asc())
    
    return query.all()


@router.get("/events/today", response_model=List[EventResponse])
def get_today_events(db: Session = Depends(get_db)):
    """Get events for today."""
    today = date.today()
    today_start = datetime.combine(today, datetime.min.time())
    today_end = datetime.combine(today, datetime.max.time())
    
    query = db.query(CalendarEvent).filter(
        and_(
            CalendarEvent.start_time >= today_start,
            CalendarEvent.start_time <= today_end
        )
    ).order_by(CalendarEvent.start_time.asc())
    
    return query.all()


@router.get("/events/week", response_model=List[EventResponse])
def get_week_events(db: Session = Depends(get_db)):
    """Get events for the current week."""
    today = date.today()
    # Start from Monday
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    start_datetime = datetime.combine(start_of_week, datetime.min.time())
    end_datetime = datetime.combine(end_of_week, datetime.max.time())
    
    query = db.query(CalendarEvent).filter(
        and_(
            CalendarEvent.start_time >= start_datetime,
            CalendarEvent.start_time <= end_datetime
        )
    ).order_by(CalendarEvent.start_time.asc())
    
    return query.all()


@router.get("/events/{event_id}", response_model=EventResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    """Get a specific event."""
    event = db.query(CalendarEvent).filter(CalendarEvent.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event


@router.post("/events", response_model=EventResponse)
def create_event(event_data: EventCreate, db: Session = Depends(get_db)):
    """Create a new event."""
    event = CalendarEvent(**event_data.model_dump())
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


@router.put("/events/{event_id}", response_model=EventResponse)
def update_event(event_id: int, event_data: EventUpdate, db: Session = Depends(get_db)):
    """Update an event."""
    event = db.query(CalendarEvent).filter(CalendarEvent.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    update_data = event_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(event, field, value)
    
    db.commit()
    db.refresh(event)
    return event


@router.delete("/events/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db)):
    """Delete an event."""
    event = db.query(CalendarEvent).filter(CalendarEvent.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    db.delete(event)
    db.commit()
    return {"message": "Event deleted"}


@router.get("/export/ical")
def export_ical(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Export events as iCal format."""
    from fastapi.responses import Response
    
    # Get events
    query = db.query(CalendarEvent)
    if start_date:
        query = query.filter(CalendarEvent.start_time >= datetime.combine(start_date, datetime.min.time()))
    if end_date:
        query = query.filter(CalendarEvent.start_time <= datetime.combine(end_date, datetime.max.time()))
    
    events = query.all()
    
    # Build iCal content
    ical_lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//LifeHub//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
    ]
    
    for event in events:
        ical_lines.extend([
            "BEGIN:VEVENT",
            f"UID:{event.id}@lifehub",
            f"DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}",
            f"DTSTART:{event.start_time.strftime('%Y%m%dT%H%M%SZ')}",
        ])
        
        if event.end_time:
            ical_lines.append(f"DTEND:{event.end_time.strftime('%Y%m%dT%H%M%SZ')}")
        
        ical_lines.append(f"SUMMARY:{event.title}")
        
        if event.description:
            ical_lines.append(f"DESCRIPTION:{event.description}")
        if event.location:
            ical_lines.append(f"LOCATION:{event.location}")
        
        ical_lines.append("END:VEVENT")
    
    ical_lines.append("END:VCALENDAR")
    
    ical_content = "\r\n".join(ical_lines)
    
    return Response(
        content=ical_content,
        media_type="text/calendar",
        headers={"Content-Disposition": "attachment; filename=lifehub-calendar.ics"}
    )
