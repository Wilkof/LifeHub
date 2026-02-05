"""Tasks API router."""
from datetime import datetime, date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from app.database import get_db
from app.models.task import Task, TaskStatus, TaskPriority
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("", response_model=List[TaskResponse])
def get_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    project: Optional[str] = None,
    is_mit: Optional[bool] = None,
    due_date_from: Optional[date] = None,
    due_date_to: Optional[date] = None,
    search: Optional[str] = None,
    limit: int = Query(100, le=500),
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """Get all tasks with optional filters."""
    query = db.query(Task)
    
    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)
    if project:
        query = query.filter(Task.project == project)
    if is_mit is not None:
        query = query.filter(Task.is_mit == is_mit)
    if due_date_from:
        query = query.filter(Task.due_date >= due_date_from)
    if due_date_to:
        query = query.filter(Task.due_date <= due_date_to)
    if search:
        query = query.filter(
            or_(
                Task.title.ilike(f"%{search}%"),
                Task.description.ilike(f"%{search}%")
            )
        )
    
    # Exclude cancelled by default, order by priority and due date
    query = query.filter(Task.status != TaskStatus.CANCELLED)
    query = query.order_by(Task.priority.desc(), Task.due_date.asc().nullslast(), Task.created_at.desc())
    
    return query.offset(offset).limit(limit).all()


@router.get("/today", response_model=List[TaskResponse])
def get_today_tasks(db: Session = Depends(get_db)):
    """Get tasks for today (MITs and tasks due today)."""
    today = date.today()
    today_start = datetime.combine(today, datetime.min.time())
    today_end = datetime.combine(today, datetime.max.time())
    
    query = db.query(Task).filter(
        and_(
            Task.status.in_([TaskStatus.TODO, TaskStatus.IN_PROGRESS]),
            or_(
                Task.is_mit == True,
                and_(Task.due_date >= today_start, Task.due_date <= today_end)
            )
        )
    ).order_by(Task.is_mit.desc(), Task.priority.desc())
    
    return query.all()


@router.get("/mit", response_model=List[TaskResponse])
def get_mit_tasks(db: Session = Depends(get_db)):
    """Get Most Important Tasks for today."""
    today = date.today()
    today_start = datetime.combine(today, datetime.min.time())
    today_end = datetime.combine(today, datetime.max.time())
    
    query = db.query(Task).filter(
        Task.is_mit == True,
        Task.status.in_([TaskStatus.TODO, TaskStatus.IN_PROGRESS]),
        or_(
            Task.mit_date.is_(None),
            and_(Task.mit_date >= today_start, Task.mit_date <= today_end)
        )
    ).order_by(Task.priority.desc())
    
    return query.limit(3).all()


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    """Get a specific task."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.post("", response_model=TaskResponse)
def create_task(task_data: TaskCreate, db: Session = Depends(get_db)):
    """Create a new task."""
    task = Task(**task_data.model_dump())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_data: TaskUpdate, db: Session = Depends(get_db)):
    """Update a task."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = task_data.model_dump(exclude_unset=True)
    
    # Auto-set completed_at when marking as done
    if update_data.get("status") == TaskStatus.DONE and not task.completed_at:
        update_data["completed_at"] = datetime.utcnow()
    
    for field, value in update_data.items():
        setattr(task, field, value)
    
    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}


@router.post("/{task_id}/complete", response_model=TaskResponse)
def complete_task(task_id: int, db: Session = Depends(get_db)):
    """Mark a task as complete."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.status = TaskStatus.DONE
    task.completed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(task)
    return task


@router.post("/{task_id}/mit", response_model=TaskResponse)
def toggle_mit(task_id: int, db: Session = Depends(get_db)):
    """Toggle MIT status for a task."""
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.is_mit = not task.is_mit
    if task.is_mit:
        task.mit_date = datetime.utcnow()
    else:
        task.mit_date = None
    
    db.commit()
    db.refresh(task)
    return task
