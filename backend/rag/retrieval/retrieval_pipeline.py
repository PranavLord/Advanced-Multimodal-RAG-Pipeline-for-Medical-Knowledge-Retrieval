from rag.retrieval.query_embedder import (
    QueryEmbedder
)

from rag.retrieval.retriever import (
    Retriever
)

from rag.retrieval.context_builder import (
    ContextBuilder
)


class RetrievalPipeline:

    def __init__(self):

        self.query_embedder = (
            QueryEmbedder()
        )

        self.retriever = (
            Retriever()
        )

    def retrieve(
        self,
        question,
        tracker
    ):

        tracker.add(
            "Question Received"
        )

        query_embedding = (
            self.query_embedder.embed_query(
                question
            )
        )

        tracker.add(
            "Query Embedded"
        )

        matches = (
            self.retriever.retrieve(
                query_embedding
            )
        )

        tracker.add(
            f"Retrieved {len(matches)} Chunks"
        )

        context = (
            ContextBuilder.build(
                matches
            )
        )

        tracker.add(
            "Context Built"
        )

        return {

            "question": question,

            "retrieved_chunks":
                len(matches),

            "context":
                context
        }