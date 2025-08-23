from pydantic import BaseModel


class ChatMessage(BaseModel):
    """Pydantic model for chat messages."""

    name: str
    message: str
