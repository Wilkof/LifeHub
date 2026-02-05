"""Finance models for income, expenses, budgets, and subscriptions."""
from datetime import datetime
from decimal import Decimal
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, Numeric, Boolean, JSON
from sqlalchemy.sql import func
import enum

from app.database import Base


class TransactionType(str, enum.Enum):
    """Transaction type enum."""
    INCOME = "income"
    EXPENSE = "expense"
    TRANSFER = "transfer"


class TransactionCategory(str, enum.Enum):
    """Transaction category enum."""
    # Income
    SALARY = "salary"
    FREELANCE = "freelance"
    INVESTMENTS = "investments"
    GIFT = "gift"
    OTHER_INCOME = "other_income"
    
    # Expenses
    RENT = "rent"
    UTILITIES = "utilities"
    GROCERIES = "groceries"
    TRANSPORT = "transport"
    HEALTH = "health"
    ENTERTAINMENT = "entertainment"
    EDUCATION = "education"
    SHOPPING = "shopping"
    SUBSCRIPTIONS = "subscriptions"
    FOOD_OUT = "food_out"
    TRAVEL = "travel"
    INSURANCE = "insurance"
    SAVINGS = "savings"
    OTHER_EXPENSE = "other_expense"


class Transaction(Base):
    """Financial transaction model."""
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Basic info
    amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(3), default="PLN")  # ISO currency code
    type = Column(Enum(TransactionType), nullable=False)
    category = Column(Enum(TransactionCategory), nullable=False)
    
    # Details
    description = Column(String(500), nullable=True)
    notes = Column(Text, nullable=True)
    
    # Date
    date = Column(DateTime(timezone=True), nullable=False)
    
    # Recurring
    is_recurring = Column(Boolean, default=False)
    recurring_day = Column(Integer, nullable=True)  # Day of month (1-31)
    
    # Tags for custom grouping
    tags = Column(JSON, default=list)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Budget(Base):
    """Monthly budget per category."""
    __tablename__ = "budgets"
    
    id = Column(Integer, primary_key=True, index=True)
    
    category = Column(Enum(TransactionCategory), nullable=False, unique=True)
    amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(3), default="PLN")
    
    # Alert threshold (percentage)
    alert_threshold = Column(Integer, default=80)  # Alert at 80% spent
    
    # Active
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Subscription(Base):
    """Recurring subscription tracking."""
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    
    name = Column(String(255), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(3), default="PLN")
    
    # Billing
    billing_day = Column(Integer, nullable=False)  # Day of month
    billing_cycle = Column(String(20), default="monthly")  # monthly, yearly
    
    # Category
    category = Column(String(100), nullable=True)
    
    # Reminders
    remind_days_before = Column(Integer, default=3)
    
    # Status
    is_active = Column(Boolean, default=True)
    next_billing_date = Column(DateTime(timezone=True), nullable=True)
    
    # Notes
    notes = Column(Text, nullable=True)
    url = Column(String(500), nullable=True)  # Link to manage subscription
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
