# 🚀 Phase 1: Backend MVP Launch Guide

**Status**: 🟢 READY TO START  
**Phase Duration**: 2-3 hours  
**Difficulty**: Beginner-Friendly (Framework pre-built)

---

## 🎯 Phase 1 Objectives

### What You'll Complete
1. ✅ Verify backend runs locally
2. ✅ Test all 5 API endpoints
3. ✅ Integrate LLM (OpenAI/Claude/Ollama)
4. ✅ Test code analysis (LLM + AST)
5. ✅ Verify cost tracking works
6. ✅ Deploy to cloud (Render or Railway)

### Deployable Milestone
**A public API endpoint that analyzes code and returns AI suggestions with cost tracking**

---

## 📋 Phase 1 Checklist

- [ ] Backend dependencies installed
- [ ] .env configured with API keys
- [ ] Local server running
- [ ] All 5 endpoints tested
- [ ] LLM integration working
- [ ] AST analysis verified
- [ ] Cost tracking functional
- [ ] Deployed to cloud
- [ ] Public endpoint tested

---

## 🏃 Quick Start (20 Minutes)

### Step 1: Install Dependencies (5 min)

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install
pip install -r requirements.txt
```

### Step 2: Configure Environment (3 min)

```bash
# Copy template
cp .env.example .env

# Edit .env - add your keys:
# OPENAI_API_KEY=sk-your-key-here
# GITHUB_TOKEN=ghp-your-token-here (optional for now)
```

**Get OpenAI Key**: https://platform.openai.com/api-keys

### Step 3: Start Server (2 min)

```bash
uvicorn app.main:app --reload
```

Expected output:
```
INFO:     Application startup complete
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Step 4: Test API (5 min)

Open in browser: **http://localhost:8000/docs**

You'll see interactive Swagger UI. Try:
1. GET `/health` → Should return `{"status": "healthy"}`
2. POST `/analyze` → Send sample code, get review

---

## 🧪 Testing Each Endpoint

### 1. Health Check (Verify running)
```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "service": "AI Developer Review API",
  "phase": "1-6"
}
```

### 2. Analyze Code (Core feature)
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "diffs": [{
      "file_name": "example.py",
      "file_path": "example.py",
      "language": "python",
      "new_code": "import os\ndef hello():\n    print(\"world\")"
    }],
    "include_ast_analysis": true
  }'
```

Expected response:
```json
[
  {
    "file_name": "example.py",
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
    "tokens_used": 0,
    "cost": 0.0,
    "latency_ms": 123
  }
]
```

### 3. View Metrics (Cost tracking)
```bash
curl http://localhost:8000/metrics
```

Response shows:
- total_requests
- total_tokens
- total_cost
- avg_latency_ms

### 4. Service Status
```bash
curl http://localhost:8000/status
```

Shows enabled features and models

### 5. Interactive Docs
Browser: **http://localhost:8000/docs**
- Try any endpoint
- See schema
- Get examples

---

## 🧠 Understanding the Code

### API Structure
```
app/main.py
├── Request/Response Models (Pydantic)
├── FastAPI instance
├── /analyze endpoint (POST)
│   ├── Parse request
│   ├── Run LLM analysis (if key provided)
│   ├── Run AST analysis
│   ├── Combine results
│   └── Return JSON response
├── /webhook/github endpoint
├── /health endpoint
├── /metrics endpoint
└── /status endpoint
```

### LLM Integration Flow
```
User sends code
    ↓
LLMClient.analyze_code()
    ├─ Build prompt with context
    ├─ Call OpenAI/Claude/Ollama
    ├─ Parse JSON response
    ├─ Calculate cost & tokens
    └─ Return structured data
```

### Code Analysis Flow
```
User sends code
    ↓
ASTAnalyzer.analyze()
    ├─ Parse Python AST
    ├─ Check unused imports
    ├─ Detect nesting depth
    ├─ Catch syntax errors
    └─ Return issues list
```

---

## 🔑 Key Configuration

### .env Variables (Phase 1)

```bash
# LLM Provider (choose one)
LLM_PROVIDER=openai              # or 'anthropic' or 'local'
LLM_MODEL=gpt-3.5-turbo          # Cheaper than gpt-4
LLM_FALLBACK_MODEL=gpt-3.5-turbo

# API Keys
OPENAI_API_KEY=sk-...             # Required for GPT
ANTHROPIC_API_KEY=sk-ant-...      # For Claude
LOCAL_MODEL_URL=http://localhost:11434  # For Ollama

# Cost Control
MAX_TOKENS_PER_REQUEST=4000
MAX_COST_PER_PR=1.0

# Features
ENABLE_PHASE_1_LLM=true
ENABLE_PHASE_4_AST=true
ENABLE_PHASE_6_COST_TRACKING=true
DEBUG=true
```

### Model Costs (per 1K tokens)

| Model | Input | Output | Cost/PR |
|-------|-------|--------|---------|
| gpt-3.5-turbo | $0.0005 | $0.0015 | ~$0.002 |
| gpt-4-turbo | $0.03 | $0.06 | ~$0.04 |
| Claude 3 | $3/M | $15/M | ~$0.01 |
| Local (Ollama) | FREE | FREE | $0 |

**Recommendation**: Start with gpt-3.5-turbo (cheapest), upgrade to gpt-4-turbo once working.

---

## 🔧 Troubleshooting Phase 1

### "ModuleNotFoundError: No module named 'openai'"
```bash
# Inside backend folder, with venv activated:
pip install -r requirements.txt
```

### "OPENAI_API_KEY not set"
```bash
# Edit backend/.env
OPENAI_API_KEY=sk-your-actual-key

