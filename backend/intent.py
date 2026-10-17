from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

RAG_EXAMPLES = [
    "When does B.Tech admission registration start?",
    "How do I register for admission?",
    "What documents are required for physical reporting?",
    "When should newly admitted students report?",
    "How do I complete the admission form?",
    "What is the registration process for B.Tech students?",
]

rag_embeddings = model.encode(
    RAG_EXAMPLES,
    convert_to_numpy=True
)


def is_rag_question(message: str, threshold=0.45):
    query_embedding = model.encode(
        [message],
        convert_to_numpy=True
    )[0]

    similarities = np.dot(
        rag_embeddings,
        query_embedding
    ) / (
        np.linalg.norm(rag_embeddings, axis=1)
        * np.linalg.norm(query_embedding)
    )

    best_score = float(np.max(similarities))

    print(f"RAG similarity: {best_score:.4f}")

    return best_score >= threshold