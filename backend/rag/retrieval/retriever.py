from core.embeddings.pubmedbert import (
    PubMedBERTEmbedding
)

from core.vectorstore_manager.pinecone_manager import (
    PineconeManager
)


class Retriever:
    """
    Retrieves the most relevant chunks
    from Pinecone for a given user query.
    """

    def __init__(self):

        self.embedder = PubMedBERTEmbedding()

        self.pinecone = PineconeManager()

    def retrieve(
        self,
        question: str,
        session_id: str,
        top_k: int = 5
    ):
        """
        Retrieve the top-k relevant chunks
        belonging only to the current upload session.

        Parameters
        ----------
        question : str
            User question.

        session_id : str
            Current upload session identifier.

        top_k : int
            Number of chunks to retrieve.

        Returns
        -------
        list[dict]
            Retrieved chunks.
        """

        # ------------------------------------------
        # Step 1 : Generate Query Embedding
        # ------------------------------------------

        query_embedding = self.embedder.embed(
            [question]
        )[0]

        # ------------------------------------------
        # Step 2 : Search Pinecone
        # ------------------------------------------

        results = self.pinecone.search(

            query_embedding=query_embedding,

            session_id=session_id,

            top_k=top_k

        )

        # ------------------------------------------
        # Step 3 : Convert Matches
        # ------------------------------------------

        chunks = []

        for match in results.matches:

            metadata = match.metadata or {}

            chunks.append({

                "text": metadata.get(
                    "text",
                    ""
                ),

                "source": metadata.get(
                    "source",
                    "Unknown"
                ),

                "chunk_index": metadata.get(
                    "chunk_index",
                    0
                ),

                "session_id": metadata.get(
                    "session_id",
                    ""
                ),

                "score": match.score

            })

        return chunks