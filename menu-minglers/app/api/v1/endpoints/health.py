"""Health check endpoints."""

from fastapi import APIRouter, HTTPException, status

from app.core.exceptions import HealthCheckException
from app.managers.health_manager import HealthManager
from app.models.health import HealthResponse

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Check the health status of the application",
    responses={
        200: {
            "description": "Application is healthy",
            "content": {
                "application/json": {
                    "example": {
                        "status": "ok",
                        "timestamp": "2023-12-01T12:00:00",
                        "version": "0.1.0",
                        "environment": "development",
                        "details": {
                            "database": "healthy",
                            "cache": "healthy",
                            "external_services": "healthy"
                        }
                    }
                }
            }
        },
        503: {
            "description": "Application is unhealthy",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Health check failed"
                    }
                }
            }
        }
    }
)
async def health_check() -> HealthResponse:
    """
    Get the health status of the application.

    Returns:
        HealthResponse: The health status response

    Raises:
        HTTPException: If the application is unhealthy
    """
    health_manager = HealthManager()

    try:
        health_data = await health_manager.get_health_status()
        return HealthResponse(**health_data)
    except HealthCheckException as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e.detail)
        )
