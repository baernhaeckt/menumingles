"""People models."""

from typing import Any, Dict, List

from pydantic import BaseModel, Field


class FamilyMember(BaseModel):
    """Model for a family member with persona data."""

    persona: Dict[str, Any] = Field(...,
                                    description="The persona data of the family member")


class FamilyMembersResponse(BaseModel):
    """Response model for family members generation."""

    family_members: List[FamilyMember] = Field(
        ..., description="List of generated family members")
    count: int = Field(..., description="Number of family members generated")
    context: str = Field(...,
                         description="The family context used for generation")
