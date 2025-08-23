from pydantic import BaseModel


class ChatMessage(BaseModel):
    """Pydantic model for chat messages."""

    type: str = "chat"
    name: str
    message: str
