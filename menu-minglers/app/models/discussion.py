"""Discussion models."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class DiscussionRequest(BaseModel):
    """Request model for starting a discussion."""

    people: list[dict] = Field(...,
                               description="List of people participating in the discussion")
    chef: dict = Field(...,
                       description="The kitchen chef that is responsible for the menu")
    consultants: list[dict] = Field(...,
                                    description="The consultants that are helping the chef to make the menu")
    menu: list[dict] = Field(..., description="The menu to discuss")


class DiscussionResponse(BaseModel):
    """Response model for discussion results."""

    results: dict = Field(...,
                          description="The consolidated results from the discussion")


class DiscussionTaskResponse(BaseModel):
    """Response model for starting an async discussion task."""

    task_id: str = Field(...,
                         description="Unique identifier for the discussion task")
    status: str = Field(..., description="Current status of the task")
    message: str = Field(...,
                         description="Human-readable message about the task status")


class DiscussionStatusResponse(BaseModel):
    """Response model for checking discussion task status."""

    task_id: str = Field(...,
                         description="Unique identifier for the discussion task")
    status: str = Field(
        ..., description="Current status of the task (pending, running, completed, failed)")
    created_at: datetime = Field(..., description="When the task was created")
    started_at: Optional[datetime] = Field(
        None, description="When the task started running")
    completed_at: Optional[datetime] = Field(
        None, description="When the task completed")
    result: Optional[dict] = Field(
        None, description="Discussion results (only if completed)")
    error: Optional[str] = Field(
        None, description="Error message (only if failed)")
