"""Discussion endpoints."""

import asyncio

from fastapi import APIRouter, HTTPException, Request, status

from app.core.logging import logger
from app.managers.discussion_manager import (
    BackgroundDiscussionManager,
    DiscussionManager,
    DiscussionStatus,
)
from app.models.discussion import (
    DiscussionRequest,
    DiscussionResponse,
    DiscussionStatusResponse,
    DiscussionTaskResponse,
)

router = APIRouter()


@router.post(
    "/discuss",
    response_model=DiscussionTaskResponse,
    summary="Start an async discussion",
    description="Start a discussion between people about a specific topic and return a task ID for polling",
    responses={
        202: {
            "description": "Discussion task started successfully",
            "content": {
                "application/json": {
                    "example": {
                        "task_id": "550e8400-e29b-41d4-a716-446655440000",
                        "status": "pending",
                        "message": "Discussion task started successfully"
                    }
                }
            }
        },
        409: {
            "description": "Another discussion is already running",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Another discussion is already running"
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
async def start_discussion(request: DiscussionRequest, http_request: Request) -> DiscussionTaskResponse:
    """
    Start an asynchronous discussion between people about a specific topic.

    Args:
        request: DiscussionRequest containing topic, people, and initiator
        http_request: FastAPI request object for logging context

    Returns:
        DiscussionTaskResponse: The task ID and status for polling

    Raises:
        HTTPException: If discussion cannot be started
    """
    # Log the start of the discussion
    logger.log_info(
        "Starting async discussion over the given menu",
        http_request,
        {
            "people_count": len(request.people),
            "chef_name": request.chef["persona"]["name"],
            "menu_count": len(request.menu)
        }
    )

    try:
        # Get the background discussion manager
        background_manager = BackgroundDiscussionManager()

        # Start the discussion task
        task_id = background_manager.start_discussion(request.model_dump())

        # Log successful task creation
        logger.log_info(
            "Discussion task created successfully",
            http_request,
            {
                "task_id": task_id,
                "people_count": len(request.people),
                "chef_name": request.chef["persona"]["name"],
                "menu_count": len(request.menu)
            }
        )

        return DiscussionTaskResponse(
            task_id=task_id,
            status="pending",
            message="Discussion task started successfully"
        )

    except RuntimeError as e:
        # Another discussion is already running
        logger.log_info(
            "Discussion start rejected - another discussion is running",
            http_request,
            {
                "people_count": len(request.people),
                "chef_name": request.chef["persona"]["name"],
                "menu_count": len(request.menu)
            }
        )

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Another discussion is already running"
        )

    except Exception as e:
        # Log the error with full context and stack trace
        error_id = logger.log_error(
            e,
            http_request,
            {
                "people_count": len(request.people),
                "chef_name": request.chef["persona"]["name"],
                "menu_count": len(request.menu),
                "endpoint": "start_discussion"
            }
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start discussion. Error ID: {error_id}. Contact support with this ID for detailed error information."
        )


@router.get(
    "/discuss/{task_id}/status",
    response_model=DiscussionStatusResponse,
    summary="Get discussion task status",
    description="Get the current status and results of a discussion task",
    responses={
        200: {
            "description": "Task status retrieved successfully",
            "content": {
                "application/json": {
                    "example": {
                        "task_id": "550e8400-e29b-41d4-a716-446655440000",
                        "status": "completed",
                        "created_at": "2023-12-01T12:00:00Z",
                        "started_at": "2023-12-01T12:00:05Z",
                        "completed_at": "2023-12-01T12:05:30Z",
                        "result": {
                            "monday": {
                                "name": "Swiss Rösti with Eggs",
                                "ingredients": ["potatoes", "eggs", "butter", "salt"]
                            }
                        },
                        "error": None
                    }
                }
            }
        },
        404: {
            "description": "Task not found",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Discussion task not found"
                    }
                }
            }
        }
    }
)
async def get_discussion_status(task_id: str, http_request: Request) -> DiscussionStatusResponse:
    """
    Get the status of a discussion task.

    Args:
        task_id: The unique identifier of the discussion task
        http_request: FastAPI request object for logging context

    Returns:
        DiscussionStatusResponse: The current status and results of the task

    Raises:
        HTTPException: If task is not found
    """
    # Log the status check request
    logger.log_info(
        "Checking discussion task status",
        http_request,
        {"task_id": task_id}
    )

    try:
        # Get the background discussion manager
        background_manager = BackgroundDiscussionManager()

        # Get the task status
        task = background_manager.get_task_status(task_id)

        if not task:
            logger.log_info(
                "Discussion task not found",
                http_request,
                {"task_id": task_id}
            )

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Discussion task not found"
            )

        # Convert task to response model
        response = DiscussionStatusResponse(
            task_id=task.task_id,
            status=task.status.value,
            created_at=task.created_at,
            started_at=task.started_at,
            completed_at=task.completed_at,
            result=task.result,
            error=task.error
        )

        # Log successful status retrieval
        logger.log_info(
            "Discussion task status retrieved successfully",
            http_request,
            {
                "task_id": task_id,
                "status": task.status.value
            }
        )

        return response

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log the error with full context and stack trace
        error_id = logger.log_error(
            e,
            http_request,
            {
                "task_id": task_id,
                "endpoint": "get_discussion_status"
            }
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get task status. Error ID: {error_id}. Contact support with this ID for detailed error information."
        )


# Legacy synchronous endpoint for backward compatibility
@router.post(
    "/discuss-sync",
    response_model=DiscussionResponse,
    summary="Start a synchronous discussion (legacy)",
    description="Start a discussion between people about a specific topic and wait for results (legacy endpoint)",
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
def discuss_menus_blocking(request: DiscussionRequest) -> DiscussionResponse:
    discussion_manager = DiscussionManager()

    results = discussion_manager.discuss_menus(
        people=request.people,
        chef=request.chef,
        consultants=request.consultants,
        menu=request.menu
    )

    return DiscussionResponse(results=results)


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
            result.dict()
        )

        return result

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