# Restart server
# Press Ctrl+C to stop
# Run: uvicorn app.main:app --reload
```

### "Port 8000 already in use"
```bash
# Try different port
uvicorn app.main:app --reload --port 8001
```

### "API returns empty reviews"
```bash
# Check if LLM key is set
curl http://localhost:8000/status

# Should show:
# "ENABLE_PHASE_1_LLM": true
# Model should be set

# Add OPENAI_API_KEY to .env
```

### "AST analysis not working"
```bash
# Should work without any key
# Check /status shows:
# "ENABLE_PHASE_4_AST": true

# Try with Python code:
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"diffs": [{"file_name": "test.py", "file_path": "test.py", "language": "python", "new_code": "import unused\nprint(\"hi\")"}]}'
```

---

## 📊 Test Cases

### Test 1: Python Code with Unused Import
```python
import os
import sys

def greet():
    print("Hello")
```

Expected: AST finds unused `os` and `sys`

### Test 2: Deep Nesting
```python
def outer():
    if True:
        if True:
            if True:
                if True:
                    print("deep")
```

Expected: AST warns about deep nesting (>3 levels)

### Test 3: Syntax Error
```python
def broken(
    print("missing closing paren")
```

Expected: AST catches syntax error

### Test 4: With LLM (need OpenAI key)
```python
def calculate(a, b):
    return a + b
```

Expected: LLM suggests improvements

### Test 5: JavaScript
```javascript
let unused = 5;
console.log("hello");
```

Expected: AST finds unused variable and console.log

---

## 🚀 Deploy to Cloud (Phase 1 Extension)

Once working locally, deploy in 5-20 minutes:

### Option 1: Render.com (Recommended)
1. Push code to GitHub
2. Go to https://render.com
3. New Web Service
4. Select repository
5. Config:
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
6. Add env vars: OPENAI_API_KEY, etc.
7. Deploy!

**Cost**: ~$7/month

### Option 2: Railway.app
```bash
npm i -g @railway/cli
railway login
railway init
railway variables set OPENAI_API_KEY=$YOUR_KEY
railway up
```

**Cost**: ~$5-15/month

### Option 3: Docker Locally
```bash
docker build -t ai-reviewer ./backend
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  ai-reviewer
```

### Option 4: Docker Compose (Full Stack)
```bash
docker-compose up -d
```

Starts:
- Backend API (port 8000)
- PostgreSQL (port 5432)
- Ollama (port 11434)

---

## 📈 Success Metrics for Phase 1

- [x] Backend starts without errors
- [x] `/health` returns 200 OK
- [x] `/analyze` accepts code and returns JSON
- [x] AST analysis finds issues
- [x] LLM analysis works (with API key)
- [x] Cost tracking functional
- [x] Metrics endpoint works
- [x] API deployed to cloud (optional)

---

## 📚 Reference

### API Endpoints
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/analyze` | POST | **Core**: Analyze code |
| `/health` | GET | Health check |
| `/metrics` | GET | Cost & latency tracking |
| `/status` | GET | Service info |
| `/webhook/github` | POST | GitHub webhooks (Phase 2) |

### Important Files
- `app/main.py` - FastAPI app
- `app/llm/client.py` - LLM client
- `app/ast_analyzer/parser.py` - Code analyzer
- `requirements.txt` - Dependencies
- `.env` - Configuration

### Useful Commands
```bash
# Start server
uvicorn app.main:app --reload

# Test endpoint
curl http://localhost:8000/health

# View logs
# Check terminal output

# Stop server
# Ctrl+C

# Deactivate venv
deactivate

# View API docs
# http://localhost:8000/docs
```

---

## 🎯 Next Phase After Completing Phase 1

Once Phase 1 is working:
1. You have a public API
2. You can analyze code
3. You can track costs
4. You're ready for Phase 2: GitHub Integration

### Phase 2 Preview
- Set up GitHub webhook
- Fetch PR diffs automatically
- Trigger analysis on PR events
- Store results in database

**Estimated time**: 1-2 hours

---

## 💡 Tips for Success

1. **Start Simple**
   - Test AST first (no API key needed)
   - Add LLM after confirming AST works

2. **Use Interactive Docs**
   - Go to http://localhost:8000/docs
   - Try endpoints there
   - See request/response schemas

3. **Monitor Costs**
   - Check `/metrics` endpoint
   - Keep track of tokens used
   - Stay within budget

4. **Read Errors Carefully**
   - Terminal shows detailed error messages
   - Search error message online
   - Check .env configuration

5. **Keep API Key Safe**
   - Never commit .env to git
   - Use environment variables
   - Regenerate keys if exposed

---

## 🎉 You're Ready!

Everything is set up. Just:

1. **Install**: `pip install -r requirements.txt`
2. **Configure**: Add API key to `.env`
3. **Run**: `uvicorn app.main:app --reload`
4. **Test**: `curl http://localhost:8000/health`
5. **Explore**: `http://localhost:8000/docs`

**Time to working API**: 15 minutes ⏱️

**Questions?** Check [GETTING_STARTED.md](./GETTING_STARTED.md) or [docs/API.md](./docs/API.md)

---

**Ready? Let's build.** 🚀

Start with: `cd backend && pip install -r requirements.txt`
