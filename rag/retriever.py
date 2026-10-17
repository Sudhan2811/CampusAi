
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle


class Retriever:

    def __init__(self):
        print("Loading embedding model...")

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.index = None
        self.documents = []

    def build_index(self, documents):

        if not documents:
            raise ValueError(
                "Cannot build FAISS index: documents are empty."
            )

        self.documents = documents

        print("Creating embeddings...")

        # Extract only the text for embedding
        texts = [
            document["text"]
            for document in documents
        ]

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True
        )

        embeddings = embeddings.astype("float32")

        # Normalize embeddings for cosine similarity
        faiss.normalize_L2(embeddings)

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(dimension)

        self.index.add(embeddings)

        print(
            f"FAISS index created with "
            f"{self.index.ntotal} vectors"
        )

    def search(self, query, top_k=3):

        # Check whether the index is ready
        if self.index is None:
            raise RuntimeError(
                "FAISS index is not loaded. "
                "Call load() or build_index() first."
            )

        # Handle empty queries
        if not isinstance(query, str) or not query.strip():
            return []

        # Validate top_k
        if not isinstance(top_k, int) or isinstance(top_k, bool) or top_k <= 0:
            raise ValueError(
                "top_k must be a positive integer."
            )

        # Ensure index and documents are consistent
        if self.index.ntotal != len(self.documents):
            raise RuntimeError(
                "FAISS index and document count do not match."
            )

        if self.index.ntotal == 0:
            return []

        # Retrieve no more results than available vectors
        k = min(top_k, self.index.ntotal)

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True
        ).astype("float32")

        # Normalize query for cosine similarity
        faiss.normalize_L2(query_embedding)

        scores, indices = self.index.search(
            query_embedding,
            k
        )

        results = []

        for score, doc_index in zip(
            scores[0],
            indices[0]
        ):

            # FAISS uses -1 when no result is available
            if doc_index == -1:
                continue

            document = self.documents[doc_index]

            results.append({
                "chunk": document["text"],
                "source": document["source"],
                "score": float(score)
            })

        return results

    def save(
        self,
        index_path="rag/faiss.index",
        chunks_path="rag/chunks.pkl"
    ):

        if self.index is None:
            raise RuntimeError(
                "Cannot save: FAISS index has not been built."
            )

        if self.index.ntotal != len(self.documents):
            raise RuntimeError(
                "Cannot save: index and document count do not match."
            )

        faiss.write_index(
            self.index,
            index_path
        )

        with open(chunks_path, "wb") as file:
            pickle.dump(
                self.documents,
                file
            )

        print("FAISS index saved.")

    def load(
        self,
        index_path="rag/faiss.index",
        chunks_path="rag/chunks.pkl"
    ):

        # Load the saved index and corresponding documents
        loaded_index = faiss.read_index(index_path)

        with open(chunks_path, "rb") as file:
            loaded_documents = pickle.load(file)

        # Validate before assigning the loaded data
        if loaded_index.ntotal != len(loaded_documents):
            raise RuntimeError(
                "Loaded FAISS index and document count do not match."
            )

        self.index = loaded_index
        self.documents = loaded_documents

        print(
            f"FAISS index loaded: "
            f"{self.index.ntotal} vectors"
        )



if __name__ == "__main__":

    questions = [
        "When does the B.Tech registration start?",
        "What is the hostel mess fee for students?"
    ]

    retriever = Retriever()
    retriever.load()

    for question in questions:
        print(f"\nQUESTION: {question}")

        results = retriever.search(question, top_k=3)

        if not results:
            print("No matching documents found.")
            continue

        for result in results:
            print("Score:", round(result["score"], 4))
            print("Source:", result["source"])
            print("Chunk:", result["chunk"][:200])
