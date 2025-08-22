"""People endpoints."""

from typing import List

from fastapi import APIRouter, HTTPException, Query, status

from app.managers.people_manager import PeopleManager
from app.models.people import FamilyMember, FamilyMembersResponse

router = APIRouter()


@router.get(
    "/family-members",
    response_model=FamilyMembersResponse,
    summary="Generate Family Members",
    description="Generate a specified number of family members with unique personalities and preferences",
    responses={
        200: {
            "description": "Family members generated successfully",
            "content": {
                "application/json": {
                    "example": {
                        "family_members": [
                            {
                                "persona": {
                                    "name": "Sarah Johnson",
                                    "role": "A mother who cares deeply about healthy, balanced meals.",
                                    "personality": "Sarah is nurturing and organized, always thinking about nutrition and family well-being.",
                                    "preferences": "Prefers organic ingredients, balanced macronutrients, and meals that can be prepared ahead of time.",
                                    "additional_attributes": "Various other persona attributes from TinyTroupe"
                                }
                            }
                        ],
                        "count": 1,
                        "context": "HomeBite is a close-knit family kitchen collective..."
                    }
                }
            }
        },
        400: {
            "description": "Invalid number of family members requested",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Number of family members must be between 1 and 20"
                    }
                }
            }
        }
    }
)
async def generate_family_members(
    count: int = Query(
        default=5,
        ge=1,
        le=20,
        description="Number of family members to generate (1-20)"
    )
) -> FamilyMembersResponse:
    """
    Generate a specified number of family members with unique personalities and preferences.

    Args:
        count: Number of family members to generate (1-20)

    Returns:
        FamilyMembersResponse: The generated family members

    Raises:
        HTTPException: If the count is invalid
    """

    people_manager = PeopleManager()

    try:
        # Generate family members using the manager
        tiny_persons = people_manager.get_family_members(count)

        # Convert TinyPerson objects to our FamilyMember model using _persona attribute
        family_members = []
        for person in tiny_persons:
            # Access the _persona attribute which contains the JSON/object data
            persona_data = getattr(person, '_persona', {})
            family_member = FamilyMember(persona=persona_data)
            family_members.append(family_member)

        return FamilyMembersResponse(
            family_members=family_members,
            count=count,
            context=people_manager.family_context.strip()
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate family members: {str(e)}"
        )
