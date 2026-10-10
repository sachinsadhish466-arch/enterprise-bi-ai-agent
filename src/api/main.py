
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
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
    business_metrics_by_date,
)
from document_search import retrieve_documents

load_dotenv(PROJECT_ROOT / ".env")

app = FastAPI(
    title="Enterprise Business Intelligence AI",
    description="Business analytics and document-search API",
    version="1.1.0",
)

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None


class QuestionRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=1000,
        description="Your business question",
    )


def get_top_customers() -> dict:
    """Return the five highest-ranking customers."""
    return {"customers": top_customers(limit=5)}


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


TOOLS = [
    total_business_metrics,
    revenue_by_region,
    revenue_by_product,
    get_top_customers,
    monthly_revenue,
    search_business_documents,
]

CONFIG = types.GenerateContentConfig(
    system_instruction=(
        "You are an enterprise business intelligence assistant. "
        "Use analytics tools for numerical questions and document search "
        "for policy questions. Use both when appropriate. "
        "Never invent metrics or policies. "
        "Clearly distinguish measured facts from recommendations. "
        "Use Indian rupees for monetary amounts and cite document filenames."
    ),
    tools=TOOLS,
    temperature=0.2,
)


@app.get("/")
def home():
    """Return API status and documentation location."""
    return {
        "message": "Enterprise Business Intelligence API is running",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    """Check API status and Gemini configuration."""
    return {
        "status": "healthy",
        "gemini_configured": client is not None,
    }


@app.get("/metrics/date-range")
def get_metrics_by_date(
    start_date: str = Query(
        ...,
        description="Start date in YYYY-MM-DD format",
        examples=["2026-01-01"],
    ),
    end_date: str = Query(
        ...,
        description="End date in YYYY-MM-DD format",
        examples=["2026-12-31"],
    ),
):
    """Return order, customer, revenue, and profit metrics for a date range."""
    try:
        return business_metrics_by_date(start_date, end_date)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@app.post("/ask")
def ask_business_question(request: QuestionRequest):
    """Answer business questions using Gemini and available tools."""
    if client is None:
        raise HTTPException(
            status_code=503,
            detail="Gemini API key is not configured.",
        )

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=422,
            detail="Question cannot be empty.",
        )

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=question,
            config=CONFIG,
        )

        return {
            "question": question,
            "answer": response.text or "No text response was returned.",
        }

    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=f"Business AI request failed: {error}",
        ) from error
