from rag.retrieval.query_embedder import (
    QueryEmbedder
)

from rag.retrieval.retriever import (
    Retriever
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

print(
    f"Retrieved {len(matches)} chunks"
)