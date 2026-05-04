# Deployment

## Local

### Backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
pip install -r requirements.txt
streamlit run frontend/streamlit_app.py
```

## Docker

```bash
docker compose up --build
```

Backend: `http://localhost:8000`
Frontend: `http://localhost:8501`

## Render

The repo includes a `render.yaml` blueprint that creates:

- a FastAPI backend service
- a Streamlit frontend service
- a managed PostgreSQL database

Set these environment variables during blueprint creation:

- `OPENAI_API_KEY`
- `GITHUB_TOKEN` if you want GitHub PR ingestion
- `GITHUB_WEBHOOK_SECRET` if you want webhook verification

Render injects the backend connection string into `DATABASE_URL` and the frontend backend address into `BACKEND_HOSTPORT`.
