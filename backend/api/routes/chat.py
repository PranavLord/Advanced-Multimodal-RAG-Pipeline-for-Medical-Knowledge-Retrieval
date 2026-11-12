from fastapi import APIRouter, HTTPException

from api.models.chat_request import (
    ChatRequest
)

from api.models.chat_response import (
    ChatResponse
)

from core.llm.generation_pipeline import (
    GenerationPipeline
)


router = APIRouter()

pipeline = GenerationPipeline()


@router.post(
    "",
    response_model=ChatResponse
)
async def chat(
    request: ChatRequest
):
    """
    Chat endpoint for querying the uploaded
    medical document.
    """

    try:

        result = pipeline.generate(

            question=request.question,

            session_id=request.session_id,

            provider=request.provider

        )

        return ChatResponse(

            answer=result.get("answer", ""),

            provider=result.get(
                "provider",
                request.provider or "gemini"
            )

        )

    # ------------------------------------------
    # Expected Errors
    # ------------------------------------------

    except ValueError as e:

        raise HTTPException(

            status_code=400,

            detail=str(e)

        )

    # ------------------------------------------
    # Unexpected Errors
    # ------------------------------------------

    except Exception as e:

        print("\n========== CHAT ERROR ==========")
        print(e)
        print("================================\n")

        raise HTTPException(

            status_code=500,

            detail="An unexpected error occurred while generating the response."

        )