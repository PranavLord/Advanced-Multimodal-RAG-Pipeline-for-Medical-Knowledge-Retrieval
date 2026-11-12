from typing import Dict, List

from core.llm.prompting.prompt_registry import (
    PromptRegistry
)


class PromptBuilder:

    @staticmethod
    def build(
        reasoning_context: Dict,
        question: str,
        conversation_history: List[Dict]
    ) -> str:

        # ==========================================================
        # Conversation History
        # ==========================================================

        if conversation_history:

            history = ""

            for message in conversation_history:

                history += (
                    f"{message['role'].capitalize()}: "
                    f"{message['content']}\n"
                )

        else:

            history = "No previous conversation."

        # ==========================================================
        # Multi-Document Clinical Context
        # ==========================================================

        clinical_context = f"""

====================================================
MULTI-DOCUMENT CLINICAL CONTEXT
====================================================

Total Documents Retrieved:
{reasoning_context['document_count']}

Highest Similarity Score:
{reasoning_context['highest_score']:.4f}

"""

        for document in reasoning_context["documents"]:

            clinical_context += f"""

----------------------------------------------------
Document Rank : {document['rank']}
----------------------------------------------------

Document Name:
{document['document']}

Importance:
{document['importance']}

Similarity Score:
{document['score']:.4f}

Average Score:
{document['average_score']:.4f}

Evidence Chunks:
{document['chunk_count']}

Relevant Evidence:

"""

            for evidence in document["evidence"]:

                clinical_context += f"""

• Chunk {evidence['chunk_index']}
  (Similarity: {evidence['score']:.4f})

{evidence['text']}

"""

        # ==========================================================
        # Select Prompt
        # ==========================================================

        selected_prompt = PromptRegistry.get_prompt(
            question
        )

        # ==========================================================
        # Final Prompt
        # ==========================================================

        prompt = f"""

{selected_prompt}

====================================================
CONVERSATION HISTORY
====================================================

{history}

{clinical_context}

====================================================
USER QUESTION
====================================================

{question}

====================================================
INSTRUCTIONS
====================================================

1. Treat the uploaded reports as the primary source.

2. Use evidence from ALL relevant documents whenever applicable.

3. If multiple reports discuss the same condition,
combine the information.

4. If reports disagree, clearly mention the difference.

5. Never invent findings.

6. Prefer higher-ranked documents when conflicts exist.

7. Clearly distinguish:

• Findings from uploaded reports

• General medical knowledge

====================================================
ANSWER
====================================================

"""

        return prompt.strip()