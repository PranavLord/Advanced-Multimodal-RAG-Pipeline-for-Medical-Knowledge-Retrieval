from rag.indexing.vector_builder import (
    VectorBuilder
)

chunks = [
    "Patient has Diabetes"
]

embeddings = [
    [0.1] * 768
]

vectors = VectorBuilder.build(
    chunks,
    embeddings
)

print(vectors)