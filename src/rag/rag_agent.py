
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai

from document_search import retrieve_documents

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL = "gemini-3.8-flash"


def main():
    load_dotenv(PROJECT_ROOT / ".env")

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing from your .env file."
        )

    client = genai.Client(api_key=api_key)

    print("=" * 55)
    print("BUSINESS DOCUMENT RAG AGENT")
    print("Powered by Google Gemini")
    print("=" * 55)
    print("Ask questions about company policies and sales strategy.")
    print("Type 'exit' to stop.")

    while True:
        question = input("\nYour question: ").strip()

        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        if not question:
            continue

        try:
            # Retrieve relevant passages from local documents.
            results = retrieve_documents(question, top_k=3)

            if not results:
                print(
                    "\nNo relevant information found in the documents."
                )
                continue

            # Include source names and retrieved text in the context.
            context = "\n\n".join(
                f"Source: {item['filename']}\n"
                f"Passage: {item['text']}"
                for item in results
            )

            prompt = f"""
You are an enterprise business policy assistant.

Answer using only the supplied document context.
Do not invent policies, numbers, or facts.
If the context does not contain enough information, say so.
Explain the answer clearly and mention the source filenames.

DOCUMENT CONTEXT:
{context}

USER QUESTION:
{question}
"""

            print("\nRetrieved document passages. Asking Gemini...")


            try:
                response = client.models.generate_content(
                    model=MODEL,
                    contents=prompt,
                )

                print("\nRAG ANSWER")
                print("-" * 55)
                print(response.text or "Gemini returned no text.")

            except Exception as api_error:
                print("\nGemini is temporarily unavailable.")
                print(f"Details: {api_error}")
                print("\nRETRIEVED DOCUMENT ANSWER")
                print("-" * 55)
                print("Gemini could not generate a response.")
                print("Here are the relevant passages from your documents:\n")

                for item in results:
                    print(f"Source: {item['filename']}")
                    print(item["text"])
                    print()


            print("\nSOURCES")
            for item in results:
                print(
                    f"- {item['filename']} "
                    f"(chunk {item['chunk_id']}, "
                    f"match score {item['score']})"
                )

        except Exception as error:
            print(f"\nRequest failed: {error}")


if __name__ == "__main__":
    main()
