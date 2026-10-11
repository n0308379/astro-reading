"""Ingest the astrology knowledge base (PDFs) into a local Qdrant collection.

Skeleton: extract text, chunk it, embed it, upsert into Qdrant.
Only knowledge content is stored, never user data.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent / "data" / "knowledge"
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION = os.getenv("QDRANT_COLLECTION", "astro_knowledge")


def main() -> None:
    pdfs = sorted(KNOWLEDGE_DIR.glob("*.pdf"))
    if not pdfs:
        print(f"No PDFs found in {KNOWLEDGE_DIR}")
        return
    for pdf in pdfs:
        print(f"TODO: ingest {pdf.name} into {COLLECTION} at {QDRANT_URL}")


if __name__ == "__main__":
    main()
