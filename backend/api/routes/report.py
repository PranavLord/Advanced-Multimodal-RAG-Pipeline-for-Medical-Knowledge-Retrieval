from fastapi import APIRouter, HTTPException

from api.models.chat_request import (
    ChatRequest
)

from services.report_service import (
    ReportService
)

router = APIRouter()

report_service = ReportService()


@router.post("")
async def generate_report(
    request: ChatRequest
):
    """
    Generate a structured medical consultation report
    using the uploaded reports and the conversation history.
    """

    try:

        result = report_service.generate_report(

            session_id=request.session_id,

            provider=request.provider

        )

        print("\n========== REPORT ROUTE RESPONSE ==========")
        print(result.keys())
        print("stats =", result.get("stats"))
        print("reasoning keys =", list(result.get("reasoning", {}).keys()))
        print("========================================\n")

        return {

            "report": result["report"],

            "provider": result["provider"],

            "stats": result.get("stats", {}),

            "reasoning": result.get("reasoning", {})

        }

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

        print("\n========== REPORT ERROR ==========")
        print(e)
        print("==================================\n")

        raise HTTPException(

            status_code=500,

            detail="An unexpected error occurred while generating the report."

        )
