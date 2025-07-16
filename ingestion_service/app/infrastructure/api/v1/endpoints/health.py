"""
Health endpoint for the ingestion service.
Provides observability for Kubernetes probes.
"""
from fastapi import APIRouter, status
from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    service: str


router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    tags=["health"],
    summary="Health Check",
    description="Returns service health status for liveness and readiness probes"
)
async def health_check() -> HealthResponse:
    """
    Health check endpoint for Kubernetes probes.
    
    Returns:
        HealthResponse: Service status information
    """
    return HealthResponse(
        status="healthy",
        service="ingestion-service"
    )
