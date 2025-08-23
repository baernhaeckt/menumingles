"""People models."""

from typing import Any, Dict, List

from pydantic import BaseModel, Field


class Persona(BaseModel):
    """Model for persona data."""

    persona: Dict[str, Any] = Field(..., description="The persona data")


class PersonGenerationRequest(BaseModel):
    """Request model for generating a person."""

    gender: str = Field(..., description="Gender of the person")
    name: str = Field(..., description="Name of the person")
    preferences: List[str] = Field(..., description="List of food preferences")
    intolerances: List[str] = Field(...,
                                    description="List of food intolerances")
    short_term_goals: List[str] = Field(...,
                                        description="List of short-term goals")
    long_term_goals: List[str] = Field(...,
                                       description="List of long-term goals")


class AgentPersonGenerationRequest(BaseModel):
    """Request model for generating an agent person."""

    gender: str = Field(..., description="Gender of the agent")
    name: str = Field(..., description="Name of the agent")
    expertise: str = Field(..., description="Area of expertise")


class PersonResponse(BaseModel):
    """Response model for person generation."""

    person: Persona = Field(..., description="The generated person")
    context: str = Field(..., description="The context used for generation")


class AgentPersonResponse(BaseModel):
    """Response model for agent person generation."""

    agent: Persona = Field(..., description="The generated agent person")
    context: str = Field(..., description="The context used for generation")


# Legacy models for backward compatibility
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
