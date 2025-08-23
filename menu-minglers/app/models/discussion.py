"""Discussion models."""

from typing import Any, Dict, List

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
