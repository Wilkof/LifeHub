"""Goals API router."""
from datetime import date
from typing import List, Optional
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.goal import Goal, GoalType, GoalStatus, GoalCategory
from app.schemas.goal import GoalCreate, GoalUpdate, GoalResponse

router = APIRouter(prefix="/goals", tags=["Goals"])


@router.get("", response_model=List[GoalResponse])
def get_goals(
    type: Optional[GoalType] = None,
    category: Optional[GoalCategory] = None,
    status: Optional[GoalStatus] = None,
    parent_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get all goals with optional filters."""
    query = db.query(Goal)
    
    if type:
        query = query.filter(Goal.type == type)
    if category:
        query = query.filter(Goal.category == category)
    if status:
        query = query.filter(Goal.status == status)
    if parent_id is not None:
        query = query.filter(Goal.parent_id == parent_id)
    
    # Exclude abandoned by default
    if not status:
        query = query.filter(Goal.status != GoalStatus.ABANDONED)
    
    query = query.order_by(Goal.priority.desc(), Goal.target_date.asc().nullslast())
    
    return query.all()


@router.get("/active", response_model=List[GoalResponse])
def get_active_goals(db: Session = Depends(get_db)):
    """Get goals that are in progress."""
    return db.query(Goal).filter(
        Goal.status.in_([GoalStatus.NOT_STARTED, GoalStatus.IN_PROGRESS])
    ).order_by(Goal.priority.desc()).all()


@router.get("/tree")
def get_goals_tree(db: Session = Depends(get_db)):
    """Get goals as hierarchical tree."""
    goals = db.query(Goal).filter(
        Goal.status != GoalStatus.ABANDONED
    ).all()
    
    # Build tree
    goal_dict = {g.id: {
        "id": g.id,
        "title": g.title,
        "type": g.type.value,
        "category": g.category.value,
        "status": g.status.value,
        "progress_percent": float(g.progress_percent),
        "target_date": g.target_date.isoformat() if g.target_date else None,
        "icon": g.icon,
        "color": g.color,
        "children": []
    } for g in goals}
    
    root_goals = []
    for goal in goals:
        if goal.parent_id and goal.parent_id in goal_dict:
            goal_dict[goal.parent_id]["children"].append(goal_dict[goal.id])
        else:
            root_goals.append(goal_dict[goal.id])
    
    return root_goals


@router.get("/{goal_id}", response_model=GoalResponse)
def get_goal(goal_id: int, db: Session = Depends(get_db)):
    """Get a specific goal."""
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return goal


@router.post("", response_model=GoalResponse)
def create_goal(data: GoalCreate, db: Session = Depends(get_db)):
    """Create a new goal."""
    goal = Goal(**data.model_dump())
    db.add(goal)
    db.commit()
    db.refresh(goal)
    return goal


@router.put("/{goal_id}", response_model=GoalResponse)
def update_goal(goal_id: int, data: GoalUpdate, db: Session = Depends(get_db)):
    """Update a goal."""
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    update_data = data.model_dump(exclude_unset=True)
    
    # Auto-complete if progress is 100%
    if update_data.get("progress_percent") == Decimal(100):
        if goal.status != GoalStatus.COMPLETED:
            update_data["status"] = GoalStatus.COMPLETED
            update_data["completed_date"] = date.today()
    
    for field, value in update_data.items():
        setattr(goal, field, value)
    
    db.commit()
    db.refresh(goal)
    return goal


@router.delete("/{goal_id}")
def delete_goal(goal_id: int, db: Session = Depends(get_db)):
    """Delete a goal."""
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    # Check for child goals
    children = db.query(Goal).filter(Goal.parent_id == goal_id).count()
    if children > 0:
        raise HTTPException(status_code=400, detail="Cannot delete goal with sub-goals")
    
    db.delete(goal)
    db.commit()
    return {"message": "Goal deleted"}


@router.post("/{goal_id}/progress", response_model=GoalResponse)
def update_progress(
    goal_id: int,
    progress: Decimal = Query(..., ge=0, le=100),
    notes: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Update goal progress."""
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    goal.progress_percent = progress
    if notes:
        goal.progress_notes = notes
    
    # Auto-complete if 100%
    if progress == Decimal(100) and goal.status != GoalStatus.COMPLETED:
        goal.status = GoalStatus.COMPLETED
        goal.completed_date = date.today()
    elif progress < Decimal(100) and goal.status == GoalStatus.COMPLETED:
        goal.status = GoalStatus.IN_PROGRESS
        goal.completed_date = None
    
    db.commit()
    db.refresh(goal)
    return goal


@router.post("/{goal_id}/start", response_model=GoalResponse)
def start_goal(goal_id: int, db: Session = Depends(get_db)):
    """Start working on a goal."""
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    goal.status = GoalStatus.IN_PROGRESS
    if not goal.start_date:
        goal.start_date = date.today()
    
    db.commit()
    db.refresh(goal)
    return goal
