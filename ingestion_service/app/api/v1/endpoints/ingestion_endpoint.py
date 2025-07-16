# Endpoint de healthcheck para el servicio de ingesta
from fastapi import APIRouter

router = APIRouter()

@router.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}
