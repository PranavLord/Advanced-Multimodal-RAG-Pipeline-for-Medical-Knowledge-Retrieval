from rag.retrieval.query_embedder import (
    QueryEmbedder
)

embedder = QueryEmbedder()

vector = embedder.embed_query(
    "What diagnosis was found?"
)

print(
    len(vector)
)