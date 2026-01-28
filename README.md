# AI-Powered Developer Productivity Tool

> An enterprise-grade AI system that reviews pull requests with context-aware reasoning, hybrid static analysis, and real-time developer feedback via VS Code extension.

## 🎯 Vision

Transform code review workflows by combining:
- **Context-Aware AI Reviews** — RAG-powered suggestions using repository knowledge
- **Static Analysis** — AST-based pattern detection (unused imports, complexity)
- **Inline Feedback** — GitHub Review API with severity labels
- **Developer Integration** — VS Code extension for code snippet analysis
- **Cost Intelligence** — Token tracking, model fallback, budget awareness
- **Measurable Quality** — Feedback loop, false positive tracking, quality reports

## ✨ Key Features

### Phase 1-5: PR Reviewer (MVP)
- ✅ FastAPI backend with `/analyze` endpoint
- ✅ LLM integration (OpenAI/Claude/Local models)
- ✅ GitHub OAuth + webhook triggers
- ✅ RAG pipeline with FAISS embeddings
- ✅ AST-based static analysis
- ✅ Inline PR comments with severity labels
- ✅ Cost & latency tracking

### Phase 7: VS Code Extension
- ✅ Authentication & backend connection
- ✅ Send selected code for analysis
- ✅ Display suggestions inline
- ✅ Quick actions (Explain / Improve / Fix)

### Phase 9: Enterprise Multi-Agent System
- ✅ Reviewer agent (code quality)
- ✅ Critic agent (edge cases)
- ✅ Optimizer agent (performance)
- ✅ Cost-guard agent (budget enforcement)
- ✅ LangGraph orchestration

## 🏗️ Architecture

See [PROJECT_PLAN.md](./PROJECT_PLAN.md) for detailed system architecture and phase breakdown.

**Tech Stack:**
- **Backend**: FastAPI (Python), PostgreSQL, FAISS/Chroma
- **Frontend**: VS Code Extension (TypeScript)
- **LLM**: OpenAI/Claude/Ollama
- **Deployment**: Docker, Render/Railway/EC2
- **CI/CD**: GitHub Actions

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- Git
- GitHub account + API token
- LLM API key (OpenAI/Claude)

### Backend Setup (Phase 1)
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### VS Code Extension Setup (Phase 7)
```bash
cd vscode-extension
npm install
npm run compile
# Press F5 to debug
```

## 📋 Deployment Checklist

### Minimum (Strong for Jobs) — Phases 0-5
- [ ] Phase 0: Planning & architecture
- [ ] Phase 1: FastAPI backend + Docker
- [ ] Phase 2: GitHub OAuth + webhooks
- [ ] Phase 3: RAG embeddings pipeline
- [ ] Phase 4: AST static analysis
- [ ] Phase 5: Inline PR comments

**Result**: Fully functional AI PR reviewer ready for GitHub integration

### Ideal (Top 5%) — Phases 0-7
- [ ] All phases 0-5
- [ ] Phase 6: Cost & latency tracking
- [ ] Phase 7: VS Code extension

**Result**: Production-ready tool with developer integration

### Elite (Startup Ready) — All Phases
- [ ] All phases 0-7
- [ ] Phase 8: Evaluation & feedback loop
- [ ] Phase 9: Multi-agent system with LangGraph

**Result**: Enterprise-grade system ready for scale

## 📊 Success Metrics

| Metric | Target |
|--------|--------|
| Review Accuracy | >85% useful suggestions |
| Latency | <5s per PR file |
| Cost per Review | <$0.10 |
| False Positives | <15% |
| User Adoption | >50% engagement |

## 🔗 Project Structure

```
.
├── backend/                    # FastAPI + LLM backend
│   ├── app/
│   │   ├── main.py            # FastAPI app
│   │   ├── analyze.py         # /analyze endpoint
│   │   ├── llm/               # LLM integration
│   │   ├── rag/               # RAG pipeline
│   │   ├── ast_analyzer/      # Static analysis
│   │   ├── github_api/        # GitHub integration
│   │   └── db/                # Database models
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
├── vscode-extension/          # TypeScript VS Code extension
│   ├── src/
│   │   ├── extension.ts       # Extension entry
│   │   ├── auth.ts            # OAuth flow
│   │   ├── client.ts          # Backend client
│   │   └── ui/                # Inline suggestions UI
│   ├── package.json
│   └── README.md
├── docs/                      # Documentation
│   ├── ARCHITECTURE.md
│   ├── API.md
│   └── DEVELOPMENT.md
├── PROJECT_PLAN.md            # Detailed phase breakdown
└── README.md                  # This file
```

## 🧠 How This Looks to Recruiters

✅ **Clear System Evolution** — 9 distinct phases, each deployable
✅ **Real Deployments** — Docker, cloud platforms, GitHub Actions
✅ **Production Mindset** — Cost tracking, latency monitoring, feedback loops
✅ **Developer Empathy** — VS Code integration, inline feedback, semantic search
✅ **AI + Engineering Depth** — RAG, AST analysis, multi-agent orchestration

## 📚 Learning Resources

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [VS Code Extension API](https://code.visualstudio.com/api)
- [GitHub REST API](https://docs.github.com/en/rest)
- [LangChain Documentation](https://python.langchain.com/)
- [FAISS GitHub](https://github.com/facebookresearch/faiss)

## 🤝 Contributing

See [CONTRIBUTING.md](./docs/CONTRIBUTING.md) for development guidelines.

## 📄 License

MIT License — See LICENSE file for details

## 🎯 Next Steps

1. **Phase 0**: ✅ Architecture & planning complete
2. **Phase 1**: Set up FastAPI backend with LLM integration
3. **Phase 2**: Integrate GitHub OAuth & webhooks
4. **Phase 3**: Implement RAG pipeline
5. Continue through phases 4-9 as needed

---

**Status**: Phase 0 Planning Complete ✅ | Ready for Phase 1 Backend MVP

For detailed phase breakdown, see [PROJECT_PLAN.md](./PROJECT_PLAN.md)
