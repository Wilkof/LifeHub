"""LifeHub API - Main FastAPI Application."""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.database import init_db, engine, Base
from app.services.scheduler import scheduler_service


# Lifespan handler for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    # Startup
    print(f"Starting LifeHub API ({settings.app_env})")
    
    # NOTE: Do not auto-create tables here to avoid race conditions
    # with multiple workers in production. Run init_db once via
    # `python -c "from app.database import init_db; init_db()"`.
    
    # Start scheduler
    scheduler_service.start()
    scheduler_service.setup_notifications()
    print("Scheduler started")
    
    yield
    
    # Shutdown
    scheduler_service.stop()
    print("LifeHub API stopped")


# Create FastAPI app
app = FastAPI(
    title="LifeHub API",
    description="Personal life management dashboard API",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Authentication middleware
async def verify_token(request: Request):
    """Verify access token for protected routes."""
    # Skip auth for docs and health check
    if request.url.path in ["/api/docs", "/api/redoc", "/api/openapi.json", "/api/health", "/api/telegram/webhook"]:
        return
    
    # Check token
    token = request.headers.get("X-Access-Token") or request.headers.get("Authorization", "").replace("Bearer ", "")
    
    if settings.app_env != "development" and token != settings.app_access_token:
        raise HTTPException(status_code=401, detail="Invalid or missing access token")


# Health check
@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app": settings.app_name,
        "env": settings.app_env
    }


# Include routers
from app.routers import (
    tasks_router,
    calendar_router,
    finances_router,
    health_router,
    habits_router,
    goals_router,
    notes_router,
    ai_router,
    settings_router,
    dashboard_router,
    weather_router,
    telegram_router
)

# Mount all routers under /api prefix
app.include_router(dashboard_router, prefix="/api", dependencies=[Depends(verify_token)])
app.include_router(tasks_router, prefix="/api", dependencies=[Depends(verify_token)])
app.include_router(calendar_router, prefix="/api", dependencies=[Depends(verify_token)])
app.include_router(finances_router, prefix="/api", dependencies=[Depends(verify_token)])
app.include_router(health_router, prefix="/api", dependencies=[Depends(verify_token)])
app.include_router(habits_router, prefix="/api", dependencies=[Depends(verify_token)])
app.include_router(goals_router, prefix="/api", dependencies=[Depends(verify_token)])
app.include_router(notes_router, prefix="/api", dependencies=[Depends(verify_token)])
app.include_router(ai_router, prefix="/api", dependencies=[Depends(verify_token)])
app.include_router(settings_router, prefix="/api", dependencies=[Depends(verify_token)])
app.include_router(weather_router, prefix="/api", dependencies=[Depends(verify_token)])
app.include_router(telegram_router, prefix="/api")  # Telegram webhook needs to be public


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    print(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


# Root redirect
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "LifeHub API",
        "docs": "/api/docs",
        "health": "/api/health"
    }
