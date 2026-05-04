# API

## Base URL

```text
http://localhost:8000
```

## `GET /health`

```json
{
  "status": "ok"
}
```

## `POST /analyze`

```json
{
  "code": "import os\nprint('debug')",
  "language": "python",
  "source_type": "pasted_code",
  "context": "Use production-safe logging"
}
```

## `GET /analyses`

Returns saved analysis summaries ordered by newest first.

## `GET /analyses/{analysis_id}`

Returns one saved analysis with stored findings and original code.

## `POST /webhook/github`

Consumes GitHub `pull_request` webhook events, fetches changed files, stores an analysis, and posts one summary comment back to the PR.
