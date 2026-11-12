from pydantic import BaseModel


class ChatResponse(BaseModel):
    """
    Response model for the Chat API.
    """

    answer: str

    provider: str