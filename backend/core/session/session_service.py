import shutil
from pathlib import Path

from core.vectorstore_manager.pinecone_manager import (
    PineconeManager
)

from core.llm.memory.conversation_memory import (
    ConversationMemory
)


class SessionService:
    """
    Handles cleanup of an upload session.
    """

    def __init__(self):

        self.pinecone = PineconeManager()

        self.upload_directory = Path(
            "data/uploaded_reports"
        )

    # --------------------------------------------------
    # End Session
    # --------------------------------------------------

    def delete_session(
        self,
        session_id: str
    ):

        # ----------------------------------------------
        # Delete Pinecone Vectors
        # ----------------------------------------------

        vector_result = self.delete_vectors(
            session_id
        )

        # ----------------------------------------------
        # Delete Uploaded Reports
        # ----------------------------------------------

        deleted_files = self.delete_uploaded_reports(
            session_id
        )

        # ----------------------------------------------
        # Clear Conversation Memory
        # ----------------------------------------------

        ConversationMemory.clear(
            session_id
        )

        return {

            "success": True,

            "session_id": session_id,

            "deleted_vectors": vector_result,

            "deleted_files": deleted_files

        }

    # --------------------------------------------------
    # Delete Pinecone Vectors
    # --------------------------------------------------

    def delete_vectors(
        self,
        session_id: str
    ):

        return self.pinecone.delete_by_session(
            session_id
        )

    # --------------------------------------------------
    # Delete Uploaded Reports
    # --------------------------------------------------

    def delete_uploaded_reports(
        self,
        session_id: str
    ):

        session_folder = self.upload_directory / session_id

        if not session_folder.exists():

            return 0

        try:

            file_count = len(
                list(session_folder.glob("*"))
            )

            shutil.rmtree(
                session_folder
            )

            return file_count

        except Exception as e:

            print(
                f"Unable to delete session folder {session_folder}: {e}"
            )

            return 0