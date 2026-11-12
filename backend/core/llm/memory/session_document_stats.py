from copy import deepcopy


class SessionDocumentStats:
    """
    Stores upload statistics for every session.

    This is completely independent from retrieval.

    These values are created ONLY during document upload
    and never modified during the conversation.

    Example
    -------
    session_id
        uploaded_documents = 3
        total_chunks = 90

        {
            "report1.pdf": 25,
            "report2.pdf": 40,
            "report3.pdf": 25
        }
    """

    # --------------------------------------------------
    # In-Memory Storage
    # --------------------------------------------------

    _stats = {}

    # --------------------------------------------------
    # Save Session Statistics
    # --------------------------------------------------

    @classmethod
    def save(
        cls,
        session_id: str,
        uploaded_documents: int,
        total_chunks: int,
        document_chunk_counts: dict
    ):

        cls._stats[session_id] = {

            "uploaded_documents": uploaded_documents,

            "total_chunks": total_chunks,

            "document_chunk_counts": deepcopy(
                document_chunk_counts
            )

        }

    # --------------------------------------------------
    # Get Session Statistics
    # --------------------------------------------------

    @classmethod
    def get(
        cls,
        session_id: str
    ):

        return deepcopy(

            cls._stats.get(

                session_id,

                {

                    "uploaded_documents": 0,

                    "total_chunks": 0,

                    "document_chunk_counts": {}

                }

            )

        )

    # --------------------------------------------------
    # Get Uploaded Document Count
    # --------------------------------------------------

    @classmethod
    def uploaded_documents(
        cls,
        session_id: str
    ) -> int:

        return cls.get(
            session_id
        )["uploaded_documents"]

    # --------------------------------------------------
    # Get Total Chunk Count
    # --------------------------------------------------

    @classmethod
    def total_chunks(
        cls,
        session_id: str
    ) -> int:

        return cls.get(
            session_id
        )["total_chunks"]

    # --------------------------------------------------
    # Get Chunk Count Per Document
    # --------------------------------------------------

    @classmethod
    def document_chunks(
        cls,
        session_id: str
    ) -> dict:

        return deepcopy(

            cls.get(
                session_id
            )["document_chunk_counts"]

        )

    # --------------------------------------------------
    # Session Exists
    # --------------------------------------------------

    @classmethod
    def exists(
        cls,
        session_id: str
    ) -> bool:

        return session_id in cls._stats

    # --------------------------------------------------
    # Clear Session
    # --------------------------------------------------

    @classmethod
    def clear(
        cls,
        session_id: str
    ):

        cls._stats.pop(
            session_id,
            None
        )

    # --------------------------------------------------
    # Clear Everything
    # --------------------------------------------------

    @classmethod
    def clear_all(cls):

        cls._stats.clear()

    # --------------------------------------------------
    # Debug
    # --------------------------------------------------

    @classmethod
    def print(
        cls,
        session_id: str
    ):

        print("\n========== SESSION DOCUMENT STATS ==========")

        print(

            deepcopy(

                cls.get(session_id)

            )

        )

        print("============================================\n")