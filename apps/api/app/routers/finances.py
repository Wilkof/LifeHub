"""Finances API router."""
from datetime import datetime, date
from typing import List, Optional
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, extract

from app.database import get_db
from app.models.finance import Transaction, Budget, Subscription, TransactionType, TransactionCategory
from app.schemas.finance import (
    TransactionCreate, TransactionUpdate, TransactionResponse,
    BudgetCreate, BudgetUpdate, BudgetResponse,
    SubscriptionCreate, SubscriptionUpdate, SubscriptionResponse
)

router = APIRouter(prefix="/finances", tags=["Finances"])


# ==================== Transactions ====================

@router.get("/transactions", response_model=List[TransactionResponse])
def get_transactions(
    type: Optional[TransactionType] = None,
    category: Optional[TransactionCategory] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    min_amount: Optional[Decimal] = None,
    max_amount: Optional[Decimal] = None,
    limit: int = Query(100, le=500),
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """Get transactions with filters."""
    query = db.query(Transaction)
    
    if type:
        query = query.filter(Transaction.type == type)
    if category:
        query = query.filter(Transaction.category == category)
    if date_from:
        query = query.filter(Transaction.date >= datetime.combine(date_from, datetime.min.time()))
    if date_to:
        query = query.filter(Transaction.date <= datetime.combine(date_to, datetime.max.time()))
    if min_amount:
        query = query.filter(Transaction.amount >= min_amount)
    if max_amount:
        query = query.filter(Transaction.amount <= max_amount)
    
    query = query.order_by(Transaction.date.desc())
    
    return query.offset(offset).limit(limit).all()


@router.get("/transactions/summary")
def get_transactions_summary(
    month: Optional[int] = None,
    year: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get monthly summary of income and expenses."""
    if not month:
        month = date.today().month
    if not year:
        year = date.today().year
    
    # Income
    income = db.query(func.sum(Transaction.amount)).filter(
        and_(
            Transaction.type == TransactionType.INCOME,
            extract('month', Transaction.date) == month,
            extract('year', Transaction.date) == year
        )
    ).scalar() or Decimal(0)
    
    # Expenses
    expenses = db.query(func.sum(Transaction.amount)).filter(
        and_(
            Transaction.type == TransactionType.EXPENSE,
            extract('month', Transaction.date) == month,
            extract('year', Transaction.date) == year
        )
    ).scalar() or Decimal(0)
    
    # By category
    category_totals = db.query(
        Transaction.category,
        func.sum(Transaction.amount).label('total')
    ).filter(
        and_(
            Transaction.type == TransactionType.EXPENSE,
            extract('month', Transaction.date) == month,
            extract('year', Transaction.date) == year
        )
    ).group_by(Transaction.category).all()
    
    return {
        "month": month,
        "year": year,
        "income": float(income),
        "expenses": float(expenses),
        "balance": float(income - expenses),
        "by_category": {str(cat): float(total) for cat, total in category_totals}
    }


@router.post("/transactions", response_model=TransactionResponse)
def create_transaction(data: TransactionCreate, db: Session = Depends(get_db)):
    """Create a new transaction."""
    transaction = Transaction(**data.model_dump())
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return transaction


@router.put("/transactions/{id}", response_model=TransactionResponse)
def update_transaction(id: int, data: TransactionUpdate, db: Session = Depends(get_db)):
    """Update a transaction."""
    transaction = db.query(Transaction).filter(Transaction.id == id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(transaction, field, value)
    
    db.commit()
    db.refresh(transaction)
    return transaction


@router.delete("/transactions/{id}")
def delete_transaction(id: int, db: Session = Depends(get_db)):
    """Delete a transaction."""
    transaction = db.query(Transaction).filter(Transaction.id == id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    db.delete(transaction)
    db.commit()
    return {"message": "Transaction deleted"}


# ==================== Budgets ====================

@router.get("/budgets", response_model=List[BudgetResponse])
def get_budgets(db: Session = Depends(get_db)):
    """Get all budgets."""
    return db.query(Budget).filter(Budget.is_active == True).all()


@router.get("/budgets/status")
def get_budget_status(
    month: Optional[int] = None,
    year: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get budget status with spending."""
    if not month:
        month = date.today().month
    if not year:
        year = date.today().year
    
    budgets = db.query(Budget).filter(Budget.is_active == True).all()
    
    result = []
    for budget in budgets:
        spent = db.query(func.sum(Transaction.amount)).filter(
            and_(
                Transaction.type == TransactionType.EXPENSE,
                Transaction.category == budget.category,
                extract('month', Transaction.date) == month,
                extract('year', Transaction.date) == year
            )
        ).scalar() or Decimal(0)
        
        percentage = (float(spent) / float(budget.amount) * 100) if budget.amount > 0 else 0
        
        result.append({
            "id": budget.id,
            "category": str(budget.category.value),
            "budget": float(budget.amount),
            "spent": float(spent),
            "remaining": float(budget.amount - spent),
            "percentage": round(percentage, 1),
            "is_over": percentage > 100,
            "alert": percentage >= budget.alert_threshold
        })
    
    return result


@router.post("/budgets", response_model=BudgetResponse)
def create_budget(data: BudgetCreate, db: Session = Depends(get_db)):
    """Create a new budget."""
    # Check if budget for this category exists
    existing = db.query(Budget).filter(Budget.category == data.category).first()
    if existing:
        raise HTTPException(status_code=400, detail="Budget for this category already exists")
    
    budget = Budget(**data.model_dump())
    db.add(budget)
    db.commit()
    db.refresh(budget)
    return budget


@router.put("/budgets/{id}", response_model=BudgetResponse)
def update_budget(id: int, data: BudgetUpdate, db: Session = Depends(get_db)):
    """Update a budget."""
    budget = db.query(Budget).filter(Budget.id == id).first()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(budget, field, value)
    
    db.commit()
    db.refresh(budget)
    return budget


@router.delete("/budgets/{id}")
def delete_budget(id: int, db: Session = Depends(get_db)):
    """Delete a budget."""
    budget = db.query(Budget).filter(Budget.id == id).first()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    
    db.delete(budget)
    db.commit()
    return {"message": "Budget deleted"}


# ==================== Subscriptions ====================

@router.get("/subscriptions", response_model=List[SubscriptionResponse])
def get_subscriptions(
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """Get all subscriptions."""
    query = db.query(Subscription)
    if active_only:
        query = query.filter(Subscription.is_active == True)
    return query.order_by(Subscription.billing_day.asc()).all()


@router.get("/subscriptions/upcoming")
def get_upcoming_subscriptions(
    days: int = Query(7, ge=1, le=30),
    db: Session = Depends(get_db)
):
    """Get subscriptions billing in the next N days."""
    today = date.today()
    subscriptions = db.query(Subscription).filter(Subscription.is_active == True).all()
    
    upcoming = []
    for sub in subscriptions:
        # Calculate next billing date
        billing_date = today.replace(day=min(sub.billing_day, 28))
        if billing_date < today:
            # Next month
            if today.month == 12:
                billing_date = billing_date.replace(year=today.year + 1, month=1)
            else:
                billing_date = billing_date.replace(month=today.month + 1)
        
        days_until = (billing_date - today).days
        if days_until <= days:
            upcoming.append({
                "id": sub.id,
                "name": sub.name,
                "amount": float(sub.amount),
                "currency": sub.currency,
                "billing_date": billing_date.isoformat(),
                "days_until": days_until
            })
    
    return sorted(upcoming, key=lambda x: x["days_until"])


@router.post("/subscriptions", response_model=SubscriptionResponse)
def create_subscription(data: SubscriptionCreate, db: Session = Depends(get_db)):
    """Create a new subscription."""
    subscription = Subscription(**data.model_dump())
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    return subscription


@router.put("/subscriptions/{id}", response_model=SubscriptionResponse)
def update_subscription(id: int, data: SubscriptionUpdate, db: Session = Depends(get_db)):
    """Update a subscription."""
    subscription = db.query(Subscription).filter(Subscription.id == id).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(subscription, field, value)
    
    db.commit()
    db.refresh(subscription)
    return subscription


@router.delete("/subscriptions/{id}")
def delete_subscription(id: int, db: Session = Depends(get_db)):
    """Delete a subscription."""
    subscription = db.query(Subscription).filter(Subscription.id == id).first()
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    db.delete(subscription)
    db.commit()
    return {"message": "Subscription deleted"}
