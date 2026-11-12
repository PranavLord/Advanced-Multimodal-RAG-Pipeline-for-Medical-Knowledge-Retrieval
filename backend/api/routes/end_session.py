from fastapi import (
    APIRouter,
    HTTPException
)

from pydantic import BaseModel

from core.session.session_service import (
    SessionService
)


router = APIRouter()

session_service = SessionService()


# --------------------------------------------------
# Request Model
# --------------------------------------------------

class EndSessionRequest(BaseModel):

    session_id: str


# --------------------------------------------------
# End Session Endpoint
# --------------------------------------------------

@router.post("/end-session")
async def end_session(
    request: EndSessionRequest
):
    """
    Ends a user session by deleting:

    • All Pinecone vectors
    • Uploaded PDF files
    """

    try:

        result = session_service.delete_session(

            request.session_id

        )

        return {

            "status": "success",

            "message": "Session ended successfully.",

            "result": result

        }

    except Exception as e:

        print("\n========== END SESSION ERROR ==========")

        print(e)

        print("=======================================\n")

        raise HTTPException(

            status_code=500,

            detail="Unable to end the current session."

        )