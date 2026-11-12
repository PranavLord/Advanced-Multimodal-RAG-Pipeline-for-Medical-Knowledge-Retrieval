from rag.retrieval.retriever import (
    Retriever
)

from rag.query_processing.query_rewriter import (
    QueryRewriter
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

from core.llm.prompting.prompt_builder import (
    PromptBuilder
)

from core.llm.llm_manager import (
    LLMManager
)

from core.llm.output_parser import (
    OutputParser
)

from core.llm.memory.conversation_memory import (
    ConversationMemory
)

from core.llm.memory.conversation_evidence import (
    ConversationEvidence
)


class GenerationPipeline:
    """
    End-to-end Retrieval Augmented Generation (RAG)
    pipeline with Multi-Document Intelligence.
    """

    def __init__(self):

        self.retriever = Retriever()

        self.prompt_builder = PromptBuilder()

    def generate(
        self,
        question: str,
        session_id: str,
        provider: str | None = None
    ) -> dict:

        print()

        print("=" * 60)
        print("RAG GENERATION PIPELINE")
        print("=" * 60)

        # --------------------------------------------------
        # Step 1 : Load Conversation History
        # --------------------------------------------------

        print("\n[1/10] Loading conversation history...")

        conversation_history = ConversationMemory.get_history(
            session_id
        )

        print(
            f"✓ Loaded {len(conversation_history)} previous messages."
        )

        # --------------------------------------------------
        # Step 2 : Rewrite Query
        # --------------------------------------------------

        print("\n[2/10] Processing query...")

        if (
            conversation_history
            and QueryRewriter.needs_rewrite(question)
        ):

            rewritten_question = QueryRewriter.rewrite(

                question=question,

                conversation_history=conversation_history,

                provider=provider

            )

            print("✓ Follow-up question detected.")
            print(
                f"✓ Rewritten Query: {rewritten_question}"
            )

        else:

            rewritten_question = question

            print("✓ Standalone question detected.")

        # --------------------------------------------------
        # Step 3 : Retrieve Chunks
        # --------------------------------------------------

        print("\n[3/10] Retrieving relevant chunks...")

        retrieved_chunks = self.retriever.retrieve(

            question=rewritten_question,

            session_id=session_id

        )

        print(
            f"✓ Retrieved {len(retrieved_chunks)} chunks."
        )

        # --------------------------------------------------
        # Step 4 : Group Documents
        # --------------------------------------------------

        print("\n[4/10] Grouping documents...")

        grouped_documents = DocumentGrouper.group(

            retrieved_chunks

        )

        # --------------------------------------------------
        # Step 5 : Rank Documents
        # --------------------------------------------------

        print("\n[5/10] Ranking documents...")

        ranked_documents = DocumentRanker.rank(

            grouped_documents

        )

        # --------------------------------------------------
        # Step 6 : Map Evidence
        # --------------------------------------------------

        print("\n[6/10] Mapping evidence...")

        mapped_documents = EvidenceMapper.map(

            ranked_documents

        )

        # --------------------------------------------------
        # Store ONLY Retrieved Chunks
        # --------------------------------------------------

        try:

            ConversationEvidence.add_question(

                session_id=session_id,

                question=question,

                retrieved_chunks=retrieved_chunks

            )
            ConversationEvidence.print(session_id)

            print(
                "✓ Retrieval evidence stored for this question."
            )

        except Exception as e:

            print("\n========== EVIDENCE STORAGE ERROR ==========")
            print(e)
            print("============================================\n")

        # --------------------------------------------------
        # Step 7 : Cross Document Reasoning
        # --------------------------------------------------

        print("\n[7/10] Building reasoning context...")

        reasoning_context = CrossDocumentReasoner.build_context(

            mapped_documents

        )

        # --------------------------------------------------
        # Step 8 : Build Prompt
        # --------------------------------------------------

        print("\n[8/10] Building prompt...")

        prompt = self.prompt_builder.build(

            reasoning_context=reasoning_context,

            question=rewritten_question,

            conversation_history=conversation_history

        )

        print("✓ Prompt created successfully.")

        # --------------------------------------------------
        # Step 9 : Generate Response
        # --------------------------------------------------

        print("\n[9/10] Initializing LLM...")

        llm_result = LLMManager.generate(

            prompt=prompt,

            provider=provider

        )

        response = llm_result["response"]

        used_provider = llm_result["provider"]

        print(
            f"✓ Response generated using {used_provider.upper()}."
        )

        # --------------------------------------------------
        # Step 10 : Parse Response
        # --------------------------------------------------

        print("\n[10/10] Parsing response...")

        final_response = OutputParser.parse(

            response

        )

        ConversationMemory.add_message(

            session_id=session_id,

            role="user",

            content=question

        )

        ConversationMemory.add_message(

            session_id=session_id,

            role="assistant",

            content=final_response

        )

        print(
            "✓ Conversation history updated."
        )

        print()

        print("=" * 60)
        print("PIPELINE COMPLETED")
        print("=" * 60)

        return {

            "answer": final_response,

            "provider": used_provider

        }