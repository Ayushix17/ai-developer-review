# Development Guide

## Setup

### Quick Start

```bash
# Clone repo
git clone https://github.com/yourusername/ai-code-reviewer.git
cd "Major Project(8th Semester)"

# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys

# VS Code Extension
cd ../vscode-extension
npm install
npm run compile
```

### Environment Setup

Create `backend/.env`:

```
OPENAI_API_KEY=sk-...
GITHUB_TOKEN=ghp-...
LLM_PROVIDER=openai
```

## Development Workflow

### Backend

```bash
cd backend
source venv/bin/activate

# Run development server
uvicorn app.main:app --reload

# Run tests
pytest

# Format code
black app/

# Lint
flake8 app/
```

### VS Code Extension

```bash
cd vscode-extension

# Install dependencies
npm install

# Build
npm run compile

# Watch mode
npm run watch

# Debug (press F5)
```

### Testing

```bash
# Backend tests
cd backend
pytest tests/

# Extension tests
cd vscode-extension
npm test
```

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app
│   │   ├── llm/
│   │   │   └── client.py        # LLM integration
│   │   ├── rag/
│   │   │   └── retriever.py     # RAG pipeline
│   │   ├── ast_analyzer/
│   │   │   └── parser.py        # Static analysis
│   │   ├── github_api/
│   │   │   └── handler.py       # GitHub integration
│   │   └── db/
│   │       └── models.py        # Database models
│   ├── requirements.txt
│   ├── Dockerfile
│   └── README.md
│
├── vscode-extension/
│   ├── src/
│   │   ├── extension.ts         # Extension entry
│   │   ├── client.ts            # API client
│   │   ├── auth.ts              # OAuth
│   │   └── ui/                  # UI components
│   ├── package.json
│   ├── tsconfig.json
│   └── README.md
│
├── docs/
│   ├── ARCHITECTURE.md          # System design
│   ├── API.md                   # API docs
│   ├── DEPLOYMENT.md            # Deployment guide
│   └── DEVELOPMENT.md           # This file
│
├── docker-compose.yml           # Local dev setup
├── PROJECT_PLAN.md              # Phase breakdown
└── README.md                    # Main readme
```

## Adding Features

### New Backend Endpoint

1. Add function in `app/main.py`:
```python
@app.post("/my-endpoint")
async def my_endpoint(request: MyRequest):
    """Description"""
    return MyResponse(...)
```

2. Define request/response models:
```python
class MyRequest(BaseModel):
    field: str

class MyResponse(BaseModel):
    result: str
```

### New LLM Provider

1. Add to `app/llm/client.py`:
```python
def _call_my_provider(self, prompt: str):
    # Implementation
    return analysis
```

2. Update provider check:
```python
elif self.provider == "my_provider":
    response = self._call_my_provider(prompt)
```

### New AST Analysis Feature

1. Add to `app/ast_analyzer/parser.py`:
```python
def check_security_issues(self, tree):
    # Find security issues
    return issues
```

2. Call in `_analyze_python`:
```python
issues.extend(self._check_security_issues(tree))
```

## Testing

### Unit Tests

```python
# tests/test_llm.py
from app.llm.client import LLMClient

def test_analyze_code():
    client = LLMClient(use_expensive=False)
    response = client.analyze_code(...)
    assert "reviews" in response
```

### Integration Tests

```python
# tests/test_api.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_analyze_endpoint():
    response = client.post("/analyze", json={...})
    assert response.status_code == 200
```

## Debugging

### Backend

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Debug message")
logger.info("Info message")
logger.error("Error message")
```

### VS Code Extension

```bash
# Debug console in VS Code
# Press Ctrl+Shift+Y to view
```

## Performance Tips

1. **Reduce token usage**:
   - Use cheaper model (gpt-3.5-turbo)
   - Limit context window
   - Use AST-only mode for simple checks

2. **Improve latency**:
   - Cache embeddings
   - Parallel processing
   - Model batching

3. **Reduce cost**:
   - Use fallback model for non-critical analysis
   - Set cost limits per PR
   - Batch multiple PRs

## Common Issues

### `ModuleNotFoundError: No module named 'app'`
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### `OPENAI_API_KEY not set`
```bash
cp .env.example .env
# Edit .env with your key
# Restart server
```

### Extension not working
```bash
cd vscode-extension
npm install
npm run compile
# Press F5 to debug
```

## Contributing

1. Create feature branch: `git checkout -b feature/my-feature`
2. Make changes and test
3. Commit: `git commit -am 'Add feature'`
4. Push: `git push origin feature/my-feature`
5. Create Pull Request

## Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [VS Code Extension API](https://code.visualstudio.com/api)
- [LangChain Docs](https://python.langchain.com/)
- [GitHub API](https://docs.github.com/en/rest)
