"""AI Assistant API router."""
# pyright: reportMissingImports=false
from datetime import date, datetime, timedelta
from typing import Optional, List
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.config import settings
from app.services.openai_service import OpenAIService, get_openai_service

router = APIRouter(prefix="/ai", tags=["AI Assistant"])


class ChatMessage(BaseModel):
    """Chat message schema."""
    role: str  # "user" or "assistant"
    content: str


class ChatRequest(BaseModel):
    """Chat request schema."""
    message: str
    mode: Optional[str] = "general"  # general, plan_day, break_goal, week_summary, anti_procrastination
    context: Optional[dict] = None


class ChatResponse(BaseModel):
    """Chat response schema."""
    response: str
    mode: str


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    ai_service: OpenAIService = Depends(get_openai_service)
):
    """Chat with AI assistant."""
    # Get user context from database
    context = await get_user_context(db, request.mode)
    if request.context:
        # Allow caller-provided context to extend/override defaults
        context = {**context, **request.context}
    
    # Generate response
    response = await ai_service.chat(
        message=request.message,
        mode=request.mode,
        context=context
    )
    
    return ChatResponse(response=response, mode=request.mode)


@router.post("/plan-day")
async def plan_day(
    db: Session = Depends(get_db),
    ai_service: OpenAIService = Depends(get_openai_service)
):
    """Generate AI-powered daily plan."""
    context = await get_user_context(db, "plan_day")
    
    prompt = """На основі моїх задач, цілей та звичок на сьогодні, створи оптимальний план дня.
    Врахуй пріоритети, дедлайни та мій рівень енергії. 
    Дай конкретні рекомендації по часу та послідовності виконання."""
    
    response = await ai_service.chat(
        message=prompt,
        mode="plan_day",
        context=context
    )
    
    return {"plan": response}


@router.post("/break-goal")
async def break_goal(
    goal_title: str,
    goal_description: Optional[str] = None,
    target_date: Optional[date] = None,
    ai_service: OpenAIService = Depends(get_openai_service)
):
    """Break down a goal into actionable steps."""
    prompt = f"""Розбий цю ціль на конкретні кроки та задачі:

Ціль: {goal_title}
{f'Опис: {goal_description}' if goal_description else ''}
{f'Дедлайн: {target_date}' if target_date else ''}

Дай:
1. 3-5 основних етапів (milestones)
2. Для кожного етапу - конкретні задачі
3. Приблизні часові рамки
4. Ключові показники успіху (KR)"""
    
    response = await ai_service.chat(
        message=prompt,
        mode="break_goal",
        context={}
    )
    
    return {"breakdown": response}


@router.post("/week-summary")
async def week_summary(
    db: Session = Depends(get_db),
    ai_service: OpenAIService = Depends(get_openai_service)
):
    """Generate weekly summary and recommendations."""
    context = await get_user_context(db, "week_summary")
    
    prompt = """Проаналізуй мій тиждень і дай:
1. Що вдалось (виконані задачі, досягнення)
2. Що не вдалось і чому
3. Прогрес по цілях
4. Тренди здоров'я (сон, настрій)
5. 2-3 конкретні рекомендації на наступний тиждень"""
    
    response = await ai_service.chat(
        message=prompt,
        mode="week_summary",
        context=context
    )
    
    return {"summary": response}


@router.post("/anti-procrastination")
async def anti_procrastination(
    task_title: Optional[str] = None,
    ai_service: OpenAIService = Depends(get_openai_service)
):
    """Get anti-procrastination advice."""
    if task_title:
        prompt = f"""Я відкладаю цю задачу: "{task_title}"

Дай мені:
1. Перший мікро-крок на 2 хвилини
2. Чому це важливо зробити зараз
3. Що найгірше може статися, якщо відкладу
4. Мотивуючу фразу"""
    else:
        prompt = """Я прокрастиную і не можу почати працювати.

Дай мені:
1. Просту техніку на 5 хвилин, щоб почати
2. Мотивацію без банальностей
3. Практичну пораду"""
    
    response = await ai_service.chat(
        message=prompt,
        mode="anti_procrastination",
        context={}
    )
    
    return {"advice": response}


