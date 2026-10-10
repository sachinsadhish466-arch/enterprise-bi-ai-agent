
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DOCUMENTS_DIR = PROJECT_ROOT / "documents"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def load_chunks():
    """Load text files and split them into searchable chunks."""

    chunks = []

    for path in sorted(DOCUMENTS_DIR.glob("*.txt")):
        text = path.read_text(encoding="utf-8")
        words = text.split()

        chunk_size = 100
        overlap = 20
        step = chunk_size - overlap

        for start in range(0, len(words), step):
            chunk = " ".join(words[start:start + chunk_size])

            if chunk.strip():
                chunks.append({
                    "source": path.name,
                    "text": chunk,
                })

    return chunks


def main():
    chunks = load_chunks()

    if not chunks:
        print("No text documents found in the documents folder.")
        return

    print(f"Loaded {len(chunks)} document chunks.")
    print("Loading the local embedding model...")

    model = SentenceTransformer(MODEL_NAME)

    documents = [item["text"] for item in chunks]

    vectors = model.encode(
        documents,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=True,
    )

    vectors = np.asarray(vectors, dtype=np.float32)

    # Normalized vectors + inner product = cosine similarity.
    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)

    print(f"FAISS index created with {index.ntotal} vectors.")
    print("\nSEMANTIC DOCUMENT SEARCH")
    print("Type 'exit' to stop.")

    while True:
        question = input("\nAsk a business question: ").strip()

        if question.lower() in {"exit", "quit"}:
            break

        if not question:
            continue

        query_vector = model.encode(
            [question],
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

        query_vector = np.asarray(
            query_vector,
            dtype=np.float32,
        )

        scores, indices = index.search(
            query_vector,
            min(3, len(chunks)),
        )

        print("\nRETRIEVED PASSAGES")
        print("-" * 50)

        for score, idx in zip(scores[0], indices[0]):
            if idx < 0:
                continue

            item = chunks[int(idx)]

            print(f"\nSource: {item['source']}")
            print(f"Similarity score: {float(score):.3f}")
            print(item["text"])


if __name__ == "__main__":
    main()
