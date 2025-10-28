"""
EclipseLink AI - Main FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import logging
from contextlib import asynccontextmanager

from app.config import settings
from app.routers import auth, handoffs, patients, users, rewards, admin

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup and shutdown events for the application
    """
    # Startup
    logger.info("🚀 EclipseLink AI Backend starting up...")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")

    yield

    # Shutdown
    logger.info("👋 EclipseLink AI Backend shutting down...")


# Initialize FastAPI app
app = FastAPI(
    title="EclipseLink AI API",
    description="Voice-Enabled Clinical Handoff Platform with Update-Only Model™",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)

# CORS Middleware - Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security: Trusted Host Middleware (prevent host header attacks)
if not settings.DEBUG:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS
    )

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(handoffs.router, prefix="/api/handoffs", tags=["Handoffs"])
app.include_router(patients.router, prefix="/api/patients", tags=["Patients"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(rewards.router, prefix="/api/rewards", tags=["Rewards"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])


@app.get("/")
async def root():
    """
    Root endpoint - API information
    """
    return {
        "name": "EclipseLink AI API",
        "version": "0.1.0",
        "description": "Voice-Enabled Clinical Handoff Platform",
        "docs": "/api/docs",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for Docker and load balancers
    """
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "version": "0.1.0"
    }


@app.get("/api/health/detailed")
async def detailed_health():
    """
    Detailed health check including dependencies
    """
    from app.database import engine
    from sqlalchemy import text

    health_status = {
        "status": "healthy",
        "checks": {}
    }

    # Check database connection
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        health_status["checks"]["database"] = "connected"
    except Exception as e:
        health_status["checks"]["database"] = f"error: {str(e)}"
        health_status["status"] = "unhealthy"

    # Check AI services configuration
    if settings.OPENAI_API_KEY and settings.ANTHROPIC_API_KEY:
        health_status["checks"]["ai_services"] = "configured"
    else:
        health_status["checks"]["ai_services"] = "not_configured"
        health_status["status"] = "degraded"

    return health_status


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unhandled errors
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "type": "internal_error"
        }
    )
