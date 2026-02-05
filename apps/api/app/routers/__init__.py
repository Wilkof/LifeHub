"""API Routers."""
from app.routers.tasks import router as tasks_router
from app.routers.calendar import router as calendar_router
from app.routers.finances import router as finances_router
from app.routers.health import router as health_router
from app.routers.habits import router as habits_router
from app.routers.goals import router as goals_router
from app.routers.notes import router as notes_router
from app.routers.ai import router as ai_router
from app.routers.settings import router as settings_router
from app.routers.dashboard import router as dashboard_router
from app.routers.weather import router as weather_router
from app.routers.telegram import router as telegram_router

__all__ = [
    "tasks_router",
    "calendar_router",
    "finances_router",
    "health_router",
    "habits_router",
    "goals_router",
    "notes_router",
    "ai_router",
    "settings_router",
    "dashboard_router",
    "weather_router",
    "telegram_router",
]
