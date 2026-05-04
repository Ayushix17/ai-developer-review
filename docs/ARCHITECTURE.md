# Architecture

## MVP shape

```text
Streamlit UI -> FastAPI API -> Static analysis + OpenAI review -> SQLite/Postgres
```

## Backend modules

- `routes/health.py`: liveness endpoint
- `routes/analyze.py`: review endpoint
- `routes/github.py`: GitHub webhook endpoint
- `routes/history.py`: saved analysis retrieval
- `services/static_analysis.py`: deterministic Python checks
- `services/llm.py`: optional OpenAI review
- `services/persistence.py`: analysis and finding storage

## Scope boundaries

This MVP intentionally excludes:

- GitHub webhook automation
- VS Code extension runtime integration
- RAG/embeddings
- billing
- team accounts
