# AI Developer Review

Minimal MVP for AI-assisted code review.

## What Is In This Repo

- `backend/`: FastAPI backend with code analysis and history APIs
- `frontend/`: Streamlit UI for submitting code and reviewing saved analyses
- `docs/`: concise MVP architecture, API, development, and deployment notes

## MVP Features

- Analyze pasted code with:
  - Python static checks
  - LLM-backed review via OpenAI
- Persist analyses and findings in SQLite by default
- Browse analysis history in the UI
- Local Docker setup for backend + frontend

## Quick Start

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend: `http://localhost:8000`

### Frontend

From the repository root:

```bash
streamlit run frontend/streamlit_app.py
```

Frontend: `http://localhost:8501`

## Required Environment

If you want LLM review enabled, set:

```bash
OPENAI_API_KEY=your_key_here
```

If `OPENAI_API_KEY` is not set, the backend still returns static-analysis findings.

## Main Endpoints

- `GET /health`
- `POST /analyze`
- `POST /webhook/github`
- `GET /analyses`
- `GET /analyses/{analysis_id}`

## Deployment

The repo includes a `render.yaml` blueprint for Render with:

- FastAPI backend
- Streamlit frontend
- managed PostgreSQL database

You still need to set `OPENAI_API_KEY` before the app can do LLM-backed reviews.
