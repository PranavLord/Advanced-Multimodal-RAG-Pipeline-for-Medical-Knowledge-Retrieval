from core.embeddings.pubmedbert import (
    PubMedBERTEmbedding
)


model = PubMedBERTEmbedding()

vectors = model.embed([
    "Patient has pneumonia."
])

print(len(vectors))

print(len(vectors[0]))