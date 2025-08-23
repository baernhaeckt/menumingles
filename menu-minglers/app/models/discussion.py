"""Discussion models."""

from typing import Any, Dict, List

from pydantic import BaseModel, Field


class DiscussionRequest(BaseModel):
    """Request model for starting a discussion."""

    topic: str = Field(..., description="The topic to discuss")
    people: List[Dict[str, Any]
                 ] = Field(..., description="List of people participating in the discussion")
    initiator: Dict[str, Any] = Field(...,
                                      description="The initiator of the discussion")


class DiscussionResponse(BaseModel):
    """Response model for discussion results."""

    results: str = Field(...,
                         description="The consolidated results from the discussion")
