# API Documentation

## Base URL
```
http://localhost:8000  (local)
https://your-domain.com  (production)
```

## Authentication

Most endpoints don't require authentication. For protected endpoints, use:

```
Authorization: Bearer <api-key>
```

## Endpoints

### Health Check

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "AI Developer Review API",
  "phase": "1-6"
}
```

---

### Analyze Code (Core Endpoint)

```http
POST /analyze
Content-Type: application/json
```

**Request:**
```json
{
  "diffs": [
    {
      "file_name": "main.py",
      "file_path": "src/main.py",
      "language": "python",
      "old_code": "def hello():\n    print('hi')",
      "new_code": "def hello():\n    print('world')",
      "diff_content": "- print('hi')\n+ print('world')"
    }
  ],
  "repository_context": "# Project README\n## Coding Standards\n- Use type hints\n- Follow PEP-8",
  "pr_title": "Update greeting message",
  "pr_description": "Changes hello message to world",
  "include_ast_analysis": true,
  "include_rag": true,
  "use_expensive_model": false
}
```

**Response:**
```json
[
  {
    "file_name": "main.py",
    "reviews": [
      {
        "line_number": 2,
        "severity": "INFO",
        "type": "llm",
        "title": "Consider f-string",
        "description": "Use f-strings for better readability",
        "suggestion": "print(f'Hello {name}')",
        "code_snippet": "print('world')"
      },
      {
        "line_number": 1,
        "severity": "WARN",
        "type": "ast",
        "title": "Missing type hints",
        "description": "Function missing return type annotation",
        "suggestion": "def hello() -> None:",
        "code_snippet": "def hello():"
      }
    ],
    "summary": "Found 2 issues (1 AST, 1 LLM)",
    "tokens_used": 245,
    "cost": 0.003,
    "latency_ms": 1234
  }
]
```

**Parameters:**
- `diffs` (required): List of code changes to analyze
  - `file_name`: Name of the file
  - `file_path`: Full path to the file
  - `language`: Programming language (python, javascript, typescript, java, etc.)
  - `old_code`: Original code (optional)
  - `new_code`: New/modified code
  - `diff_content`: Git diff format (optional)

- `repository_context` (optional): README, coding standards, project docs
- `pr_title` (optional): Pull request title
- `pr_description` (optional): Pull request description
- `include_ast_analysis` (default: true): Enable static analysis
- `include_rag` (default: true): Enable context retrieval
- `use_expensive_model` (default: false): Use expensive model (GPT-4) vs cheap (GPT-3.5)

**Response Fields:**
- `reviews`: List of code review findings
  - `line_number`: Line number in code
  - `severity`: BLOCKER, WARN, INFO
  - `type`: "ast" (static analysis) or "llm" (AI analysis)
  - `title`: Issue title
  - `description`: Detailed explanation
  - `suggestion`: Proposed fix
  - `code_snippet`: Affected code

- `summary`: Overall summary
- `tokens_used`: LLM tokens used
- `cost`: Cost in USD
- `latency_ms`: Response time

---

### GitHub Webhook

```http
POST /webhook/github
Content-Type: application/json
X-GitHub-Event: pull_request
X-Hub-Signature: sha256=...
```

**Payload:**
GitHub sends standard PR event payload. Backend automatically:
1. Fetches PR files
2. Runs analysis
3. Posts review comments

**Response:**
```json
{
  "status": "processing",
  "pr_number": 123
}
```

---

### Metrics

```http
GET /metrics
```

**Response:**
```json
{
  "total_requests": 42,
  "total_tokens": 10250,
  "total_cost": 0.125,
  "avg_latency_ms": 1567,
  "recent_metrics": [
    {
      "timestamp": "2024-01-20T10:30:00",
      "pr_number": 123,
      "tokens_used": 245,
      "cost": 0.003,
      "latency_ms": 1234
    }
  ]
}
```

---

### Status

```http
GET /status
```

**Response:**
```json
{
  "service": "AI Developer Review API",
  "version": "1.0.0",
  "phase": "1-6",
  "endpoints": {
    "analyze": "/analyze",
    "github_webhook": "/webhook/github",
    "metrics": "/metrics",
    "health": "/health"
  },
  "models": {
    "primary": "gpt-4-turbo",
    "fallback": "gpt-3.5-turbo"
  },
  "features": {
    "phase_1_llm": true,
    "phase_2_github": true,
    "phase_3_rag": true,
    "phase_4_ast": true,
    "phase_6_cost_tracking": true
  }
}
```

---

## Error Handling

All errors return JSON with status code:

```json
{
  "detail": "Error message"
}
```

**Common Status Codes:**
- `200`: Success
- `400`: Bad request (invalid parameters)
- `401`: Unauthorized
- `422`: Validation error
- `500`: Server error (LLM timeout, etc.)

---

## Rate Limiting

Currently no rate limiting. For production, add:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 99
X-RateLimit-Reset: 1705760400
```

---

## Examples

### Analyze Python Code

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "diffs": [{
      "file_name": "main.py",
      "file_path": "main.py",
      "language": "python",
      "new_code": "import os\n\ndef greet(name):\n    print(f\"Hello {name}\")"
    }]
  }'
```

### Analyze with Context

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "diffs": [{
      "file_name": "api.py",
      "file_path": "src/api.py",
      "language": "python",
      "new_code": "from fastapi import FastAPI\napp = FastAPI()"
    }],
    "repository_context": "# Project: AI Code Reviewer\n## Standards\n- Use type hints\n- Async first\n- Test coverage >80%",
    "pr_title": "Add FastAPI setup"
  }'
```

### Get Metrics

```bash
curl http://localhost:8000/metrics | jq
```

---

## Integration Examples

### Python Client

```python
import requests

API_URL = "http://localhost:8000"

def analyze_code(code: str, language: str = "python"):
    response = requests.post(
        f"{API_URL}/analyze",
        json={
            "diffs": [{
                "file_name": "code.py",
                "file_path": "code.py",
                "language": language,
                "new_code": code
            }]
        }
    )
    return response.json()

# Usage
results = analyze_code("def hello(): print('world')")
for result in results:
    for review in result['reviews']:
        print(f"{review['severity']}: {review['title']}")
```

### JavaScript Client

```javascript
const API_URL = "http://localhost:8000";

async function analyzeCode(code, language = "javascript") {
  const response = await fetch(`${API_URL}/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      diffs: [{
        file_name: "code.js",
        file_path: "code.js",
        language,
        new_code: code
      }]
    })
  });
  return response.json();
}

// Usage
const results = await analyzeCode("console.log('hello')");
results.forEach(result => {
  result.reviews.forEach(review => {
    console.log(`${review.severity}: ${review.title}`);
  });
});
```

---

## Support

For issues, questions, or feature requests, create an issue on GitHub.
