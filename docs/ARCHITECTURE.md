# Architecture & System Design

## System Overview

This AI-powered developer productivity tool combines multiple technologies to provide intelligent code review and analysis:

```
┌─────────────────────────────────────────────────────────────┐
│                    Development Tools Layer                  │
├──────────────────────────────────┬──────────────────────────┤
│   VS Code Extension (Phase 7)    │   GitHub Interface (P2)  │
│   - Inline suggestions           │   - Webhook triggers     │
│   - Quick actions                │   - PR comments          │
│   - Code snippet analysis        │   - Review API           │
└──────────────────────────────────┴──────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────────┐
│              API & Integration Layer (Phase 1-2)             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │  FastAPI Server                                         ││
│  │  - /analyze endpoint (code diffs)                       ││
│  │  - /webhook/github (PR events)                          ││
│  │  - /metrics (cost tracking)                             ││
│  └─────────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────────┐
│              Analysis & Processing Layer                     │
├──────────────────────┬──────────────┬───────────────────────┤
│ LLM Module (P1)      │ RAG Pipeline │ AST Analyzer (P4)     │
│ - OpenAI/Claude/     │ (Phase 3)    │ - Python AST          │
│   Local models       │ - Embedding  │ - Tree-sitter         │
│ - Cost tracking      │ - Retrieval  │ - Pattern detection   │
│ - Model fallback     │ - Context    │ - Unused imports      │
│                      │   injection  │ - Complexity metrics  │
├──────────────────────┴──────────────┴───────────────────────┤
│              Hybrid Analysis Results                         │
│  - Deterministic findings (AST)                             │
│  - AI suggestions (LLM)                                     │
│  - Context-aware insights (RAG)                             │
└──────────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────────┐
│                 Output & Feedback Layer                      │
├──────────────────────┬──────────────┬───────────────────────┤
│ Inline Comments      │ Cost Tracking│ Feedback Loop (P8)    │
│ (Phase 5)            │ (Phase 6)    │ - User ratings        │
│ - GitHub API         │ - Tokens     │ - False positives     │
│ - Severity labels    │ - Latency    │ - Accuracy metrics    │
│ - Fix suggestions    │ - Budget     │ - Quality reports     │
│ - Grouping           │   limits     │                       │
└──────────────────────┴──────────────┴───────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────────┐
│              Data & Persistence Layer                        │
├──────────────────────────────────────────────────────────────┤
│  PostgreSQL Database   │  FAISS/Chroma Vector Store         │
│  - PR metadata         │  - Repository embeddings           │
│  - Review history      │  - Semantic search cache           │
│  - Metrics & feedback  │  - Context retrieval               │
│  - User preferences    │  - Performance optimization        │
└──────────────────────────────────────────────────────────────┘
```

## Data Flow

### Code Analysis Flow (Phase 1-4, 6)

```
1. User submits code (VS Code extension or GitHub PR)
   ↓
2. Backend receives code diff
   ├─ Phase 1: Send to LLM for analysis
   ├─ Phase 3: Retrieve relevant repository context (RAG)
   ├─ Phase 4: Run AST analysis for static findings
   └─ Phase 6: Track tokens, latency, cost
   ↓
3. Combine results
   ├─ AST findings (deterministic)
   ├─ LLM suggestions (AI-powered)
   └─ Context insights (repository-aware)
   ↓
4. Output
   ├─ Return JSON with reviews + metrics
   └─ Phase 5: Post to GitHub (if PR context)
   ↓
5. Phase 8: Collect feedback for evaluation
```

### GitHub Integration Flow (Phase 2, 5)

```
1. PR opened/updated on GitHub
   ↓
2. Webhook triggers backend
   ├─ Fetch PR files via GitHub API
   ├─ Extract diffs
   └─ Store PR metadata (Phase 2)
   ↓
3. Run analysis (Phase 1-4)
   ↓
4. Post review comments (Phase 5)
   ├─ Inline comments on changed lines
   ├─ Add severity labels
   └─ Group similar issues
   ↓
5. GitHub notification sent to reviewer
```

