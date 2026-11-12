from typing import Dict, List


class DocumentRanker:
    """
    Assigns a relevance score to each document
    based on the similarity scores of its retrieved chunks.
    """

    @staticmethod
    def rank(
        grouped_documents: Dict[str, List[Dict]]
    ) -> List[Dict]:

        ranked_documents = []

        # ------------------------------------------
        # Compute document score
        # ------------------------------------------

        for document_name, chunks in grouped_documents.items():

            scores = [

                chunk.get("score", 0.0)

                for chunk in chunks

            ]

            if scores:

                highest_score = max(scores)

                average_score = sum(scores) / len(scores)

            else:

                highest_score = 0.0

                average_score = 0.0

            ranked_documents.append(

                {

                    "document": document_name,

                    "score": highest_score,

                    "average_score": average_score,

                    "chunk_count": len(chunks),

                    "chunks": chunks

                }

            )

        # ------------------------------------------
        # Sort documents
        # ------------------------------------------

        ranked_documents.sort(

            key=lambda document: document["score"],

            reverse=True

        )

        # ------------------------------------------
        # Logging
        # ------------------------------------------

        print()

        print("=" * 60)
        print("DOCUMENT RANKER")
        print("=" * 60)

        for index, document in enumerate(

            ranked_documents,

            start=1

        ):

            print(

                f"{index}. "

                f"{document['document']}"

            )

            print(

                f"   Highest Score : "

                f"{document['score']:.4f}"

            )

            print(

                f"   Average Score : "

                f"{document['average_score']:.4f}"

            )

            print(

                f"   Chunks : "

                f"{document['chunk_count']}"

            )

            print()

        print("=" * 60)

        return ranked_documents