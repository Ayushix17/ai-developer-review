# Architecture

## Vercel service split

```text
Next.js UI -> Vercel /api service -> FastAPI review API -> SQLite/Postgres
```

## Frontend

- Next.js App Router
- Client-side workbench for analysis, history, and settings
- Calls the backend through `/api/*` in production

## Backend modules

- `routes/health.py`: liveness endpoint
- `routes/analyze.py`: review endpoint
- `routes/github.py`: GitHub webhook endpoint
- `routes/history.py`: saved analysis retrieval
- `services/static_analysis.py`: deterministic checks
- `services/llm.py`: optional OpenAI review
- `services/persistence.py`: analysis and finding storage

## Scope boundaries

This MVP intentionally excludes:

- VS Code extension runtime integration
- RAG/embeddings
- billing
- team accounts
- multi-model routing
