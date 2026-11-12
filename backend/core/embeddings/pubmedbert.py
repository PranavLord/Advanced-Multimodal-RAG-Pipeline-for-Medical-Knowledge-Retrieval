from sentence_transformers import (
    SentenceTransformer
)


class PubMedBERTEmbedding:

    def __init__(self):

        self.model = SentenceTransformer(
            "pritamdeka/PubMedBERT-mnli-snli-scinli-scitail-mednli-stsb"
        )

        

    def embed(self, texts):

        return self.model.encode(
            texts,
            normalize_embeddings=True
        ).tolist()