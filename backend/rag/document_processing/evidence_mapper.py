from typing import Dict, List


class EvidenceMapper:
    """
    Converts ranked documents into structured evidence
    that can be consumed by the Prompt Builder.

    Each document contains:
    - document name
    - relevance score
    - supporting evidence (chunks)
    """

    @staticmethod
    def map(
        ranked_documents: List[Dict]
    ) -> List[Dict]:

        mapped_documents = []

        # ------------------------------------------
        # Build Evidence
        # ------------------------------------------

        for document in ranked_documents:

            evidence = []

            for chunk in document["chunks"]:

                evidence.append(

                    {

                        "chunk_index": chunk.get(
                            "chunk_index",
                            0
                        ),

                        "score": chunk.get(
                            "score",
                            0.0
                        ),

                        "text": chunk.get(
                            "text",
                            ""
                        ).strip()

                    }

                )

            mapped_documents.append(

                {

                    "document": document["document"],

                    "score": document["score"],

                    "average_score": document["average_score"],

                    "chunk_count": document["chunk_count"],

                    "evidence": evidence

                }

            )

        # ------------------------------------------
        # Logging
        # ------------------------------------------

        print()

        print("=" * 60)
        print("EVIDENCE MAPPER")
        print("=" * 60)

        for document in mapped_documents:

            print(

                f"Document : {document['document']}"

            )

            print(

                f"Evidence Chunks : {document['chunk_count']}"

            )

            print(

                f"Document Score : {document['score']:.4f}"

            )

            print()

        print("=" * 60)

        return mapped_documents