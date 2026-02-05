"""Habits API router."""
from datetime import date, datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from app.database import get_db
from app.models.habit import Habit, HabitLog, HabitFrequency
from app.schemas.habit import HabitCreate, HabitUpdate, HabitResponse, HabitLogCreate, HabitLogResponse

router = APIRouter(prefix="/habits", tags=["Habits"])


def calculate_streak(habit_id: int, db: Session) -> int:
    """Calculate current streak for a habit."""
    today = date.today()
    streak = 0
    current_date = today
    
    while True:
        log = db.query(HabitLog).filter(
            and_(
                HabitLog.habit_id == habit_id,
                HabitLog.log_date == current_date,
                HabitLog.completed == True
            )
        ).first()
        
        if log:
            streak += 1
            current_date -= timedelta(days=1)
        else:
            break
    
    return streak


@router.get("", response_model=List[HabitResponse])
def get_habits(
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """Get all habits."""
    query = db.query(Habit)
    if active_only:
        query = query.filter(Habit.is_active == True)
    return query.order_by(Habit.display_order.asc()).all()


@router.get("/today")
def get_today_habits(db: Session = Depends(get_db)):
    """Get habits for today with completion status."""
    today = date.today()
    weekday = today.weekday()  # 0 = Monday
    
    habits = db.query(Habit).filter(Habit.is_active == True).all()
    
    result = []
    for habit in habits:
        # Check if habit is scheduled for today
        should_track = False
        if habit.frequency == HabitFrequency.DAILY:
            should_track = True
        elif habit.frequency == HabitFrequency.WEEKDAYS:
            should_track = weekday < 5
        elif habit.frequency == HabitFrequency.WEEKENDS:
            should_track = weekday >= 5
        elif habit.frequency == HabitFrequency.CUSTOM:
            should_track = weekday in (habit.custom_days or [])
        else:
            should_track = True
        
        if should_track:
            # Check if completed today
            log = db.query(HabitLog).filter(
                and_(
                    HabitLog.habit_id == habit.id,
                    HabitLog.log_date == today
                )
            ).first()
            
            result.append({
                "id": habit.id,
                "name": habit.name,
                "icon": habit.icon,
                "color": habit.color,
                "completed": log.completed if log else False,
                "current_streak": habit.current_streak,
                "preferred_time": habit.preferred_time
            })
    
    return result


@router.get("/{habit_id}", response_model=HabitResponse)
def get_habit(habit_id: int, db: Session = Depends(get_db)):
    """Get a specific habit."""
    habit = db.query(Habit).filter(Habit.id == habit_id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return habit


@router.post("", response_model=HabitResponse)
def create_habit(data: HabitCreate, db: Session = Depends(get_db)):
    """Create a new habit."""
    habit = Habit(**data.model_dump())
    db.add(habit)
    db.commit()
    db.refresh(habit)
    return habit


@router.put("/{habit_id}", response_model=HabitResponse)
def update_habit(habit_id: int, data: HabitUpdate, db: Session = Depends(get_db)):
    """Update a habit."""
    habit = db.query(Habit).filter(Habit.id == habit_id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(habit, field, value)
    
    db.commit()
    db.refresh(habit)
    return habit


@router.delete("/{habit_id}")
def delete_habit(habit_id: int, db: Session = Depends(get_db)):
    """Delete a habit."""
    habit = db.query(Habit).filter(Habit.id == habit_id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    # Delete associated logs
    db.query(HabitLog).filter(HabitLog.habit_id == habit_id).delete()
    db.delete(habit)
    db.commit()
    return {"message": "Habit deleted"}


@router.post("/{habit_id}/complete")
def complete_habit(habit_id: int, log_date: Optional[date] = None, db: Session = Depends(get_db)):
    """Mark a habit as completed for a date (default: today)."""
    habit = db.query(Habit).filter(Habit.id == habit_id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    if not log_date:
        log_date = date.today()
    
    # Check if log exists
    log = db.query(HabitLog).filter(
        and_(
            HabitLog.habit_id == habit_id,
            HabitLog.log_date == log_date
        )
    ).first()
    
    if log:
        log.completed = True
        log.completed_at = datetime.utcnow()
    else:
        log = HabitLog(
            habit_id=habit_id,
            log_date=log_date,
            completed=True,
            completed_at=datetime.utcnow()
        )
        db.add(log)
    
    # Update streak
    habit.current_streak = calculate_streak(habit_id, db)
    if habit.current_streak > habit.longest_streak:
        habit.longest_streak = habit.current_streak
    
    db.commit()
    
    return {
        "habit_id": habit_id,
        "log_date": log_date.isoformat(),
        "completed": True,
        "current_streak": habit.current_streak
    }


@router.post("/{habit_id}/uncomplete")
def uncomplete_habit(habit_id: int, log_date: Optional[date] = None, db: Session = Depends(get_db)):
    """Unmark a habit completion for a date (default: today)."""
    habit = db.query(Habit).filter(Habit.id == habit_id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    if not log_date:
        log_date = date.today()
    
    log = db.query(HabitLog).filter(
        and_(
            HabitLog.habit_id == habit_id,
            HabitLog.log_date == log_date
        )
    ).first()
    
    if log:
        log.completed = False
        log.completed_at = None
    
    # Update streak
    habit.current_streak = calculate_streak(habit_id, db)
    
    db.commit()
    
    return {
        "habit_id": habit_id,
        "log_date": log_date.isoformat(),
        "completed": False,
        "current_streak": habit.current_streak
    }


@router.get("/{habit_id}/logs", response_model=List[HabitLogResponse])
def get_habit_logs(
    habit_id: int,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Get logs for a habit."""
    query = db.query(HabitLog).filter(HabitLog.habit_id == habit_id)
    
    if date_from:
        query = query.filter(HabitLog.log_date >= date_from)
    if date_to:
        query = query.filter(HabitLog.log_date <= date_to)
    
    return query.order_by(HabitLog.log_date.desc()).all()


@router.get("/{habit_id}/stats")
def get_habit_stats(
    habit_id: int,
    days: int = Query(30, ge=7, le=365),
    db: Session = Depends(get_db)
):
    """Get habit statistics."""
    habit = db.query(Habit).filter(Habit.id == habit_id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    today = date.today()
    start_date = today - timedelta(days=days)
    
    logs = db.query(HabitLog).filter(
        and_(
            HabitLog.habit_id == habit_id,
            HabitLog.log_date >= start_date,
            HabitLog.log_date <= today
        )
    ).all()
    
    completed_count = sum(1 for log in logs if log.completed)
    
    return {
        "habit_id": habit_id,
        "name": habit.name,
        "days_tracked": days,
        "completed_count": completed_count,
        "completion_rate": round(completed_count / days * 100, 1),
        "current_streak": habit.current_streak,
        "longest_streak": habit.longest_streak
    }
