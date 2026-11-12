import json
import re

from core.llm.prompting.prompts.report_prompt import REPORT_PROMPT
from core.llm.llm_manager import LLMManager

from core.llm.memory.conversation_memory import (
    ConversationMemory
)

from core.llm.memory.conversation_evidence import (
    ConversationEvidence
)

from core.llm.memory.session_document_stats import (
    SessionDocumentStats
)

from rag.document_processing.document_grouper import (
    DocumentGrouper
)

from rag.document_processing.document_ranker import (
    DocumentRanker
)

from rag.document_processing.evidence_mapper import (
    EvidenceMapper
)

from rag.reasoning.cross_document_reasoner import (
    CrossDocumentReasoner
)


class ReportService:
    """
    Generates the final consultation report using
    ONLY the evidence that was actually used
    throughout the conversation.
    """

    def generate_report(
        self,
        session_id: str,
        provider: str | None = None
    ):

        # --------------------------------------------------
        # Load Conversation History
        # --------------------------------------------------

        conversation_history = ConversationMemory.get_history(
            session_id
        )

        history = ""

        if conversation_history:

            for message in conversation_history:

                history += (
                    f"{message['role'].capitalize()}: "
                    f"{message['content']}\n"
                )

        else:

            history = "No conversation."

        # --------------------------------------------------
        # Load Conversation Evidence
        # --------------------------------------------------

        conversation_chunks = ConversationEvidence.get_chunks(
            session_id
        )

        grouped_documents = DocumentGrouper.group(
            conversation_chunks
        )

        ranked_documents = DocumentRanker.rank(
            grouped_documents
        )

        mapped_documents = EvidenceMapper.map(
            ranked_documents
        )

        reasoning_context = CrossDocumentReasoner.build_context(
            mapped_documents
        )

        # --------------------------------------------------
        # Report Statistics
        # --------------------------------------------------


        session_stats = SessionDocumentStats.get(
            session_id
        )

        scores = [

            chunk.get("score", 0)

            for chunk in conversation_chunks

        ]

        average_score = (

            sum(scores) / len(scores)

            if scores else 0

        )

        report_stats = {

            # Upload Statistics
            "uploaded_documents": session_stats["uploaded_documents"],

            "total_chunks": session_stats["total_chunks"],

            # Conversation Statistics
            "conversation_questions": len(

                [

                    m

                    for m in conversation_history

                    if m.get("role") == "user"

                ]

            ),

            # Retrieval Statistics
            "documents_used": len(
                reasoning_context["documents"]
            ),

            "evidence_chunks": len(
                conversation_chunks
            ),

            # Confidence
            "overall_confidence": round(
                average_score * 100
            )

        }

        # --------------------------------------------------
        # Build Evidence Context
        # --------------------------------------------------

        evidence = ""

        for document in reasoning_context["documents"]:

            evidence += f"""

Document:
{document['document']}

Importance:
{document['importance']}

"""

            for chunk in document["evidence"]:

                evidence += f"""

{chunk['text']}

"""

        # --------------------------------------------------
        # Build Prompt
        # --------------------------------------------------

        prompt = f"""

{REPORT_PROMPT}

======================================================
CONVERSATION HISTORY
======================================================

{history}

======================================================
MEDICAL DOCUMENTS
======================================================

{evidence}

"""

        # --------------------------------------------------
        # Generate Report
        # --------------------------------------------------

        try:

            llm_result = LLMManager.generate(

                prompt=prompt,

                provider=provider

            )

            response = llm_result["response"]

            used_provider = llm_result["provider"]

            print(
                f"\n✓ Report generated using {used_provider.upper()}"
            )

        except Exception as e:

            print("\n========== REPORT ERROR ==========")
            print(e)
            print("==================================\n")

            return {

                "report": {

                    "executive_summary":
                    "Unable to generate report because all configured AI providers are currently unavailable.",

                    "clinical_findings": [],

                    "clinical_interpretation":
                    "Not available.",

                    "cross_document_reasoning":
                    "Not available.",

                    "medications": [],

                    "recommendations": [],

                    "sources": []

                },

                "provider": "unknown",

                "stats": report_stats,

                "reasoning": reasoning_context

            }

        print("\n========== RAW REPORT ==========")
        print(response)
        print("================================\n")

        # --------------------------------------------------
        # Clean Response
        # --------------------------------------------------

        cleaned_response = response.strip()

        cleaned_response = re.sub(

            r"^```json",

            "",

            cleaned_response,

            flags=re.IGNORECASE

        )

        cleaned_response = re.sub(

            r"^```",

            "",

            cleaned_response

        )

        cleaned_response = re.sub(

            r"```$",

            "",

            cleaned_response

        ).strip()

        # --------------------------------------------------
        # Extract JSON
        # --------------------------------------------------

        start = cleaned_response.find("{")
        end = cleaned_response.rfind("}")

        if start != -1 and end != -1:

            cleaned_response = cleaned_response[
                start:end + 1
            ]

        # --------------------------------------------------
        # Parse JSON
        # --------------------------------------------------

        try:

            report = json.loads(
                cleaned_response
            )

            print(
                "✓ Report JSON Parsed Successfully"
            )

        except Exception as e:

            print("\n========== REPORT PARSE ERROR ==========")
            print(e)
            print("========================================\n")

            report = {

                "executive_summary": response,

                "clinical_findings": [],

                "clinical_interpretation":
                "Not available.",

                "cross_document_reasoning":
                "Not available.",

                "medications": [],

                "recommendations": [],

                "sources": []

            }

        print("\n========== FINAL REPORT ==========")
        print("\n========== REPORT STATS ==========")
        print(report_stats)
        print("==================================")

        print("\n========== REASONING CONTEXT ==========")
        print(reasoning_context)
        print("=======================================")

        return {

            "report": report,

            "provider": used_provider,

            "stats": {

                "uploaded_documents": report_stats["uploaded_documents"],

                "total_chunks": report_stats["total_chunks"],

                "documents_used": report_stats["documents_used"],

                "evidence_chunks": report_stats["evidence_chunks"],

                "conversation_questions": report_stats["conversation_questions"],

                "overall_confidence": report_stats["overall_confidence"]

            },

            "reasoning": {

                "document_count": reasoning_context["document_count"],

                "highest_score": reasoning_context["highest_score"],

                "documents": reasoning_context["documents"]

            }

        }