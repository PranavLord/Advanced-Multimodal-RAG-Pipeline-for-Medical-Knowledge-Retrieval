from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    Request model for the Chat API.
    """

    question: str = Field(
        ...,
        min_length=1,
        description="User's medical question."
    )

    session_id: str = Field(
        ...,
        description="Unique session ID generated when the medical reports were uploaded."
    )

    provider: str | None = Field(
        default=None,
        description="LLM Provider (gemini or groq)."
    )