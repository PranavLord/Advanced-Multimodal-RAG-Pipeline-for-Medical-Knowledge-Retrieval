from collections import defaultdict
from copy import deepcopy
from datetime import datetime


class ConversationEvidence:
    """
    Stores every retrieval event generated during
    a conversation session.

    Unlike ConversationMemory (messages),
    this class stores ONLY the retrieval evidence
    used to answer each user question.

    During report generation we rebuild:

    Document Grouper
    ↓
    Document Ranker
    ↓
    Evidence Mapper
    ↓
    Cross Document Reasoner

    using ALL unique retrieved chunks.
    """

    # --------------------------------------------------
    # In-Memory Storage
    # --------------------------------------------------

    _sessions = defaultdict(list)

    # --------------------------------------------------
    # Save Retrieval Event
    # --------------------------------------------------

    @classmethod
    def add_question(
        cls,
        session_id: str,
        question: str,
        retrieved_chunks: list
    ):
        """
        Save one retrieval event.

        Only retrieved chunks are stored.
        """

        cls._sessions[session_id].append(

            {

                "question": question,

                "timestamp": datetime.utcnow().isoformat(),

                "retrieved_chunks": deepcopy(
                    retrieved_chunks
                )

            }

        )

    # --------------------------------------------------
    # Return Every Retrieval Event
    # --------------------------------------------------

    @classmethod
    def get_session(
        cls,
        session_id: str
    ):

        return deepcopy(

            cls._sessions.get(

                session_id,

                []

            )

        )

    # --------------------------------------------------
    # Return UNIQUE Chunks Used
    # --------------------------------------------------

    @classmethod
    def get_chunks(
        cls,
        session_id: str
    ):

        unique_chunks = {}

        for event in cls._sessions.get(session_id, []):

            for chunk in event["retrieved_chunks"]:

                key = (

                    chunk.get("source"),

                    chunk.get("chunk_index")

                )

                previous = unique_chunks.get(key)

                if (

                    previous is None

                    or chunk.get("score", 0)
                    > previous.get("score", 0)

                ):

                    unique_chunks[key] = deepcopy(
                        chunk
                    )

        return list(

            unique_chunks.values()

        )

    # --------------------------------------------------
    # Number Of Questions
    # --------------------------------------------------

    @classmethod
    def question_count(
        cls,
        session_id: str
    ):

        return len(

            cls._sessions.get(

                session_id,

                []

            )

        )

    # --------------------------------------------------
    # Number Of UNIQUE Chunks
    # --------------------------------------------------

    @classmethod
    def chunk_count(
        cls,
        session_id: str
    ):

        return len(

            cls.get_chunks(
                session_id
            )

        )

    # --------------------------------------------------
    # Session Exists
    # --------------------------------------------------

    @classmethod
    def exists(
        cls,
        session_id: str
    ):

        return session_id in cls._sessions

    # --------------------------------------------------
    # Clear Session
    # --------------------------------------------------

    @classmethod
    def clear_session(
        cls,
        session_id: str
    ):

        cls._sessions.pop(

            session_id,

            None

        )

    # --------------------------------------------------
    # Clear Everything
    # --------------------------------------------------

    @classmethod
    def clear_all(cls):

        cls._sessions.clear()

    # --------------------------------------------------
    # Debug
    # --------------------------------------------------

    @classmethod
    def print(
        cls,
        session_id: str
    ):

        events = cls._sessions.get(

            session_id,

            []

        )

        print()

        print("=" * 60)
        print("CONVERSATION EVIDENCE")
        print("=" * 60)

        print(f"Questions Asked      : {len(events)}")

        print(
            f"Unique Evidence Chunks : {len(cls.get_chunks(session_id))}"
        )

        print()

        for index, event in enumerate(

            events,

            start=1

        ):

            print(f"Question {index}")

            print(f"   {event['question']}")

            print(
                f"   Retrieved Chunks : {len(event['retrieved_chunks'])}"
            )

            print()

        print("=" * 60)
        print()