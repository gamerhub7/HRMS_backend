from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
from app.config import settings
from app.database import init_db, close_db
from app.routes import employees, attendance

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events.
    """
    # Startup
    logger.info("🚀 Starting HRMS Lite API...")
    await init_db()
    logger.info("✅ Application startup complete")
    
    yield
    
    # Shutdown
    logger.info("👋 Shutting down HRMS Lite API...")
    await close_db()
    logger.info("✅ Application shutdown complete")


# Create FastAPI application
app = FastAPI(
    title="HRMS Lite API",
    description="A lightweight Human Resource Management System for managing employees and attendance",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins_list(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register routers
app.include_router(employees.router)
app.include_router(attendance.router)


# Health check endpoint
@app.get("/", tags=["health"], summary="API Health Check")
async def root():
    """
    Health check endpoint.
    Returns API status and basic information.
    """
    return {
        "message": "HRMS Lite API is running",
        "version": "1.0.0",
        "database": "PostgreSQL (Supabase)",
        "status": "healthy",
        "docs": "/docs",
        "redoc": "/redoc"
    }


# Global exception handlers
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for unexpected errors.
    Logs the error and returns a user-friendly message.
    """
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An unexpected error occurred. Please try again later.",
            "error": str(exc) if settings.database_url.startswith("postgresql://postgres:") else "Internal server error"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
