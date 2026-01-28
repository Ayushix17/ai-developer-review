# Quick Reference

## 🚀 Start Backend (60 seconds)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env: OPENAI_API_KEY=sk-...
uvicorn app.main:app --reload
```

Then go to: **http://localhost:8000/docs**

## 📋 Common Commands

### Backend
```bash
# Start server
uvicorn app.main:app --reload

# Run tests
pytest

# Format code
black app/

# Lint
flake8 app/

# Install dependencies
pip install -r requirements.txt
```

### Extension
```bash
cd vscode-extension
npm install
npm run compile
npm run watch

# Debug: Press F5 in VS Code
```

### Docker
```bash
# Build image
docker build -t ai-reviewer-backend ./backend

# Run container
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  ai-reviewer-backend

# Compose
docker-compose up -d
docker-compose down
```

## 🔗 Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check |
| `/analyze` | POST | **Core**: Analyze code |
| `/webhook/github` | POST | GitHub PR webhook |
| `/metrics` | GET | Cost & latency stats |
| `/status` | GET | Service info |
| `/docs` | GET | Interactive API docs |

## 📊 Key Files

| File | Lines | Purpose |
|------|-------|---------|
| `app/main.py` | 200+ | FastAPI app & endpoints |
| `app/llm/client.py` | 300+ | LLM integration |
| `app/ast_analyzer/parser.py` | 200+ | Static analysis |
| `app/rag/retriever.py` | 150+ | Context retrieval |
| `app/github_api/handler.py` | 150+ | GitHub integration |
| `docs/ARCHITECTURE.md` | 250+ | System design |
| `docs/API.md` | 300+ | API documentation |

## ⚙️ Configuration

```bash
# Create .env file
cp backend/.env.example backend/.env
```

Key variables:
```
OPENAI_API_KEY=sk-...              # Required for GPT
GITHUB_TOKEN=ghp-...               # For GitHub integration
LLM_PROVIDER=openai                # openai, anthropic, local
ENABLE_PHASE_1_LLM=true            # Enable LLM analysis
ENABLE_PHASE_3_RAG=true            # Enable context retrieval
ENABLE_PHASE_4_AST=true            # Enable static analysis
MAX_TOKENS_PER_REQUEST=4000        # Budget limit
MAX_COST_PER_PR=1.0                # Cost limit per PR
```

## 🧪 Test API

### Health Check
```bash
curl http://localhost:8000/health
```

### Analyze Code
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "diffs": [{
      "file_name": "test.py",
      "file_path": "test.py",
      "language": "python",
      "new_code": "print(\"hello\")"
    }]
  }'
```

### View Metrics
```bash
curl http://localhost:8000/metrics
```

### Interactive Docs
```
http://localhost:8000/docs
```

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'app'` | `cd backend && source venv/bin/activate` |
| `OPENAI_API_KEY not set` | `export OPENAI_API_KEY=sk-...` or edit `.env` |
| Port 8000 already in use | `uvicorn app.main:app --port 8001` |
| Extension not loading | `cd vscode-extension && npm install && npm run compile` |
| GitHub webhook not working | Check webhook logs in GitHub settings |

## 📈 Phases at a Glance

| Phase | Focus | Status |
|-------|-------|--------|
| 0 | Planning | ✅ Done |
| 1 | FastAPI Backend | ✅ Scaffolded |
| 2 | GitHub Integration | ⏳ Next |
| 3 | RAG Pipeline | ⏳ Planned |
| 4 | AST Analysis | ✅ Implemented |
| 5 | PR Comments | ⏳ Planned |
| 6 | Cost Tracking | ✅ Implemented |
| 7 | VS Code Extension | ✅ Scaffolded |
| 8 | Evaluation Loop | ⏳ Planned |
| 9 | Multi-Agent | ⏳ Optional |

## 📚 Read These First

1. [GETTING_STARTED.md](./GETTING_STARTED.md) - 10 min start guide
2. [docs/API.md](./docs/API.md) - API endpoints
3. [docs/ARCHITECTURE.md](./docs/ARCHITECTURE.md) - System design
4. [PHASE_0_SUMMARY.md](./PHASE_0_SUMMARY.md) - What's completed

## 💰 Cost Estimates (Monthly)

| Service | Cost | Notes |
|---------|------|-------|
| Render.com | $7 | Recommended for beginners |
| Railway.app | $5-15 | Free tier available |
| AWS EC2 | $10+ | Self-managed |
| OpenAI API | $20-100 | Usage-based |
| **Total** | **$50-150** | Depends on usage |

## 🎯 Success Checklist

- [ ] Backend starts: `uvicorn app.main:app --reload`
- [ ] Health check works: `curl http://localhost:8000/health`
- [ ] Analyze works: Send code to `/analyze`
- [ ] View docs: Open `http://localhost:8000/docs`
- [ ] Edit `.env` with API key
- [ ] All tests pass: `pytest`
- [ ] Docker builds: `docker build -t ai-reviewer-backend ./backend`

## 🚀 Deploy to Cloud

### Render.com (5 minutes)
1. Push to GitHub
2. Create new Web Service on render.com
3. Select repository
4. Set env vars: `OPENAI_API_KEY`, `GITHUB_TOKEN`
5. Click Deploy!

### Railway.app (5 minutes)
```bash
npm i -g @railway/cli
railway login
railway init
railway variables set OPENAI_API_KEY=$YOUR_KEY
railway up
```

### Local Docker
```bash
docker-compose up -d
# API at http://localhost:8000
```

## 📱 VS Code Extension

```bash
cd vscode-extension
npm install
npm run compile

# Debug: Press F5
# Commands:
# - Ctrl+Shift+L: Analyze code
# - Ctrl+Shift+I: Improve code
```

## 🔑 Important Concepts

- **LLM**: Large Language Model (GPT-4, Claude)
- **RAG**: Retrieval-Augmented Generation (context injection)
- **AST**: Abstract Syntax Tree (code parsing)
- **FAISS**: Fast similarity search (vector DB)
- **Webhook**: GitHub → Backend trigger

## 📞 Need Help?

- **Quick answers**: See GETTING_STARTED.md
- **API questions**: See docs/API.md
- **Architecture questions**: See docs/ARCHITECTURE.md
- **Deployment questions**: See docs/DEPLOYMENT.md
- **Dev workflow**: See docs/DEVELOPMENT.md

---

**Ready?** Start with: `cd backend && pip install -r requirements.txt`
