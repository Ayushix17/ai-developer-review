# Development

## Current contract

The frontend is a client UI that speaks to the FastAPI backend over `GET /health`, `POST /analyze`, and the history endpoints.

## Recommended order

1. Run the backend locally on port 8000
2. Run the frontend locally with `NEXT_PUBLIC_API_BASE_URL=http://localhost:8000`
3. Verify analysis, history, and webhook behavior
4. Deploy through Vercel Services
