"""Health check models."""

from datetime import datetime
from typing import Any, Dict

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str = Field(description="Health status", example="ok")
    timestamp: datetime = Field(description="Health check timestamp")
    version: str = Field(description="Application version", example="0.1.0")
    environment: str = Field(
        description="Application environment", example="development")
    details: Dict[str, Any] = Field(
        default_factory=dict, description="Additional health details"
    )
