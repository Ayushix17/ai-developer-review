# AI Developer Review

Minimal AI-assisted code review product built as a Vercel service split:

- `frontend/`: Next.js app router UI
- `backend/`: FastAPI review API and GitHub webhook handler
- `docs/`: architecture, API, development, and deployment notes

## What it does

- Paste code and run a review
- Combine deterministic static checks with optional OpenAI-backed review
- Save analyses and findings
- Inspect history and stored source
- Accept GitHub PR webhooks and post one summary comment

## Local development

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

For local frontend development without Vercel services, set:

```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

## Vercel deployment

The repo includes a `vercel.json` services config:

- `web` -> `frontend/`
- `api` -> `backend/main.py`

Before deploying, set these environment variables in Vercel:

- `DATABASE_URL`
- `OPENAI_API_KEY`
- `GITHUB_TOKEN`
- `GITHUB_WEBHOOK_SECRET`

## Main endpoints

- `GET /health`
- `POST /analyze`
- `GET /analyses`
- `GET /analyses/{analysis_id}`
- `POST /webhook/github`
