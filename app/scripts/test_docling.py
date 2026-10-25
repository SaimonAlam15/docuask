from docling.chunking import HybridChunker
from docling.document_converter import DocumentConverter

converter = DocumentConverter()
result = converter.convert("saimon_alam_resume.pdf")

document = result.document

print(document.export_to_markdown())

chunker = HybridChunker()

for chunk in chunker.chunk(document):
    print("Headings:", chunk.meta.headings)
    print("Content:", chunk.text)
    print("---")
