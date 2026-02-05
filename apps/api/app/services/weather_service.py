"""Weather service using OpenWeatherMap API."""
from typing import Optional, Dict, Any
import httpx

from app.config import settings


class WeatherService:
    """Service for weather data."""
    
    BASE_URL = "https://api.openweathermap.org/data/2.5"
    
    def __init__(self):
        self.api_key = settings.weather_api_key
    
    async def get_current_weather(self, city: str) -> Dict[str, Any]:
        """Get current weather for a city."""
        if not self.api_key:
            return self._mock_weather(city)
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.BASE_URL}/weather",
                    params={
                        "q": city,
                        "appid": self.api_key,
                        "units": "metric",
                        "lang": "uk"  # Ukrainian language
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                return {
                    "city": data["name"],
                    "country": data["sys"]["country"],
                    "temperature": round(data["main"]["temp"]),
                    "feels_like": round(data["main"]["feels_like"]),
                    "humidity": data["main"]["humidity"],
                    "description": data["weather"][0]["description"],
                    "icon": data["weather"][0]["icon"],
                    "wind_speed": round(data["wind"]["speed"], 1),
                    "icon_url": f"https://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
                }
        except Exception as e:
            print(f"Weather API error: {e}")
            return self._mock_weather(city)
    
    async def get_forecast(self, city: str, days: int = 3) -> Dict[str, Any]:
        """Get weather forecast for a city."""
        if not self.api_key:
            return self._mock_forecast(city, days)
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.BASE_URL}/forecast",
                    params={
                        "q": city,
                        "appid": self.api_key,
                        "units": "metric",
                        "lang": "uk",
                        "cnt": days * 8  # 3-hour intervals
                    }
                )
                response.raise_for_status()
                data = response.json()
                
                # Group by day
                daily = {}
                for item in data["list"]:
                    date = item["dt_txt"].split(" ")[0]
                    if date not in daily:
                        daily[date] = {
                            "date": date,
                            "temps": [],
                            "descriptions": [],
                            "icons": []
                        }
                    daily[date]["temps"].append(item["main"]["temp"])
                    daily[date]["descriptions"].append(item["weather"][0]["description"])
                    daily[date]["icons"].append(item["weather"][0]["icon"])
                
                forecast = []
                for date, info in list(daily.items())[:days]:
                    forecast.append({
                        "date": date,
                        "temp_min": round(min(info["temps"])),
                        "temp_max": round(max(info["temps"])),
                        "description": max(set(info["descriptions"]), key=info["descriptions"].count),
                        "icon": max(set(info["icons"]), key=info["icons"].count)
                    })
                
                return {
                    "city": data["city"]["name"],
                    "country": data["city"]["country"],
                    "forecast": forecast
                }
        except Exception as e:
            print(f"Forecast API error: {e}")
            return self._mock_forecast(city, days)
    
    def _mock_weather(self, city: str) -> Dict[str, Any]:
        """Return mock weather data when API is unavailable."""
        return {
            "city": city,
            "country": "PL",
            "temperature": 5,
            "feels_like": 2,
            "humidity": 75,
            "description": "хмарно",
            "icon": "04d",
            "wind_speed": 3.5,
            "icon_url": "https://openweathermap.org/img/wn/04d@2x.png",
            "is_mock": True
        }
    
    def _mock_forecast(self, city: str, days: int) -> Dict[str, Any]:
        """Return mock forecast data."""
        from datetime import date, timedelta
        
        forecast = []
        for i in range(days):
            d = date.today() + timedelta(days=i)
            forecast.append({
                "date": d.isoformat(),
                "temp_min": 2 + i,
                "temp_max": 8 + i,
                "description": "хмарно",
                "icon": "04d"
            })
        
        return {
            "city": city,
            "country": "PL",
            "forecast": forecast,
            "is_mock": True
        }


# Dependency
def get_weather_service() -> WeatherService:
    """Get weather service instance."""
    return WeatherService()
