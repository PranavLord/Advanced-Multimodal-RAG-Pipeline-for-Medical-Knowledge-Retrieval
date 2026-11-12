from typing import Dict, List

from core.llm.memory.conversation_evidence import ConversationEvidence


class ConversationMemory:
    """
    Stores conversation history for each upload session.

    Data is stored in memory and removed when the
    session ends.
    """

    # --------------------------------------------------
    # In-Memory Storage
    # --------------------------------------------------

    _memory: Dict[str, List[Dict]] = {}

    # --------------------------------------------------
    # Add Conversation
    # --------------------------------------------------

    @classmethod
    def add_message(
        cls,
        session_id: str,
        role: str,
        content: str
    ):

        if session_id not in cls._memory:

            cls._memory[session_id] = []

        cls._memory[session_id].append(

            {

                "role": role,

                "content": content

            }

        )
        print("\n========== MEMORY ==========")
        print(cls._memory)
        print("============================\n")

    # --------------------------------------------------
    # Get Conversation
    # --------------------------------------------------

    @classmethod
    def get_history(
        cls,
        session_id: str
    ) -> List[Dict]:

        return cls._memory.get(
            session_id,
            []
        )

    # --------------------------------------------------
    # Clear Conversation
    # --------------------------------------------------

    @classmethod
    def clear(
        cls,
        session_id: str
    ):

        cls._memory.pop(
            session_id,
            None
        )

        ConversationEvidence.clear_session(
            session_id
        )

    # --------------------------------------------------
    # Check Session Exists
    # --------------------------------------------------

    @classmethod
    def exists(
        cls,
        session_id: str
    ) -> bool:

        return session_id in cls._memory

    # --------------------------------------------------
    # Number of Messages
    # --------------------------------------------------

    @classmethod
    def message_count(
        cls,
        session_id: str
    ) -> int:

        return len(

            cls.get_history(
                session_id
            )

        )

    # --------------------------------------------------
    # Get All Sessions
    # --------------------------------------------------

    @classmethod
    def active_sessions(
        cls
    ) -> List[str]:

        return list(

            cls._memory.keys()

        )