@router.get("/daily-briefing")
async def daily_briefing(
    db: Session = Depends(get_db),
    ai_service: OpenAIService = Depends(get_openai_service)
):
    """Generate daily briefing."""
    context = await get_user_context(db, "daily_briefing")
    
    prompt = """Створи короткий ранковий брифінг:
1. Головний фокус дня (1 речення)
2. Три найважливіші задачі
3. Про що не забути
4. Коротка мотивація (персональна, не цитата)"""
    
    response = await ai_service.chat(
        message=prompt,
        mode="daily_briefing",
        context=context
    )
    
    return {"briefing": response}


async def get_user_context(db: Session, mode: str) -> dict:
    """Get relevant user context for AI."""
    from app.models.task import Task, TaskStatus
    from app.models.goal import Goal, GoalStatus
    from app.models.habit import Habit, HabitLog
    from app.models.health import HealthLog
    from app.models.finance import Transaction, TransactionType
    from sqlalchemy import and_, func
    
    today = date.today()
    week_ago = today - timedelta(days=7)
    
    context = {}
    
    # Tasks
    if mode in ["plan_day", "daily_briefing", "week_summary", "general"]:
        tasks_today = db.query(Task).filter(
            Task.status.in_([TaskStatus.TODO, TaskStatus.IN_PROGRESS])
        ).order_by(Task.priority.desc()).limit(10).all()
        
        context["tasks"] = [
            {"title": t.title, "priority": t.priority.value, "is_mit": t.is_mit}
            for t in tasks_today
        ]
    
    # Goals
    if mode in ["plan_day", "week_summary", "general"]:
        goals = db.query(Goal).filter(
            Goal.status.in_([GoalStatus.NOT_STARTED, GoalStatus.IN_PROGRESS])
        ).limit(5).all()
        
        context["goals"] = [
            {"title": g.title, "progress": float(g.progress_percent), "type": g.type.value}
            for g in goals
        ]
    
    # Habits (week summary)
    if mode in ["week_summary", "daily_briefing"]:
        habits = db.query(Habit).filter(Habit.is_active == True).all()
        habit_data = []
        for h in habits:
            completed_this_week = db.query(HabitLog).filter(
                and_(
                    HabitLog.habit_id == h.id,
                    HabitLog.log_date >= week_ago,
                    HabitLog.completed == True
                )
            ).count()
            habit_data.append({
                "name": h.name,
                "streak": h.current_streak,
                "completed_this_week": completed_this_week
            })
        context["habits"] = habit_data
    
    # Health
    if mode in ["week_summary", "daily_briefing"]:
        health_logs = db.query(HealthLog).filter(
            HealthLog.log_date >= week_ago
        ).all()
        
        if health_logs:
            avg_sleep = sum(float(h.sleep_hours) for h in health_logs if h.sleep_hours) / max(len([h for h in health_logs if h.sleep_hours]), 1)
            avg_mood = sum(h.mood.value for h in health_logs if h.mood) / max(len([h for h in health_logs if h.mood]), 1)
            context["health"] = {
                "avg_sleep": round(avg_sleep, 1),
                "avg_mood": round(avg_mood, 1),
                "days_logged": len(health_logs)
            }
    
    # Finances (week summary)
    if mode == "week_summary":
        this_month_start = today.replace(day=1)
        expenses = db.query(func.sum(Transaction.amount)).filter(
            and_(
                Transaction.type == TransactionType.EXPENSE,
                Transaction.date >= datetime.combine(this_month_start, datetime.min.time())
            )
        ).scalar() or 0
        
        context["finances"] = {
            "month_expenses": float(expenses)
        }
    
    return context
