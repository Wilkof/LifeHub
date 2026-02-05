"""Health tracking API router."""
from datetime import date, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from app.database import get_db
from app.models.health import HealthLog
from app.schemas.health import HealthLogCreate, HealthLogUpdate, HealthLogResponse

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/logs", response_model=List[HealthLogResponse])
def get_health_logs(
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    limit: int = Query(30, le=365),
    db: Session = Depends(get_db)
):
    """Get health logs with optional date range."""
    query = db.query(HealthLog)
    
    if date_from:
        query = query.filter(HealthLog.log_date >= date_from)
    if date_to:
        query = query.filter(HealthLog.log_date <= date_to)
    
    query = query.order_by(HealthLog.log_date.desc())
    
    return query.limit(limit).all()


@router.get("/logs/today", response_model=Optional[HealthLogResponse])
def get_today_log(db: Session = Depends(get_db)):
    """Get today's health log."""
    today = date.today()
    log = db.query(HealthLog).filter(HealthLog.log_date == today).first()
    return log


@router.get("/logs/{log_date}", response_model=HealthLogResponse)
def get_health_log(log_date: date, db: Session = Depends(get_db)):
    """Get health log for a specific date."""
    log = db.query(HealthLog).filter(HealthLog.log_date == log_date).first()
    if not log:
        raise HTTPException(status_code=404, detail="Health log not found")
    return log


@router.post("/logs", response_model=HealthLogResponse)
def create_health_log(data: HealthLogCreate, db: Session = Depends(get_db)):
    """Create a new health log."""
    # Check if log for this date exists
    existing = db.query(HealthLog).filter(HealthLog.log_date == data.log_date).first()
    if existing:
        raise HTTPException(status_code=400, detail="Log for this date already exists. Use PUT to update.")
    
    log = HealthLog(**data.model_dump())
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


@router.put("/logs/{log_date}", response_model=HealthLogResponse)
def update_health_log(log_date: date, data: HealthLogUpdate, db: Session = Depends(get_db)):
    """Update a health log (or create if doesn't exist)."""
    log = db.query(HealthLog).filter(HealthLog.log_date == log_date).first()
    
    if not log:
        # Create new log
        log = HealthLog(log_date=log_date, **data.model_dump(exclude_unset=True))
        db.add(log)
    else:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(log, field, value)
    
    db.commit()
    db.refresh(log)
    return log


@router.post("/logs/water")
def add_water(glasses: int = 1, db: Session = Depends(get_db)):
    """Add water intake for today."""
    today = date.today()
    log = db.query(HealthLog).filter(HealthLog.log_date == today).first()
    
    if not log:
        log = HealthLog(log_date=today, water_glasses=glasses)
        db.add(log)
    else:
        log.water_glasses = (log.water_glasses or 0) + glasses
    
    db.commit()
    db.refresh(log)
    return {"water_glasses": log.water_glasses}


@router.get("/stats/weekly")
def get_weekly_stats(db: Session = Depends(get_db)):
    """Get health stats for the past week."""
    today = date.today()
    week_ago = today - timedelta(days=7)
    
    logs = db.query(HealthLog).filter(
        and_(
            HealthLog.log_date >= week_ago,
            HealthLog.log_date <= today
        )
    ).all()
    
    # Calculate averages
    sleep_hours = [float(l.sleep_hours) for l in logs if l.sleep_hours]
    water_glasses = [l.water_glasses for l in logs if l.water_glasses]
    moods = [l.mood.value for l in logs if l.mood]
    
    return {
        "days_logged": len(logs),
        "avg_sleep_hours": round(sum(sleep_hours) / len(sleep_hours), 1) if sleep_hours else None,
        "avg_water_glasses": round(sum(water_glasses) / len(water_glasses), 1) if water_glasses else None,
        "avg_mood": round(sum(moods) / len(moods), 1) if moods else None,
        "total_water": sum(water_glasses),
        "logs": [
            {
                "date": l.log_date.isoformat(),
                "sleep_hours": float(l.sleep_hours) if l.sleep_hours else None,
                "water_glasses": l.water_glasses,
                "mood": l.mood.value if l.mood else None,
                "energy": l.energy_level
            }
            for l in sorted(logs, key=lambda x: x.log_date)
        ]
    }


@router.get("/alerts")
def get_health_alerts(db: Session = Depends(get_db)):
    """Get health alerts based on recent data."""
    today = date.today()
    yesterday = today - timedelta(days=1)
    two_days_ago = today - timedelta(days=2)
    
    alerts = []
    
    # Check last 2 days for sleep
    recent_logs = db.query(HealthLog).filter(
        HealthLog.log_date.in_([yesterday, two_days_ago])
    ).all()
    
    low_sleep_days = [l for l in recent_logs if l.sleep_hours and float(l.sleep_hours) < 6]
    if len(low_sleep_days) >= 2:
        alerts.append({
            "type": "sleep",
            "severity": "warning",
            "message": "Ви спали менше 6 годин 2 дні поспіль. Рекомендуємо лягти раніше сьогодні."
        })
    
    # Check today's water
    today_log = db.query(HealthLog).filter(HealthLog.log_date == today).first()
    if today_log and (today_log.water_glasses or 0) < 4:
        alerts.append({
            "type": "water",
            "severity": "info",
            "message": f"Ви випили тільки {today_log.water_glasses or 0} склянок води. Не забудьте пити більше!"
        })
    
    return alerts