## Component Details

### LLM Module (Phase 1)
- **Purpose**: Provide intelligent code suggestions
- **Supported Models**: GPT-4, Claude 3, Local (Ollama)
- **Features**:
  - Provider abstraction (swap between OpenAI/Anthropic/Local)
  - Fallback model for cost optimization
  - Context-aware prompting
  - Cost calculation per request

### RAG Pipeline (Phase 3)
- **Purpose**: Inject repository context into analysis
- **Components**:
  - Sentence Transformers for embeddings
  - FAISS for efficient similarity search
  - Chroma for persistent vector storage
- **Workflow**:
  1. Embed entire repository (startup)
  2. For each PR, retrieve top-K relevant files
  3. Inject into LLM prompt
  4. Reduce hallucination and improve accuracy

### AST Analyzer (Phase 4)
- **Purpose**: Deterministic code analysis
- **Capabilities**:
  - Python AST parsing
  - JavaScript/TypeScript basic analysis
  - Detections:
    - Unused imports
    - Deep nesting (>3 levels)
    - Syntax errors
    - Debug statements
- **Benefits**:
  - No LLM cost
  - 100% accurate for patterns
  - Instant results

### Cost Tracking (Phase 6)
- **Tracks**:
  - Tokens per request
  - Response latency
  - Cost by model
  - Budget utilization
- **Features**:
  - Model fallback when budget exceeded
  - Cost alerts
  - Metrics dashboard
  - Historical analysis

## Technology Choices

| Component | Tech | Why |
|-----------|------|-----|
| Backend API | FastAPI | Fast, async, auto-docs |
| LLM | OpenAI/Claude | SOTA models, reliable |
| Embeddings | Sentence-Transformers | Fast, high-quality |
| Vector DB | FAISS | Open, efficient, fast |
| Code Parsing | Python AST + tree-sitter | Language support |
| GitHub | REST API + Webhooks | Reliable, well-documented |
| VS Code | TS + VS Code API | Native extension |
| Deployment | Docker + Render/Railway | Portable, scalable |

## Scaling Considerations

### Phase 1-5 (MVP)
- Single-server deployment
- In-memory metrics
- PostgreSQL for PR metadata
- FAISS for embeddings

### Phase 6-7
- Cost tracking across requests
- Model fallback mechanism
- Extension distribution

### Phase 8-9 (Enterprise)
- Multi-agent orchestration (LangGraph)
- Distributed processing
- Real-time monitoring
- Advanced caching

## Phase 9: Multi-Agent Orchestration (Enterprise)

Phase 9 introduces a distributed multi-agent architecture where specialized
agents collaborate to enhance review quality, optimize code, and enforce
operational constraints.  The orchestrator (see `app/multi_agent/orchestrator.py`)
serves as the central coordinator, dispatching tasks and aggregating results.

### Agent Roles

- **Reviewer Agent** – produces initial code reviews combining LLM+AST+RAG
- **Critic Agent** – evaluates reviewer output for false positives or gaps
- **Optimizer Agent** – suggests performance improvements or refactorings
- **CostGuard Agent** – monitors token usage, triggers model fallback
- **FeedbackCollector Agent** – ingests Phase 8 feedback to retrain models

Agents communicate over a lightweight message bus (for MVP, in-memory; later
Redis/Kafka).  This architecture supports horizontal scaling and easy
integration of new capabilities (e.g. security scanner, test generator).

A simplified data flow for Phase 9:

```
Client submits task → Orchestrator → Reviewer → Critic → Optimizer
                                ↑            ↓
                         CostGuard monitors usage
                                ↓
                       FeedbackCollector updates models
```

Phase 9 is optional and intended for enterprise deployments.  It provides a
framework for future expansion beyond simple LLM analysis.

## Security

- GitHub OAuth for authentication
- API key management (env variables)
- Rate limiting on endpoints
- CORS configuration
- Input validation on all endpoints

## Performance

- Average latency: <5s per PR
- Token efficiency: <4000 tokens per analysis
- Cost per PR: <$0.10
- Parallel processing (async)
