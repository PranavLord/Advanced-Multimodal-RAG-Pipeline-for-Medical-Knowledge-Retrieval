from collections import defaultdict
from typing import Dict, List


class DocumentGrouper:
    """
    Groups retrieved chunks by their source document.

    Example
    -------
    Input:
        [
            {"source": "Blood_Report.pdf", ...},
            {"source": "Blood_Report.pdf", ...},
            {"source": "MRI_Report.pdf", ...}
        ]

    Output:
        {
            "Blood_Report.pdf": [...],
            "MRI_Report.pdf": [...]
        }
    """

    @staticmethod
    def group(
        chunks: List[Dict]
    ) -> Dict[str, List[Dict]]:

        grouped_documents = defaultdict(list)

        # ------------------------------------------
        # Group chunks by source document
        # ------------------------------------------

        for chunk in chunks:

            document_name = chunk.get(
                "source",
                "Unknown Document"
            )

            grouped_documents[document_name].append(
                chunk
            )

        # ------------------------------------------
        # Sort chunks inside each document
        # ------------------------------------------

        for document in grouped_documents:

            grouped_documents[document].sort(

                key=lambda chunk: chunk.get(
                    "chunk_index",
                    0
                )

            )

        # ------------------------------------------
        # Logging
        # ------------------------------------------

        print()

        print("=" * 60)
        print("DOCUMENT GROUPER")
        print("=" * 60)

        print(
            f"Documents Retrieved : {len(grouped_documents)}"
        )

        total_chunks = 0

        for document, chunks in grouped_documents.items():

            total_chunks += len(chunks)

            print(
                f"• {document:<35} {len(chunks)} chunks"
            )

        print()

        print(
            f"Total Retrieved Chunks : {total_chunks}"
        )

        print("=" * 60)

        return dict(grouped_documents)