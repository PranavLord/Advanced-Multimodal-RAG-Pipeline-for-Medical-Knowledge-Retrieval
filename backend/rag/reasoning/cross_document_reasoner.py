from typing import Dict, List


class CrossDocumentReasoner:
    """
    Creates a structured reasoning context from
    multiple retrieved documents.

    This component DOES NOT call an LLM.

    Its responsibility is to organize the retrieved
    evidence so the Prompt Builder can generate a
    much better prompt for the LLM.
    """

    @staticmethod
    def build_context(
        mapped_documents: List[Dict]
    ) -> Dict:

        reasoning_context = {

            "document_count": len(mapped_documents),

            "highest_score": 0.0,

            "documents": []

        }

        if mapped_documents:

            reasoning_context["highest_score"] = max(

                doc["score"]

                for doc in mapped_documents

            )

        print()
        print("=" * 70)
        print("MULTI DOCUMENT REASONER")
        print("=" * 70)

        for rank, document in enumerate(

            mapped_documents,

            start=1

        ):

            # ------------------------------------------
            # Determine document importance
            # ------------------------------------------

            score = document["score"]

            if score >= 0.90:

                importance = "Very High"

            elif score >= 0.80:

                importance = "High"

            elif score >= 0.70:

                importance = "Medium"

            else:

                importance = "Low"

            # ------------------------------------------
            # Extract evidence
            # ------------------------------------------

            evidence = []

            for item in document["evidence"]:

                evidence.append(

                    {

                        "chunk_index": item["chunk_index"],

                        "score": item["score"],

                        "text": item["text"]

                    }

                )

            # ------------------------------------------
            # Build document reasoning block
            # ------------------------------------------

            reasoning_context["documents"].append(

                {

                    "rank": rank,

                    "document": document["document"],

                    "importance": importance,

                    "score": score,

                    "average_score": document["average_score"],

                    "chunk_count": document["chunk_count"],

                    "evidence": evidence

                }

            )

            print(f"{rank}. {document['document']}")

            print(f"   Importance : {importance}")

            print(f"   Score      : {score:.4f}")

            print(f"   Evidence   : {len(evidence)}")

            print()

        print("=" * 70)

        return reasoning_context