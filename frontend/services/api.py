import requests

from services.config import (
    UPLOAD_ENDPOINT,
    CHAT_ENDPOINT,
    REPORT_ENDPOINT,
    END_SESSION_ENDPOINT
)


class BackendAPI:
    """
    Handles all communication with the FastAPI backend.
    """

    # ==========================================================
    # Upload Reports
    # ==========================================================

    @staticmethod
    def upload_reports(files):

        payload = []

        for file in files:

            payload.append(
                (
                    "file",
                    (
                        file.name,
                        file,
                        "application/pdf"
                    )
                )
            )

        response = requests.post(
            UPLOAD_ENDPOINT,
            files=payload,
            timeout=300
        )

        response.raise_for_status()

        return response.json()

    # ==========================================================
    # Chat
    # ==========================================================

    @staticmethod
    def chat(
        question: str,
        session_id: str,
        provider: str | None = None
    ):

        payload = {

            "question": question,

            "session_id": session_id,

            "provider": provider

        }

        response = requests.post(

            CHAT_ENDPOINT,

            json=payload,

            timeout=300

        )

        response.raise_for_status()

        return response.json()

    # ==========================================================
    # Generate Report
    # ==========================================================

    @staticmethod
    def generate_report(
        session_id: str,
        provider: str | None = None
    ):

        payload = {

            "question": "Generate Report",

            "session_id": session_id,

            "provider": provider

        }

        response = requests.post(

            REPORT_ENDPOINT,

            json=payload,

            timeout=600

        )

        response.raise_for_status()

        return response.json()

    # ==========================================================
    # End Session
    # ==========================================================

    @staticmethod
    def end_session(session_id: str):

        response = requests.post(

            END_SESSION_ENDPOINT,

            json={

                "session_id": session_id

            },

            timeout=300

        )

        response.raise_for_status()

        return response.json()