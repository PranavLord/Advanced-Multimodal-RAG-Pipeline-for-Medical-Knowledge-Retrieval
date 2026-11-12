from rag.retrieval.query_embedder import (
    QueryEmbedder
)

from rag.retrieval.retriever import (
    Retriever
)

from rag.retrieval.context_builder import (
    ContextBuilder
)

embedder = QueryEmbedder()

retriever = Retriever()

query_embedding = (
    embedder.embed_query(
        "What diagnosis was found?"
    )
)

matches = (
    retriever.retrieve(
        query_embedding
    )
)

context = (
    ContextBuilder.build(
        matches
    )
)

print(context)