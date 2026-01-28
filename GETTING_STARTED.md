# Getting Started Guide

## 🎯 Phase 0 Complete! ✅

**Status**: Project planning, architecture, and initial scaffolding complete.

You now have:
- ✅ Complete project structure (mono-repo)
- ✅ FastAPI backend scaffolding (Phase 1-6)
- ✅ VS Code extension setup (Phase 7 ready)
- ✅ Full documentation
- ✅ Docker & deployment configs
- ✅ API specifications

**Time to read this guide**: 10 minutes  
**Time to have a working API**: 20 minutes  
**Time to add GitHub integration**: 1-2 hours

---

## 🚀 Next Steps

### Step 1: Setup Backend (15 minutes)

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Add your API keys to .env
# Edit with your favorite editor:
#   OPENAI_API_KEY=sk-...
#   GITHUB_TOKEN=ghp-...
```

### Step 2: Run Backend (5 minutes)

```bash
# Make sure you're in backend/ and venv is activated

# Start development server
uvicorn app.main:app --reload

# You should see:
# INFO:     Application startup complete
# Go to http://localhost:8000
```

### Step 3: Test the API (5 minutes)

```bash
# In a new terminal, test the health endpoint
curl http://localhost:8000/health

# Response should be:
# {"status":"healthy","service":"AI Developer Review API","phase":"1-6"}

# Now test the analyze endpoint
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "diffs": [{
      "file_name": "example.py",
      "file_path": "example.py",
      "language": "python",
      "new_code": "def hello():\n    print(\"world\")"
    }]
  }'
```

### Step 4: View API Docs (2 minutes)

Go to **http://localhost:8000/docs** in your browser

You'll see interactive Swagger UI to test all endpoints!

---

## 📋 Understanding the Codebase

### Key Files You Should Know

| File | Purpose | Phase |
|------|---------|-------|
| `app/main.py` | FastAPI app, endpoints | 1-6 |
| `app/llm/client.py` | LLM integration (OpenAI, Claude, Ollama) | 1 |
| `app/ast_analyzer/parser.py` | Static code analysis | 4 |
| `app/rag/retriever.py` | Context retrieval (RAG) | 3 |
| `app/github_api/handler.py` | GitHub webhook handler | 2 |
| `app/db/models.py` | Database models | 2, 6, 8 |

### Quick Overview

1. **User sends code** → Endpoint receives it in `/analyze`
2. **Run analysis** → LLM (Phase 1) + AST (Phase 4) + RAG (Phase 3)
3. **Return results** → JSON with reviews + cost + latency

---

## 🔧 Configuration

### Environment Variables

Edit `backend/.env`:

```
# Required
OPENAI_API_KEY=sk-your-openai-key-here
LLM_PROVIDER=openai  # or 'anthropic' or 'local'

# Optional
GITHUB_TOKEN=ghp-your-github-token
GITHUB_CLIENT_ID=your-oauth-id
GITHUB_CLIENT_SECRET=your-oauth-secret

# Cost Control
MAX_TOKENS_PER_REQUEST=4000
MAX_COST_PER_PR=1.0

# Features
ENABLE_PHASE_1_LLM=true
ENABLE_PHASE_3_RAG=true
ENABLE_PHASE_4_AST=true
ENABLE_PHASE_6_COST_TRACKING=true
```

### Models

We support:
- **OpenAI**: GPT-4, GPT-3.5-turbo (cheapest)
- **Anthropic**: Claude 3 Sonnet
- **Local**: Ollama (free, self-hosted)

Try cheap model first:
```
LLM_MODEL=gpt-3.5-turbo
```

---

## 🧪 Quick Test

### Analyze Python Code

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "diffs": [{
      "file_name": "test.py",
      "file_path": "src/test.py",
      "language": "python",
      "new_code": "import os\n\ndef greet(name):\n    print(f\"Hello {name}\")"
    }],
    "pr_title": "Add greeting function",
    "include_ast_analysis": true
  }'
```

### Expected Response

```json
[
  {
    "file_name": "test.py",
    "reviews": [
      {
        "line_number": 1,
        "severity": "WARN",
        "type": "ast",
        "title": "Unused import",
        "description": "Import 'os' is never used"
      }
    ],
    "summary": "Found 1 issue (1 AST, 0 LLM)",
    "tokens_used": 150,
    "cost": 0.002,
    "latency_ms": 1234
  }
]
```

---

## 📊 Phases & Features

### Phase 1: FastAPI Backend ✅ READY
- Create `/analyze` endpoint
- LLM integration (OpenAI/Claude/Local)
- Cost tracking
- Async processing

**Try it now**: `curl http://localhost:8000/analyze`

### Phase 2: GitHub Integration (1-2 hours)
- Set up GitHub OAuth
- Webhook for PR events
- Fetch PR diffs
- Store metadata

**Do this when ready**: Add GitHub token to `.env` and setup webhook in GitHub settings

### Phase 3: RAG Pipeline (2-3 hours)
- Embed repository files
- Retrieve relevant context
- Inject into LLM prompt
- Reduce hallucination

**Do this when ready**: Install sentence-transformers, setup FAISS

### Phase 4: AST Analysis ✅ READY
- Python AST parsing
- Detect unused imports
- Find complexity issues
- No LLM cost

**Already implemented**: See `app/ast_analyzer/parser.py`

