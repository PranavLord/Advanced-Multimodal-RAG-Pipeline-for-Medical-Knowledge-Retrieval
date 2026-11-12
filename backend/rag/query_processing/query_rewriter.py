from typing import Dict, List

from core.llm.llm_factory import (
    LLMFactory
)

from core.llm.prompting.prompts.query_rewrite_prompt import (
    QUERY_REWRITE_PROMPT
)


class QueryRewriter:
    """
    Uses an LLM to rewrite conversational follow-up
    questions into standalone questions before retrieval.
    """

    FOLLOWUP_PRONOUNS = {

        "it",
        "its",
        "they",
        "them",
        "their",
        "this",
        "that",
        "these",
        "those"

    }

    FOLLOWUP_PHRASES = [

        "what about",
        "how about",
        "and the",
        "and what",
        "and how",
        "what else",
        "tell me more",
        "more about",
        "continue",
        "next",
        "also",
        "any complications",
        "any side effects",
        "what symptoms",
        "what treatment",
        "how is it treated",
        "can it",
        "is it",
        "does it",
        "will it"

    ]

    @classmethod
    def needs_rewrite(
        cls,
        question: str
    ) -> bool:
        """
        Determines whether a question depends
        on previous conversation.
        """

        question = question.lower().strip()

        words = question.split()

        # -----------------------------
        # Pronoun Detection
        # -----------------------------

        if any(

            word.strip(".,?!")

            in cls.FOLLOWUP_PRONOUNS

            for word in words

        ):

            return True

        # -----------------------------
        # Conversational Phrase Detection
        # -----------------------------

        for phrase in cls.FOLLOWUP_PHRASES:

            if question.startswith(phrase):

                return True

        return False

    @staticmethod
    def rewrite(
        question: str,
        conversation_history: List[Dict],
        provider: str | None = None
    ) -> str:

        if not conversation_history:

            return question

        history = ""

        for message in conversation_history:

            role = message.get(
                "role",
                "user"
            ).capitalize()

            history += f"""
{role}:
{message.get("content", "")}

"""

        prompt = f"""
{QUERY_REWRITE_PROMPT}

========================================================
PREVIOUS CONVERSATION
========================================================

{history}

========================================================
CURRENT QUESTION
========================================================

{question}

========================================================
REWRITTEN QUESTION
========================================================
"""

        try:

            llm = LLMFactory.get_llm(

                provider=provider

            )

            rewritten_question = llm.generate(

                prompt

            ).strip()

            print("\n========== QUERY REWRITER ==========")
            print(f"Original Question : {question}")
            print(f"Rewritten Question: {rewritten_question}")
            print("====================================\n")

            if not rewritten_question:

                return question

            return rewritten_question

        except Exception as e:

            print("\n========== QUERY REWRITER ERROR ==========")
            print(str(e))
            print("==========================================\n")

            return question