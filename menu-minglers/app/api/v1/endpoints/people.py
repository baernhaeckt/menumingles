"""People endpoints."""

from typing import List

from fastapi import APIRouter, HTTPException, status, Request

from app.core.logging import logger
from app.managers.people_manager import PeopleManager
from app.models.people import (
    AgentPersonGenerationRequest,
    AgentPersonResponse,
    Persona,
    PersonGenerationRequest,
    PersonResponse,
)

router = APIRouter()


@router.post(
    "/generate-person",
    response_model=PersonResponse,
    summary="Generate a Person",
    description="Generate a person with specific attributes including preferences, intolerances, and goals",
    responses={
        200: {
            "description": "Person generated successfully",
            "content": {
                "application/json": {
                    "example": {
                        "person": {
                            "persona": {
                                "name": "Sarah Johnson",
                                "role": "A female person named Sarah Johnson who likes ['organic food', 'quick meals'].",
                                "personality": "Sarah is nurturing and organized, always thinking about nutrition and family well-being.",
                                "preferences": "Prefers organic ingredients, balanced macronutrients, and meals that can be prepared ahead of time.",
                                "additional_attributes": "Various other persona attributes from TinyTroupe"
                            }
                        },
                        "context": "HomeBite is a typical Swiss family household..."
                    }
                }
            }
        },
        400: {
            "description": "Invalid request parameters",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid parameters provided"
                    }
                }
            }
        }
    }
)
async def generate_person(request: PersonGenerationRequest, http_request: Request) -> PersonResponse:
    """
    Generate a person with specific attributes.

    Args:
        request: PersonGenerationRequest containing all required attributes
        http_request: FastAPI request object for logging context

    Returns:
        PersonResponse: The generated person with persona data

    Raises:
        HTTPException: If generation fails
    """
    people_manager = PeopleManager()

    # Log the start of person generation
    logger.log_info(
        "Starting person generation",
        http_request,
        {
            "gender": request.gender,
            "name": request.name,
            "preferences_count": len(request.preferences),
            "intolerances_count": len(request.intolerances),
            "goals_count": len(request.short_term_goals) + len(request.long_term_goals)
        }
    )

    try:
        # Generate person using the manager
        tiny_person = people_manager.generate_person(
            gender=request.gender,
            name=request.name,
            preferences=request.preferences,
            intolerances=request.intolerances,
            short_term_goals=request.short_term_goals,
            long_term_goals=request.long_term_goals
        )

        # Convert TinyPerson object to our Persona model
        persona_data = getattr(tiny_person, '_persona', {})
        person = Persona(persona=persona_data)

        # Log successful generation
        logger.log_info(
            "Person generated successfully",
            http_request,
            {"person_name": request.name}
        )

        return PersonResponse(
            person=person,
            context=people_manager.family_context.strip()
        )

    except Exception as e:
        # Log the error with full context and stack trace
        error_id = logger.log_error(
            e,
            http_request,
            {
                "gender": request.gender,
                "name": request.name,
                "preferences_count": len(request.preferences),
                "intolerances_count": len(request.intolerances),
                "endpoint": "generate_person"
            }
        )
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate person. Error ID: {error_id}. Contact support with this ID for detailed error information."
        )


@router.post(
    "/generate-agent-person",
    response_model=AgentPersonResponse,
    summary="Generate an Agent Person",
    description="Generate an agent person with specific expertise",
    responses={
        200: {
            "description": "Agent person generated successfully",
            "content": {
                "application/json": {
                    "example": {
                        "agent": {
                            "persona": {
                                "name": "Dr. Maria Schmidt",
                                "role": "A female person named Dr. Maria Schmidt that is an absolute expert in nutrition science.",
                                "personality": "Dr. Schmidt is passionate about nutrition science and sees herself as a guardian of quality and accuracy.",
                                "expertise": "Deep knowledge in nutrition science with a focus on evidence-based recommendations.",
                                "additional_attributes": "Various other persona attributes from TinyTroupe"
                            }
                        },
                        "context": "HomeBite Experts are a diverse circle of specialists..."
                    }
                }
            }
        },
        400: {
            "description": "Invalid request parameters",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Invalid parameters provided"
                    }
                }
            }
        }
    }
)
async def generate_agent_person(request: AgentPersonGenerationRequest, http_request: Request) -> AgentPersonResponse:
    """
    Generate an agent person with specific expertise.

    Args:
        request: AgentPersonGenerationRequest containing gender, name, and expertise
        http_request: FastAPI request object for logging context

    Returns:
        AgentPersonResponse: The generated agent person with persona data

    Raises:
        HTTPException: If generation fails
    """
    people_manager = PeopleManager()

    # Log the start of agent person generation
    logger.log_info(
        "Starting agent person generation",
        http_request,
        {
            "gender": request.gender,
            "name": request.name,
            "expertise": request.expertise
        }
    )

    try:
        # Generate agent person using the manager
        tiny_person = people_manager.generate_agent_person(
            gender=request.gender,
            name=request.name,
            expertise=request.expertise
        )

        # Convert TinyPerson object to our Persona model
        persona_data = getattr(tiny_person, '_persona', {})
        agent = Persona(persona=persona_data)

        # Log successful generation
        logger.log_info(
            "Agent person generated successfully",
            http_request,
            {"agent_name": request.name, "expertise": request.expertise}
        )

        return AgentPersonResponse(
            agent=agent,
            context=people_manager.agent_context.strip()
        )

    except Exception as e:
        # Log the error with full context and stack trace
        error_id = logger.log_error(
            e,
            http_request,
            {
                "gender": request.gender,
                "name": request.name,
                "expertise": request.expertise,
                "endpoint": "generate_agent_person"
            }
        )
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate agent person. Error ID: {error_id}. Contact support with this ID for detailed error information."
        )
