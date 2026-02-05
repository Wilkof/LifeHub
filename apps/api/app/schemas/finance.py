"""Finance schemas."""
from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, Field

from app.models.finance import TransactionType, TransactionCategory


# Transaction schemas
class TransactionBase(BaseModel):
    """Base transaction schema."""
    amount: Decimal = Field(..., gt=0)
    currency: str = "PLN"
    type: TransactionType
    category: TransactionCategory
    description: Optional[str] = None
    notes: Optional[str] = None
    date: datetime
    is_recurring: bool = False
    recurring_day: Optional[int] = Field(None, ge=1, le=31)
    tags: List[str] = []


class TransactionCreate(TransactionBase):
    """Schema for creating a transaction."""
    pass


class TransactionUpdate(BaseModel):
    """Schema for updating a transaction."""
    amount: Optional[Decimal] = Field(None, gt=0)
    currency: Optional[str] = None
    type: Optional[TransactionType] = None
    category: Optional[TransactionCategory] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    date: Optional[datetime] = None
    is_recurring: Optional[bool] = None
    recurring_day: Optional[int] = Field(None, ge=1, le=31)
    tags: Optional[List[str]] = None


class TransactionResponse(TransactionBase):
    """Transaction response schema."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Budget schemas
class BudgetBase(BaseModel):
    """Base budget schema."""
    category: TransactionCategory
    amount: Decimal = Field(..., gt=0)
    currency: str = "PLN"
    alert_threshold: int = Field(80, ge=0, le=100)
    is_active: bool = True


class BudgetCreate(BudgetBase):
    """Schema for creating a budget."""
    pass


class BudgetUpdate(BaseModel):
    """Schema for updating a budget."""
    amount: Optional[Decimal] = Field(None, gt=0)
    currency: Optional[str] = None
    alert_threshold: Optional[int] = Field(None, ge=0, le=100)
    is_active: Optional[bool] = None


class BudgetResponse(BudgetBase):
    """Budget response schema."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# Subscription schemas
class SubscriptionBase(BaseModel):
    """Base subscription schema."""
    name: str = Field(..., min_length=1, max_length=255)
    amount: Decimal = Field(..., gt=0)
    currency: str = "PLN"
    billing_day: int = Field(..., ge=1, le=31)
    billing_cycle: str = "monthly"
    category: Optional[str] = None
    remind_days_before: int = 3
    is_active: bool = True
    notes: Optional[str] = None
    url: Optional[str] = None


class SubscriptionCreate(SubscriptionBase):
    """Schema for creating a subscription."""
    pass


class SubscriptionUpdate(BaseModel):
    """Schema for updating a subscription."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    amount: Optional[Decimal] = Field(None, gt=0)
    currency: Optional[str] = None
    billing_day: Optional[int] = Field(None, ge=1, le=31)
    billing_cycle: Optional[str] = None
    category: Optional[str] = None
    remind_days_before: Optional[int] = None
    is_active: Optional[bool] = None
    notes: Optional[str] = None
    url: Optional[str] = None


class SubscriptionResponse(SubscriptionBase):
    """Subscription response schema."""
    id: int
    next_billing_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
