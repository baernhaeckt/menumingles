"""Health check manager."""

from typing import Any, Dict

from app.core.exceptions import HealthCheckException
from app.services.health_service import HealthService


class HealthManager:
    """Manager for health check operations."""

    def __init__(self) -> None:
        """Initialize the health manager."""
        self.health_service = HealthService()

    async def get_health_status(self) -> Dict[str, Any]:
        """
        Get the application health status.

        Returns:
            Dict[str, Any]: Health status response

        Raises:
            HealthCheckException: If health checks fail
        """
        try:
            # Perform health checks
            health_checks = await self.health_service.perform_health_checks()

            # Check if any health checks failed
            if not all(health_checks.values()):
                failed_checks = [
                    check for check, status in health_checks.items() if not status
                ]
                raise HealthCheckException(
                    f"Health checks failed for: {', '.join(failed_checks)}"
                )

                        # Get health status response
            health_response = await self.health_service.get_health_status()
            
            return health_response.model_dump()

        except Exception as e:
            # Log the error here in a real application
            raise HealthCheckException(f"Health check failed: {str(e)}")

    async def is_healthy(self) -> bool:
        """
        Check if the application is healthy.

        Returns:
            bool: True if healthy, False otherwise
        """
        try:
            await self.get_health_status()
            return True
        except HealthCheckException:
            return False
