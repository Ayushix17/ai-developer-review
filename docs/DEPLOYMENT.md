# Deployment

## Local

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
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000 npm run dev
```

## Vercel

The repo is configured as a Vercel Services project with:

- `frontend/` as the web service
- `backend/main.py` as the API service
- `routePrefix: "/api"` for the backend

Required environment variables:

- `DATABASE_URL`
- `OPENAI_API_KEY`
- `GITHUB_TOKEN` if GitHub PR ingestion is enabled
- `GITHUB_WEBHOOK_SECRET` if webhook verification is enabled

For local work outside Vercel, set `NEXT_PUBLIC_API_BASE_URL=http://localhost:8000` so the frontend can reach the backend service directly.
