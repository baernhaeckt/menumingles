"""Health check endpoints."""

from fastapi import APIRouter, HTTPException, Request, status

from app.core.exceptions import HealthCheckException
from app.core.logging import logger
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
async def health_check(http_request: Request) -> HealthResponse:
    """
    Get the health status of the application.

    Args:
        http_request: FastAPI request object for logging context

    Returns:
        HealthResponse: The health status response

    Raises:
        HTTPException: If the application is unhealthy
    """
    health_manager = HealthManager()

    # Log health check request
    logger.log_info("Health check requested", http_request)

    try:
        health_data = await health_manager.get_health_status()

        # Log successful health check
        logger.log_info(
            "Health check completed successfully",
            http_request,
            {"status": health_data.get("status", "unknown")}
        )

        return HealthResponse(**health_data)
    except HealthCheckException as e:
        # Log health check failure
        error_id = logger.log_error(
            e,
            http_request,
            {"endpoint": "health_check", "error_type": "HealthCheckException"}
        )

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Health check failed. Error ID: {error_id}. Contact support with this ID for detailed error information."
        )
    except Exception as e:
        # Log unexpected errors during health check
        error_id = logger.log_error(
            e,
            http_request,
            {"endpoint": "health_check", "error_type": "UnexpectedException"}
        )

        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Health check failed due to unexpected error. Error ID: {error_id}. Contact support with this ID for detailed error information."
        )
