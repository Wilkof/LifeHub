"""Telegram webhook router."""
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.config import settings

router = APIRouter(prefix="/telegram", tags=["Telegram"])


@router.post("/webhook")
async def telegram_webhook(request: Request, db: Session = Depends(get_db)):
    """Handle Telegram webhook updates."""
    from app.services.telegram_service import TelegramService
    
    try:
        data = await request.json()
        telegram_service = TelegramService(db)
        await telegram_service.handle_update(data)
        return {"ok": True}
    except Exception as e:
        # Log but don't fail - Telegram will retry
        print(f"Telegram webhook error: {e}")
        return {"ok": True}


@router.get("/setup")
async def setup_webhook():
    """Get webhook setup instructions."""
    return {
        "message": "Set webhook URL in Telegram BotFather",
        "webhook_url": f"{settings.frontend_url.replace('localhost:3000', 'your-render-api.onrender.com')}/api/telegram/webhook",
        "instructions": [
            "1. Open Telegram and find @BotFather",
            "2. Send /setwebhook",
            "3. Select your bot",
            "4. Send the webhook URL above"
        ]
    }


@router.post("/test-send")
async def test_send_message(message: str, db: Session = Depends(get_db)):
    """Test sending a message to registered chat."""
    from app.services.telegram_service import TelegramService
    
    telegram_service = TelegramService(db)
    success = await telegram_service.send_message(message)
    
    if success:
        return {"message": "Message sent successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to send message")
