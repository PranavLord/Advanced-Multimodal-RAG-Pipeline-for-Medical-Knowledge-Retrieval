from fastapi import (
    APIRouter
)

from pydantic import (
    BaseModel
)

from utils.pipeline_tracker import (
    PipelineTracker
)

from rag.retrieval.retrieval_pipeline import (
    RetrievalPipeline
)


router = APIRouter()


class QueryRequest(
    BaseModel
):

    question: str


@router.post("/retrieve")
async def retrieve_context(
    request: QueryRequest
):

    tracker = PipelineTracker()

    pipeline = RetrievalPipeline()

    result = pipeline.retrieve(
        request.question,
        tracker
    )

    return {

        "status": "success",

        "pipeline_steps":
            tracker.get_steps(),

        "result":
            result
    }