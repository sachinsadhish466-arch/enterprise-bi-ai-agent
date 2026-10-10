
from pathlib import Path
import re


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DOCUMENTS_DIR = PROJECT_ROOT / "documents"


def load_documents():
    """Read all .txt documents from the documents directory."""

    documents = []

    for file_path in sorted(DOCUMENTS_DIR.glob("*.txt")):
        text = file_path.read_text(encoding="utf-8")

        if text.strip():
            documents.append({
                "filename": file_path.name,
                "text": text,
            })

    return documents


def chunk_text(text, chunk_size=120, overlap=25):
    """Split text into overlapping word-based chunks."""

    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError(
            "chunk_size must be positive and overlap "
            "must be between 0 and chunk_size."
        )

    words = text.split()
    chunks = []

    for start in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[start:start + chunk_size])

        if chunk:
            chunks.append(chunk)

    return chunks


def tokenize(text):
    """Convert text to lowercase searchable terms."""

    return set(re.findall(r"\b[a-z0-9]+\b", text.lower()))


def retrieve_documents(question, top_k=3):
    """Retrieve the document chunks with the most word overlap."""

    if top_k < 1:
        raise ValueError("top_k must be at least 1.")

    question_terms = tokenize(question)

    if not question_terms:
        return []

    results = []

    for document in load_documents():
        chunks = chunk_text(document["text"])

        for index, chunk in enumerate(chunks, start=1):
            chunk_terms = tokenize(chunk)
            score = len(question_terms & chunk_terms)

            if score > 0:
                results.append({
                    "filename": document["filename"],
                    "chunk_id": index,
                    "score": score,
                    "text": chunk,
                })

    results.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return results[:top_k]


def main():
    documents = load_documents()

    print(f"Documents loaded: {len(documents)}")

    if not documents:
        print(
            "No documents found. Add .txt files to the "
            "documents folder."
        )
        return

    print("\nLOCAL DOCUMENT SEARCH")
    print("Type 'exit' to stop.")

    while True:
        question = input("\nAsk about company policy: ").strip()

        if question.lower() in {"exit", "quit"}:
            break

        results = retrieve_documents(question)

        if not results:
            print("No relevant document passages found.")
            continue

        for result in results:
            print(
                f"\nSource: {result['filename']} "
                f"| Chunk: {result['chunk_id']} "
                f"| Match score: {result['score']}"
            )
            print(result["text"])


if __name__ == "__main__":
    main()
