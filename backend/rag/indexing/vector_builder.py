import uuid


class VectorBuilder:

    @staticmethod
    def build(
        chunks,
        embeddings,
        source_file=None,
        session_id=None
    ):

        vectors = []

        for idx, (chunk, embedding) in enumerate(
            zip(chunks, embeddings)
        ):

            vectors.append(

                {
                    "id": str(
                        uuid.uuid4()
                    ),

                    "values": embedding,

                    "metadata": {

                        # ----------------------------------
                        # Session Information
                        # ----------------------------------

                        "session_id": session_id,

                        # ----------------------------------
                        # Chunk Information
                        # ----------------------------------

                        "text": chunk,

                        "chunk_index": idx,

                        # ----------------------------------
                        # Source Information
                        # ----------------------------------

                        "source": source_file
                    }
                }

            )

        return vectors