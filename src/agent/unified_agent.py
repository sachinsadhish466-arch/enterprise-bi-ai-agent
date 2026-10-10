
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

PROJECT_ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(PROJECT_ROOT / "src" / "analytics"))
sys.path.insert(0, str(PROJECT_ROOT / "src" / "rag"))

from metrics import (
    total_business_metrics,
    revenue_by_region,
    revenue_by_product,
    top_customers,
    monthly_revenue,
)
from document_search import retrieve_documents


def search_business_documents(question: str) -> dict:
    """Retrieve relevant passages from business documents."""

    results = retrieve_documents(question, top_k=3)

    return {
        "sources": [
            {
                "filename": item["filename"],
                "chunk_id": item["chunk_id"],
                "text": item["text"],
                "score": item["score"],
            }
            for item in results
        ]
    }


def get_top_customers() -> dict:
    """Return the five highest-ranking customers."""
    return {"customers": top_customers(limit=5)}


def main():
    load_dotenv(PROJECT_ROOT / ".env")

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing from the project .env file."
        )

    client = genai.Client(api_key=api_key)


    approved_tools = [
        total_business_metrics,
        revenue_by_region,
        revenue_by_product,
        get_top_customers,
        monthly_revenue,
        search_business_documents,
    ]


    config = types.GenerateContentConfig(
        system_instruction=(
            "You are an enterprise business intelligence assistant. "
            "Use analytics tools for numerical business questions and "
            "search_business_documents for policy and strategy questions. "
            "You may use both when a question needs both data and policy. "
            "Never invent revenue, profit, customer figures, or policies. "
            "Clearly distinguish measured facts from recommendations. "
            "Use Indian rupees for monetary amounts. "
            "Cite retrieved document filenames when using document evidence."
        ),
        tools=approved_tools,
        temperature=0.2,
    )

    print("=" * 60)
    print("UNIFIED BUSINESS INTELLIGENCE AI AGENT")
    print("SQL Analytics + RAG + Google Gemini")
    print("=" * 60)
    print("Type 'exit' to stop.")

    while True:
        question = input("\nBusiness question: ").strip()

        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        if not question:
            continue

        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=question,
                config=config,
            )

            print("\nBUSINESS ANSWER")
            print("-" * 60)
            print(response.text or "Gemini returned no text.")

        except Exception as error:
            print(f"\nRequest failed: {error}")


if __name__ == "__main__":
    main()
