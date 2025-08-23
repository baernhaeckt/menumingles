"""Discussion endpoints."""

from fastapi import APIRouter, HTTPException, status

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
async def discuss_topic(request: DiscussionRequest) -> DiscussionResponse:
    """
    Start a discussion between people about a specific topic.

    Args:
        request: DiscussionRequest containing topic, people, and initiator

    Returns:
        DiscussionResponse: The consolidated results from the discussion

    Raises:
        HTTPException: If discussion fails
    """
    discussion_manager = DiscussionManager()

    try:
        # Call the discussion manager with the specified constraints
        results = discussion_manager.discuss_topic(
            world_name="Group Chat",
            situation="A group chat that discuss and modify the dishes / menus of the next week",
            topic=request.topic,
            people=request.people,
            initiator=request.initiator,
            extraction_objective="Consolidate all opinions and create a menu plan for the following week, with the dish names and ingredients for each day. Add remarks to each menu if applicable, if there should be something concerned.",
            turns=None
        )

        return DiscussionResponse(results=results)

    except Exception as e:
        e.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to complete discussion: {str(e)}"
        )
