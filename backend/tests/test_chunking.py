from document_processors.pdf_parser import (
    PDFParser
)

from rag.indexing.chunking import (
    MedicalChunker
)


def main():

    parser = PDFParser()

    chunker = MedicalChunker()

    text = parser.extract_text(
        "data/sample_reports/sample.pdf"
    )

    chunks = chunker.split(text)

    print(
        f"Total Chunks: {len(chunks)}"
    )

    print("\nFIRST CHUNK\n")

    print(chunks[0])


if __name__ == "__main__":
    main()