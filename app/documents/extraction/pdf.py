from pathlib import Path

import pymupdf


class PDFExtractor:
    def extract_text(self, file_path: Path) -> str:
        with pymupdf.open(file_path) as document:
            return "\n".join(page.get_text() for page in document)
