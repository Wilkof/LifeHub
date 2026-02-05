"""Weather API router."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.config import settings as app_settings
from app.services.weather_service import WeatherService, get_weather_service

router = APIRouter(prefix="/weather", tags=["Weather"])


@router.get("/current")
async def get_current_weather(
    city: str = None,
    weather_service: WeatherService = Depends(get_weather_service),
    db: Session = Depends(get_db)
):
    """Get current weather for a city."""
    from app.models.settings import UserSettings
    
    if not city:
        # Get from user settings
        user_settings = db.query(UserSettings).first()
        city = user_settings.weather_city if user_settings else app_settings.default_city
    
    try:
        weather = await weather_service.get_current_weather(city)
        return weather
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch weather: {str(e)}")


@router.get("/forecast")
async def get_weather_forecast(
    city: str = None,
    days: int = 3,
    weather_service: WeatherService = Depends(get_weather_service),
    db: Session = Depends(get_db)
):
    """Get weather forecast for a city."""
    from app.models.settings import UserSettings
    
    if not city:
        user_settings = db.query(UserSettings).first()
        city = user_settings.weather_city if user_settings else app_settings.default_city
    
    try:
        forecast = await weather_service.get_forecast(city, days)
        return forecast
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch forecast: {str(e)}")
