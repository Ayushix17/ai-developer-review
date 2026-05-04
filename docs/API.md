# API

## Base URLs

- Local backend: `http://localhost:8000`
- Vercel production backend: `/api`

## `GET /health`

```json
{ "status": "ok" }
```

## `POST /analyze`

Request:

```json
{
  "code": "import os\nprint('debug')",
  "language": "python",
  "source_type": "pasted_code",
  "context": "Use production-safe logging"
}
```

Response:

```json
{
  "analysis_id": 12,
  "summary": "Found 2 issue(s): 1 static, 1 AI.",
  "findings": [],
  "tokens_used": 180,
  "latency_ms": 950,
  "cost_usd": 0.0018
}
```

## `GET /analyses`

Returns saved analysis summaries ordered by newest first.

## `GET /analyses/{analysis_id}`

Returns one saved analysis with stored findings and original code.

## `POST /webhook/github`

Consumes GitHub `pull_request` webhook events, fetches changed files, stores an analysis, and posts one summary comment back to the PR.
