from pathlib import Path

from rag.ingest import load_pdf, create_chunks
from rag.retriever import Retriever


DATA_DIR = Path("rag/data")


def main():

    pdf_files = list(DATA_DIR.glob("*.pdf"))

    if not pdf_files:
        print("No PDF files found in rag/data")
        return

    documents = []

    for pdf_path in pdf_files:

        print(f"\nProcessing: {pdf_path.name}")

        text = load_pdf(pdf_path)

        chunks = create_chunks(text)

        print(f"Created {len(chunks)} chunks")

        for chunk in chunks:

            documents.append({
                "text": chunk,
                "source": pdf_path.name
            })

    print(f"\nTotal chunks: {len(documents)}")

    retriever = Retriever()

    retriever.build_index(documents)

    retriever.save()

    print("\nRAG index built successfully!")


if __name__ == "__main__":
    main()