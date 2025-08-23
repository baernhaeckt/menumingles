"""Discussion endpoints."""

import asyncio

from fastapi import APIRouter, HTTPException, Request, status

from app.core.logging import logger
from app.managers.discussion_manager import DiscussionManager
from app.models.discussion import DiscussionRequest, DiscussionResponse

router = APIRouter()


@router.post(
    "/discuss",
    response_model=DiscussionResponse,
    summary="Start a discussion",
    description="Start a discussion between people about a specific topic and get consolidated results",
    responses={
        200: {
            "description": "Discussion completed successfully",
            "content": {
                "application/json": {
                    "example": {
                        "results": "Consolidated menu plan for the following week with dishes, ingredients, and remarks."
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
def discuss_menus_blocking(request: DiscussionRequest) -> dict:
    discussion_manager = DiscussionManager()

    return discussion_manager.discuss_menus(
        people=request.people,
        chef=request.chef,
        consultants=request.consultants,
        menu=request.menu
    )


async def discuss_topic(request: DiscussionRequest, http_request: Request) -> DiscussionResponse:
    """
    Start a discussion between people about a specific topic.

    Args:
        request: DiscussionRequest containing topic, people, and initiator
        http_request: FastAPI request object for logging context

    Returns:
        DiscussionResponse: The consolidated results from the discussion

    Raises:
        HTTPException: If discussion fails
    """
    # Log the start of the discussion
    logger.log_info(
        "Starting discussion over the given menu",
        http_request,
        {
            "people_count": len(request.people),
            "chef_name": request.chef["persona"]["name"],
            "menu_count": len(request.menu)
        }
    )

    try:
        # Call the discussion manager with the specified constraints
        result = await asyncio.to_thread(discuss_menus_blocking, request)

        # Log successful completion
        logger.log_info(
            "Discussion completed successfully",
            http_request,
            result
        )

        return DiscussionResponse(results=result)

    except Exception as e:
        # Log the error with full context and stack trace
        error_id = logger.log_error(
            e,
            http_request,
            {
                "people_count": len(request.people),
                "chef_name": request.chef["persona"]["name"],
                "menu_count": len(request.menu),
                "endpoint": "discuss_topic"
            }
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to complete discussion. Error ID: {error_id}. Contact support with this ID for detailed error information."
        )
