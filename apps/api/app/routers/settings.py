"""Settings API router."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.settings import UserSettings
from app.schemas.settings import SettingsUpdate, SettingsResponse

router = APIRouter(prefix="/settings", tags=["Settings"])


def get_or_create_settings(db: Session) -> UserSettings:
    """Get settings or create default if not exists."""
    settings = db.query(UserSettings).first()
    if not settings:
        settings = UserSettings(id=1)
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings


@router.get("", response_model=SettingsResponse)
def get_settings(db: Session = Depends(get_db)):
    """Get user settings."""
    return get_or_create_settings(db)


@router.put("", response_model=SettingsResponse)
def update_settings(data: SettingsUpdate, db: Session = Depends(get_db)):
    """Update user settings."""
    settings = get_or_create_settings(db)
    
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(settings, field, value)
    
    db.commit()
    db.refresh(settings)
    return settings


@router.post("/telegram/register")
def register_telegram(chat_id: str, db: Session = Depends(get_db)):
    """Register Telegram chat ID."""
    settings = get_or_create_settings(db)
    settings.telegram_chat_id = chat_id
    db.commit()
    return {"message": "Telegram registered", "chat_id": chat_id}
