
# Enterprise Business Intelligence AI Agent

An AI-powered Business Intelligence application that combines SQL analytics, Retrieval-Augmented Generation (RAG), Google Gemini, FastAPI, and Streamlit to answer business questions using structured data and company documents.

## Features

- **Business analytics:** Revenue, profit, orders, customers, products, and regional performance.
- **SQL analytics:** SQLite database with reusable analytical queries.
- **Document retrieval:** Searches company documents for relevant policies and business strategies.
- **AI-powered answers:** Google Gemini uses approved analytics and document-search tools.
- **Unified business assistant:** Combines numerical business results with relevant policy information.
- **Interactive dashboard:** KPI cards, revenue charts, customer tables, and AI chat.
- **REST API:** FastAPI endpoints with input validation and interactive documentation.
- **Automated tests:** Pytest tests for analytics and API behavior.

## Technology Stack

| Component | Technology |
|---|---|
| Programming language | Python 3.10 |
| Database | SQLite |
| Data analysis | Pandas, SQL |
| AI model | Google Gemini |
| Retrieval | Keyword-based document chunk retrieval |
| Backend | FastAPI, Uvicorn |
| Frontend | Streamlit |
| Visualizations | Plotly |
| Testing | Pytest |
| Configuration | python-dotenv |

## Architecture

```text
User
 |
 v
Streamlit Dashboard
 |
 v
FastAPI Backend
 |
 v
Unified Business Intelligence Agent
 |
 +---------------------+
 |                     |
 v                     v
SQL Analytics      Document Retrieval
 |                     |
 v                     v
SQLite Database    Business Documents
 |                     |
 +----------+----------+
            |
            v
       Google Gemini
            |
            v
      Business Answer
```

## Project Structure

```text
enterprise-bi-ai-agent/
├── data/
│   ├── customers.csv
│   ├── products.csv
│   ├── orders.csv
│   └── business.db
├── documents/
│   └── sales_strategy.txt
├── src/
│   ├── analytics/
│   │   ├── create_database.py
│   │   ├── data_validation.py
│   │   ├── metrics.py
│   │   ├── sql_analysis.py
│   │   ├── ask_business.py
│   │   └── local_agent.py
│   ├── rag/
│   │   ├── document_search.py
│   │   ├── semantic_search.py
│   │   └── rag_agent.py
│   ├── agent/
│   │   └── unified_agent.py
│   ├── api/
│   │   └── main.py
│   └── ui/
│       └── app.py
├── tests/
│   ├── test_metrics.py
│   └── test_api.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Prerequisites

- Python 3.10
- Git
- A Google Gemini API key
- Internet access for Gemini API requests

## Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd enterprise-bi-ai-agent
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure the Gemini API key

Copy the example environment file:

```powershell
Copy-Item .env.example .env
```

Open `.env` and replace the placeholder with your own Google Gemini API key:

```dotenv
GEMINI_API_KEY=your_actual_api_key
```

Never commit your real `.env` file or publish your API key.

### 5. Prepare the database

If the database has not already been created, run:

```powershell
python src/analytics/data_validation.py
python src/analytics/create_database.py
```

## Running the Application

Open two terminals in the project root and activate `.venv` in both.

### Terminal 1: Start FastAPI

```powershell
python -m uvicorn src.api.main:app --reload
```

API documentation:

http://127.0.0.1:8000/docs

Health check:

http://127.0.0.1:8000/health

### Terminal 2: Start Streamlit

```powershell
python -m streamlit run src/ui/app.py
```

Dashboard:

http://localhost:8501

## Example Business Questions

- What is our total revenue and profit?
- Who are our top five customers?
- Which region generates the most revenue?
- What is the discount approval policy?
- Which region generates the most revenue, and what sales strategy applies there?

## API Usage

Endpoint:

`POST /ask`

Example request:

```json
{
  "question": "What is our total revenue and profit?"
}
```

Example response:

```json
{
  "question": "What is our total revenue and profit?",
  "answer": "The answer is generated using the available business analytics."
}
```

The exact answer depends on the current database and Gemini response.

## Running Tests

Run the analytics tests:

```powershell
python -m pytest tests/test_metrics.py -v
```

Run the API tests:

```powershell
python -m pytest tests/test_api.py -v
```

Run the complete test suite:

```powershell
python -m pytest -v
```

The current test suite covers five analytics checks and four API checks. It does not yet test every financial calculation or make live Gemini API calls.

## Current Limitations

- Document retrieval currently uses keyword overlap rather than semantic embeddings.
- The project uses sample business data and sample sales policies.
- Gemini requests require a valid API key and network access.
- Authentication and production deployment configuration still need to be added.
- PySpark, FAISS, LangChain, LangGraph, and Docker are not part of the currently verified end-to-end application.

## Future Enhancements

- Improved semantic document retrieval.
- More comprehensive analytics and API tests.
- Authentication, access controls, and production-grade logging.
- Docker-based deployment.
- Additional analytics using Apache Spark.
- Evaluation of retrieval quality and AI answer accuracy.

## Security

- Store API keys in `.env`.
- Keep `.env`, local databases, and virtual environments out of Git.
- Use only authorized business data.
- Do not expose the development server directly to the public internet.

## License

Add an appropriate license before distributing or reusing this project.
