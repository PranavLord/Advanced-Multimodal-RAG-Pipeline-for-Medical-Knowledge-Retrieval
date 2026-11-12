from utils.pipeline_tracker import (
    PipelineTracker
)

from rag.retrieval.retrieval_pipeline import (
    RetrievalPipeline
)

tracker = PipelineTracker()

pipeline = RetrievalPipeline()

result = pipeline.retrieve(
    "What diagnosis was found?",
    tracker
)

print()

print(result)