### Phase 5: Inline Comments (2-3 hours)
- Post review comments on GitHub
- Add severity labels
- Group similar issues

**Do this after Phase 2**: Use GitHub Review API

### Phase 6: Cost Tracking ✅ READY
- Track tokens per request
- Calculate cost
- Set budget limits
- Model fallback

**Already implemented**: See `/metrics` endpoint

### Phase 7: VS Code Extension (4-6 hours)
- Scaffold TypeScript extension
- Send code snippets to backend
- Show inline suggestions

**Start when ready**: `cd vscode-extension && npm install`

### Phase 8: Evaluation & Feedback (2-3 hours)
- Collect user feedback
- Track accuracy
- Generate reports

**Phase 9**: Multi-agent system (optional, enterprise)

---

## 🐳 Docker Deployment

### Run Everything with Docker Compose

```bash
# Make sure Docker is running
docker-compose up -d

# Check if running
docker ps

# View logs
docker-compose logs -f backend

# Stop everything
docker-compose down
```

Services:
- Backend API: http://localhost:8000
- PostgreSQL: localhost:5432
- Ollama (local LLM): http://localhost:11434

---

## 📈 Metrics & Monitoring

### Check Metrics

```bash
curl http://localhost:8000/metrics

# Response:
# {
#   "total_requests": 0,
#   "total_tokens": 0,
#   "total_cost": 0.0,
#   "avg_latency_ms": 0,
#   "recent_metrics": []
# }
```

### View API Status

```bash
curl http://localhost:8000/status

# Shows enabled features and models
```

---

## 🚀 Deploy to Cloud (20 minutes)

### Render.com (Recommended for beginners)

1. Push code to GitHub
2. Go to [render.com](https://render.com)
3. Create New → Web Service
4. Select GitHub repository
5. Configure:
   ```
   Build: pip install -r requirements.txt
   Start: uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```
6. Add environment variables (OPENAI_API_KEY, etc.)
7. Click Deploy!

Your API is live at: `https://your-service-name.onrender.com`

Cost: ~$7/month

### Railway.app (Also easy)

```bash
npm i -g @railway/cli
railway login
railway init
railway variables set OPENAI_API_KEY=$YOUR_KEY
railway up
```

Cost: ~$5/month (free tier available)

---

## 🆘 Troubleshooting

### Backend won't start

```bash
# Check Python version (need 3.10+)
python --version

# Check dependencies installed
pip list | grep fastapi

# Run with debug
uvicorn app.main:app --reload --log-level debug
```

### API returns errors

Check logs:
```bash
# Terminal where server is running shows live logs
# Look for ERROR messages
```

### High cost

Use cheaper model:
```
LLM_MODEL=gpt-3.5-turbo
```

Or enable AST-only:
```
ENABLE_PHASE_1_LLM=false
ENABLE_PHASE_4_AST=true
```

### API too slow

1. Use faster model (gpt-3.5-turbo)
2. Reduce RAG context size
3. Disable RAG: `ENABLE_PHASE_3_RAG=false`

---

## 📚 Next Phases

After backend is working:

1. **Integrate GitHub** (Phase 2)
   - Get GitHub token from settings
   - Setup OAuth app
   - Create webhook

2. **Add RAG** (Phase 3)
   - Install embeddings model
   - Create vector store
   - Embed your repo

3. **Post PR Comments** (Phase 5)
   - Integrate GitHub Review API
   - Format suggestions
   - Post to PRs

4. **Build Extension** (Phase 7)
   - Setup VS Code extension
   - Connect to backend
   - Show inline suggestions

See [PROJECT_PLAN.md](./PROJECT_PLAN.md) for detailed phase breakdown.

---

## 📖 Documentation

- **[Architecture](./docs/ARCHITECTURE.md)** - System design & data flow
- **[API Docs](./docs/API.md)** - All endpoints & examples
- **[Deployment](./docs/DEPLOYMENT.md)** - Cloud deployment steps
- **[Development](./docs/DEVELOPMENT.md)** - Dev workflow & contributing

---

## 💡 Pro Tips

1. **Start with cheap model** to learn:
   ```
   LLM_MODEL=gpt-3.5-turbo
   ```

2. **Test locally first**:
   ```bash
   uvicorn app.main:app --reload
   # Then curl http://localhost:8000
   ```

3. **Use `--log-level debug`** for troubleshooting:
   ```bash
   uvicorn app.main:app --reload --log-level debug
   ```

4. **Keep `.env` out of git**:
   ```bash
   echo ".env" >> .gitignore
   git rm --cached backend/.env
   ```

5. **Monitor costs** with `/metrics`:
   ```bash
   curl http://localhost:8000/metrics | jq
   ```

---

## 🎯 Success Criteria

✅ **Phase 1 Complete** when:
- [ ] Backend starts without errors
- [ ] `/health` returns 200
- [ ] `/analyze` returns reviews for code
- [ ] Cost tracking works (`/metrics`)

✅ **All Phases** when:
- [ ] GitHub integration posts PR comments
- [ ] VS Code extension shows suggestions
- [ ] Cost per review < $0.10
- [ ] Latency < 5 seconds
- [ ] Feedback collected for evaluation

---

**You're all set! Start the backend and begin building.** 🚀

Questions? Check the docs or create an issue on GitHub.
