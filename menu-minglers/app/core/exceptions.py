"""Custom exception classes."""

from fastapi import HTTPException, status


class MenuMinglersException(HTTPException):
    """Base exception for Menu Minglers application."""

    def __init__(
        self,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail: str = "Internal server error",
    ) -> None:
        """Initialize the exception."""
        super().__init__(status_code=status_code, detail=detail)


class HealthCheckException(MenuMinglersException):
    """Exception raised when health check fails."""

    def __init__(self, detail: str = "Health check failed") -> None:
        """Initialize the health check exception."""
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=detail
        )
