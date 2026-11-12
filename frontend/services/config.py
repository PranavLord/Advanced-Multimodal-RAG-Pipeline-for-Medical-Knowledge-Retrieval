"""
Frontend Configuration
"""

# ==========================================================
# FastAPI Backend
# ==========================================================

API_BASE_URL = "http://127.0.0.1:8000"

# ==========================================================
# API Endpoints
# ==========================================================

UPLOAD_ENDPOINT = f"{API_BASE_URL}/upload-report"

CHAT_ENDPOINT = f"{API_BASE_URL}/chat"

# NEW
REPORT_ENDPOINT = f"{API_BASE_URL}/report"

END_SESSION_ENDPOINT = f"{API_BASE_URL}/end-session"

HEALTH_ENDPOINT = f"{API_BASE_URL}/"