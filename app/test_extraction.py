from app.documents.extraction.pdf import PDFExtractor


def extract():
    extractor = PDFExtractor()
    content = extractor.extract(
        "/Users/saimonalam/Work/docuask/uploads/79/7e/797e2887-b752-45a2-a8c9-b776890aa8b7.pdf"
    )
    print(content)


if __name__ == "__main__":
    extract()
