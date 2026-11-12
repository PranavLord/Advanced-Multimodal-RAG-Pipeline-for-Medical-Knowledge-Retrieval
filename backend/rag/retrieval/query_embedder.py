from core.embeddings.pubmedbert import (
    PubMedBERTEmbedding
)


class QueryEmbedder:

    def __init__(self):

        self.embedder = (
            PubMedBERTEmbedding()
        )

    def embed_query(
        self,
        question: str
    ):

        embedding = self.embedder.embed(
            [question]
        )

        return embedding[0]