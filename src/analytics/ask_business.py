
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

from metrics import (
    total_business_metrics,
    revenue_by_region,
    revenue_by_product,
    top_customers,
    monthly_revenue,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL = "gemini-3.8-flash"


def main():
    load_dotenv(PROJECT_ROOT / ".env")

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY is missing. Check your project .env file."
        )

    client = genai.Client(api_key=api_key)

    # Only expose approved, read-only analytics functions.
    approved_tools = [
        total_business_metrics,
        revenue_by_region,
        revenue_by_product,
        top_customers,
        monthly_revenue,
    ]

    config = types.GenerateContentConfig(
        system_instruction=(
            "You are an enterprise business intelligence analyst. "
            "Use the provided analytics functions to obtain actual "
            "business numbers. Never invent metrics. Explain results "
            "clearly and use Indian rupees for monetary values. "
            "Distinguish measured facts from possible explanations."
        ),
        tools=approved_tools,
        temperature=0.2,
    )

    print("=" * 55)
    print("ENTERPRISE BUSINESS INTELLIGENCE AI")
    print("Powered by Google Gemini")
    print("=" * 55)

    while True:
        question = input(
            "\nAsk a business question (or type 'exit'): "
        ).strip()

        if question.lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        if not question:
            continue

        try:
            print("\nAnalyzing your business question...")

            response = client.models.generate_content(
                model=MODEL,
                contents=question,
                config=config,
            )

            print("\nAI BUSINESS ANSWER")
            print("-" * 55)
            print(response.text or "The model returned no text.")

        except Exception as error:
            print(f"\nRequest failed: {error}")


if __name__ == "__main__":
    main()
