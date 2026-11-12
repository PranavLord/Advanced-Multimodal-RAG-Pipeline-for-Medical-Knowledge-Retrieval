from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from middlewares.exception_handlers import (
    catch_exception_middleware
)

from api.routes.upload import (
    router as upload_router
)

from api.routes.retrieval import (
    router as retrieval_router
)

from api.routes.chat import (
    router as chat_router
)

from api.routes.end_session import (
    router as end_session_router
)

# NEW
from api.routes.report import (
    router as report_router
)


app = FastAPI(
    title="Advanced Multimodal RAG Pipeline for Medical Knowledge Retrieval",
    description="API for AI Medical Assistant Chatbot",
    version="1.0.0"
)

# ==========================================================
# CORS Configuration
# ==========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# ==========================================================
# Global Exception Middleware
# ==========================================================

app.middleware("http")(
    catch_exception_middleware
)

# ==========================================================
# API Routes
# ==========================================================

app.include_router(
    upload_router,
    tags=["Upload"]
)

app.include_router(
    retrieval_router,
    tags=["Retrieval"]
)

app.include_router(
    chat_router,
    prefix="/chat",
    tags=["Chat"]
)

# NEW REPORT ROUTE
app.include_router(
    report_router,
    prefix="/report",
    tags=["Report"]
)

app.include_router(
    end_session_router,
    tags=["Session"]
)

# ==========================================================
# Health Check
# ==========================================================

@app.get("/")
async def root():

    return {
        "message": "Medical RAG Backend Running",
        "version": "1.0.0",
        "status": "healthy"
    }