import os

from document_processors.pdf_parser import PDFParser

from rag.indexing.chunking import MedicalChunker

from core.embeddings.pubmedbert import (
    PubMedBERTEmbedding
)

from core.vectorstore_manager.pinecone_manager import (
    PineconeManager
)

from core.llm.memory.session_document_stats import (
    SessionDocumentStats
)

from rag.indexing.vector_builder import (
    VectorBuilder
)


class IngestionPipeline:

    def __init__(self):

        self.parser = PDFParser()

        self.chunker = MedicalChunker()

        self.embedder = PubMedBERTEmbedding()

        self.pinecone = PineconeManager()

    def ingest(
        self,
        pdf_path,
        tracker,
        session_id
    ):

        # --------------------------------------------------
        # Step 1 : PDF Uploaded
        # --------------------------------------------------

        tracker.add(
            "PDF Uploaded"
        )

        # --------------------------------------------------
        # Step 2 : Extract Text
        # --------------------------------------------------

        text = self.parser.extract_text(
            pdf_path
        )

        tracker.add(
            "Text Extraction Completed"
        )

        # --------------------------------------------------
        # Validation : Extracted Text
        # --------------------------------------------------

        if not text or not text.strip():

            raise ValueError(
                "No readable text was found in the uploaded PDF.\n\n"
                "This usually happens when the document is scanned, "
                "image-based, encrypted, or contains no selectable text.\n\n"
                "Please upload a text-based medical report."
            )

        # --------------------------------------------------
        # Step 3 : Chunking
        # --------------------------------------------------

        chunks = self.chunker.split(
            text
        )

        if not chunks:

            raise ValueError(
                "The uploaded PDF could not be converted into readable text chunks."
            )

        tracker.add(
            f"Chunking Completed ({len(chunks)} chunks)"
        )

        # --------------------------------------------------
        # Update Session Upload Statistics
        # --------------------------------------------------

        current_stats = SessionDocumentStats.get(
            session_id
        )

        document_chunk_counts = current_stats[
            "document_chunk_counts"
        ]

        source_file = os.path.basename(
            pdf_path
        )

        # Store/Update this document's chunk count
        document_chunk_counts[source_file] = len(
            chunks
        )

        uploaded_documents = len(
            document_chunk_counts
        )

        total_chunks = sum(
            document_chunk_counts.values()
        )

        SessionDocumentStats.save(

            session_id=session_id,

            uploaded_documents=uploaded_documents,

            total_chunks=total_chunks,

            document_chunk_counts=document_chunk_counts

        )

        SessionDocumentStats.print(
            session_id
        )

        # --------------------------------------------------
        # Step 4 : Generate Embeddings
        # --------------------------------------------------

        embeddings = self.embedder.embed(
            chunks
        )

        tracker.add(
            "Embeddings Generated"
        )

        # --------------------------------------------------
        # Step 5 : Build Pinecone Vectors
        # --------------------------------------------------

        vectors = VectorBuilder.build(

            chunks=chunks,

            embeddings=embeddings,

            source_file=source_file,

            session_id=session_id

        )

        tracker.add(
            f"Vectors Created ({len(vectors)})"
        )

        # --------------------------------------------------
        # Step 6 : Store In Pinecone
        # --------------------------------------------------

        self.pinecone.upsert(
            vectors
        )

        tracker.add(
            "Stored In Pinecone"
        )

        # --------------------------------------------------
        # Final Response
        # --------------------------------------------------

        return {

            "chunks": len(chunks),

            "vectors": len(vectors),

            "characters": len(text),

            "source_file": source_file,

            "session_id": session_id,

            "uploaded_documents": uploaded_documents,

            "total_chunks": total_chunks,

            "document_chunk_counts": document_chunk_counts

        }