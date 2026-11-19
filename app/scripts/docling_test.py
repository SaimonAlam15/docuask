from docling.chunking import HybridChunker
from docling.document_converter import DocumentConverter
from docling_core.transforms.chunker.tokenizer.huggingface import (
    HuggingFaceTokenizer,
)
from transformers import AutoTokenizer


def chunk():
    converter = DocumentConverter()
    result = converter.convert("saimon_alam_cl_breathment.pdf")

    document = result.document

    # print(document.export_to_markdown())

    chunker = HybridChunker(
        max_tokens=400,
        merge_peers=True,
    )

    for chunk in chunker.chunk(document):
        print("Headings:", chunk.meta.headings)
        print("Content:", chunk.text)
        print("---")


def count_tokens(text: str):
    # Initialize the HuggingFace tokenizer wrapper
    tokenizer = HuggingFaceTokenizer.from_pretrained(
        model_name="sentence-transformers/all-MiniLM-L6-v2", max_tokens=400
    )

    token_count = tokenizer.count_tokens(text)

    print(f"Token count: {token_count}")


if __name__ == "__main__":
    count_tokens(
        "| - |\n| 14/06/2025, Description = NORTH END PVT LTD DHANMON. 14/06/2025, Withdrawal = 180.00. 14/06/2025, Deposit = -. 14/06/2025, Balance = 4,661,454.22. 14/06/2025, Description = ATM WDR AT 11040022 /19:. 14/06/2025, Withdrawal = 4,000.00. 14/06/2025, Deposit = -. 14/06/2025, Balance = 4,657,454.22. 14/06/2025, Description = LAZZ PHARMA FRANCHISE. 14/06/2025, Withdrawal = 160.00. 14/06/2025, Deposit = -. 14/06/2025, Balance = 4,657,294.22. 14/06/2025, Description = JAAGO FOUNDATION. 14/06/2025, Withdrawal = 5,100.00. 14/06/2025, Deposit = -. 14/06/2025, Balance = 4,652,194.22. 14/06/2025, Description = M/S GINZA DHANMONDI. 14/06/2025, Withdrawal = 1,984.50. 14/06/2025, Deposit = -. 14/06/2025, Balance = 4,650,209.72. 14/06/2025, Description = PRESCRIPTION AID PHARM>D. 14/06/2025, Withdrawal = 1,850.00. 14/06/2025, Deposit = -. 14/06/2025, Balance = 4,648,359.72. 14/06/2025, Description = FOODPANDA BANGLADESH"
    )
