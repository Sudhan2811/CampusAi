from rag.ingest import load_pdf, create_chunks
from rag.retriever import Retriever


pdf_path = "rag/data/ADMISSION_FORM_REGISTRATION_NOTICE_FOR_B.TECH_2026.pdf"


# Load PDF
text = load_pdf(pdf_path)

# Create chunks
chunks = create_chunks(text)


# Create retriever
retriever = Retriever()

# Build vector index
retriever.build_index(chunks)


# Test semantic search
query = "When does online registration start?"

results = retriever.search(
    query,
    top_k=3
)


print("\nSEARCH RESULTS:\n")

for i, result in enumerate(results):

    print(f"--- Result {i + 1} ---")
    print(f"Similarity: {result['score']:.4f}")
    print(result["chunk"][:500])
    print()