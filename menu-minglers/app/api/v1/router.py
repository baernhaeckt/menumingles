"""API v1 router."""

from fastapi import APIRouter

from app.api.v1.endpoints import discussion, health, people, websocket

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(health.router, tags=["health"])
api_router.include_router(people.router, tags=["people"])
api_router.include_router(discussion.router, tags=["discussion"])
api_router.include_router(websocket.router, tags=["websocket"])
