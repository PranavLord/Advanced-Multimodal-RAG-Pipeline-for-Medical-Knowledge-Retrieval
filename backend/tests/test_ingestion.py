from utils.pipeline_tracker import (
    PipelineTracker
)

from rag.indexing.ingestion_pipeline import (
    IngestionPipeline
)

tracker = PipelineTracker()

pipeline = IngestionPipeline()

result = pipeline.ingest(
    "data/sample_reports/sample.pdf",
    tracker
)

print(result)