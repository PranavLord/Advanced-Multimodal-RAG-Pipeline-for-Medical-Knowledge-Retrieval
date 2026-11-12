import os
import uuid

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException
)

from utils.pipeline_tracker import (
    PipelineTracker
)

from rag.indexing.ingestion_pipeline import (
    IngestionPipeline
)

from core.llm.memory.session_document_stats import (
    SessionDocumentStats
)


router = APIRouter()


@router.post("/upload-report")
async def upload_report(
    file: UploadFile = File(...)
):

    # --------------------------------------------------
    # Generate Session ID
    # --------------------------------------------------

    session_id = str(
        uuid.uuid4()
    )

    # --------------------------------------------------
    # Create Session Folder
    # --------------------------------------------------

    session_folder = os.path.join(

        "data",

        "uploaded_reports",

        session_id

    )

    os.makedirs(

        session_folder,

        exist_ok=True

    )

    # --------------------------------------------------
    # Save Path
    # --------------------------------------------------

    save_path = os.path.join(

        session_folder,

        file.filename

    )

    try:

        # --------------------------------------------------
        # Save Uploaded File
        # --------------------------------------------------

        with open(
            save_path,
            "wb"
        ) as buffer:

            content = await file.read()

            buffer.write(content)

        # --------------------------------------------------
        # Initialize Pipeline
        # --------------------------------------------------

        tracker = PipelineTracker()

        pipeline = IngestionPipeline()

        # --------------------------------------------------
        # Process Document
        # --------------------------------------------------

        result = pipeline.ingest(

            pdf_path=save_path,

            tracker=tracker,

            session_id=session_id

        )

        print("\n========== SESSION DOCUMENT STATS ==========")
        SessionDocumentStats.print(session_id)
        print("============================================")
        # --------------------------------------------------
        # Store Upload Statistics
        # --------------------------------------------------

        SessionDocumentStats.save(

            session_id=session_id,

            uploaded_documents=1,

            total_chunks=result["chunks"],

            document_chunk_counts={

                result["source_file"]: result["chunks"]

            }

        )

        print("\n========== SESSION DOCUMENT STATS ==========")
        print(SessionDocumentStats.get(session_id))
        print("============================================\n")

        # --------------------------------------------------
        # Success Response
        # --------------------------------------------------

        return {

            "status": "success",

            "session_id": session_id,

            "pipeline_steps": tracker.get_steps(),

            "result": result

        }

    # ------------------------------------------------------
    # Expected Errors
    # ------------------------------------------------------

    except ValueError as e:

        raise HTTPException(

            status_code=400,

            detail=str(e)

        )

    # ------------------------------------------------------
    # Unexpected Errors
    # ------------------------------------------------------

    except Exception as e:

        print("\n========== BACKEND ERROR ==========")

        print(e)

        print("===================================\n")

        raise HTTPException(

            status_code=500,

            detail="An unexpected error occurred while processing the uploaded report."

        )