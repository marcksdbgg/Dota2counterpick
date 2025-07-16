"""
FastAPI server configuration for the ingestion service.
This configures the FastAPI instance with proper middleware and routing.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.infrastructure.api.v1.endpoints.health import router as health_router
from app.core.config import settings


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application.
    
    Returns:
        Configured FastAPI application instance
    """
    app = FastAPI(
        title="Ingestion Service",
        description="Dota 2 match data ingestion service",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["GET"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(health_router, prefix="/api/v1")
    
    return app
