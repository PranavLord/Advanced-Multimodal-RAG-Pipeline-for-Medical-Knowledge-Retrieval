from document_processors.pdf_parser import (
    PDFParser
)


def main():

    parser = PDFParser()

    text = parser.extract_text(
        "data/sample_reports/sample.pdf"
    )

    print(text[:2000])


if __name__ == "__main__":
    main()