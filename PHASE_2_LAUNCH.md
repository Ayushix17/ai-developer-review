# 🚀 Phase 2: GitHub Integration - Launch Guide

**Status**: 🟢 READY TO START  
**Phase Duration**: 2-3 hours  
**Difficulty**: Intermediate (GitHub OAuth + webhooks)

---

## 🎯 Phase 2 Objectives

### What You'll Complete
1. ✅ Create GitHub OAuth Application
2. ✅ Setup GitHub webhook handler
3. ✅ Automatic PR detection and analysis
4. ✅ Store PR metadata in database
5. ✅ Trigger background analysis on PR events
6. ✅ Test with real GitHub repo

### Deployable Milestone
**Your API automatically analyzes PRs when they're created/updated**

---

## 📋 Phase 2 Checklist

- [ ] Create GitHub OAuth App
- [ ] Get Client ID & Client Secret
- [ ] Configure webhook in repository
- [ ] Test webhook connection
- [ ] Verify PR analysis triggers
- [ ] Store PR metadata in database
- [ ] Test with real PR

---

## 🏃 Quick Start (30 minutes)

### Step 1: Create GitHub OAuth App

1. Go to: https://github.com/settings/developers
2. Click **"New GitHub App"** (or OAuth App → New OAuth App)
3. Fill in:
   - **App Name**: `AI Developer Review`
   - **Homepage URL**: `http://localhost:8000`
   - **Webhook URL**: `http://localhost:8000/webhook/github`
   - **Webhook Secret**: (generate a random string, e.g., `abc123xyz789`)
4. Select Permissions:
   - **Pull Requests**: Read & Write
   - **Issues**: Read & Write
   - **Contents**: Read-only
5. Create App → Get **Client ID** and **Client Secret**

---

### Step 2: Configure Backend

Add to `backend/.env`:
```bash
GITHUB_TOKEN=ghp_your-token-here
GITHUB_CLIENT_ID=your-client-id
GITHUB_CLIENT_SECRET=your-client-secret
GITHUB_WEBHOOK_SECRET=your-webhook-secret
```

**Get GitHub Token**:
1. Go: https://github.com/settings/tokens
2. Click "Generate new token"
3. Select scopes: `repo`, `read:user`, `user:email`
4. Copy token

---

### Step 3: Setup Webhook in Repository

1. Go to your GitHub repo
2. Settings → Webhooks → Add webhook
3. Configure:
   - **Payload URL**: `http://localhost:8000/webhook/github`
   - **Content type**: `application/json`
   - **Secret**: (same as GITHUB_WEBHOOK_SECRET)
   - **Events**: Select "Pull requests"
4. Add webhook

**For local testing**: Use ngrok to expose localhost
```bash
ngrok http 8000
# Get URL like: https://abc123.ngrok.io
# Use: https://abc123.ngrok.io/webhook/github in webhook setup
```

---

### Step 4: Test with Real PR

1. Create a test branch:
   ```bash
   git checkout -b test-feature
   # Make some code changes
   git push origin test-feature
   ```

2. Open Pull Request on GitHub

3. Check server logs for webhook trigger

4. Verify analysis completed

---

## 🧪 What Happens in Phase 2

### Flow Diagram
```
GitHub PR Created
    ↓
GitHub sends webhook to /webhook/github
    ↓
Backend extracts PR info
    ↓
Spawns background analysis task
    ↓
Fetches PR diff
    ↓
Runs AST + LLM analysis
    ↓
Posts review as PR comment
    ↓
Stores metadata in database
    ↓
✅ Complete!
```

---

## 📁 Files Created/Modified in Phase 2

### New Files
- `backend/app/github_integration/` (already scaffolded)
  - `oauth.py` - OAuth token handling
  - `pr_analyzer.py` - PR analysis orchestration
  - `comment_formatter.py` - Format reviews as GitHub comments

### Modified Files
- `backend/app/main.py` - Update `/webhook/github` endpoint
- `backend/.env` - Add GitHub credentials
- `backend/app/db/pr_store.py` - Already has PR storage

---

## 🔌 Key Endpoints

### POST /webhook/github
**What it does**: Receives GitHub webhook events

**Triggered by**: 
- PR opened
- PR updated (new commits)
- PR synchronized

**Payload**:
```json
{
  "action": "opened",
  "pull_request": {
    "number": 123,
    "title": "Add new feature",
    "user": { "login": "username" },
    "head": { "sha": "abc123" },
    "base": { "sha": "def456" }
  }
}
```

**Response**:
```json
{
  "status": "processing",
  "pr_number": 123,
  "analysis_id": "uuid"
}
```

---

## 💾 Database Schema (Phase 2)

### PR Metadata Table
```python
{
  "pr_id": 123,
  "repo": "Ayushix17/ai-developer-review",
  "branch": "feature-branch",
  "author": "username",
  "title": "Add new feature",
  "created_at": "2026-01-29T10:00:00Z",
  "analysis_results": [...],
  "status": "completed"
}
```

---

## 🧠 Implementation Steps

### 1. Update GitHub Handler (main.py)
```python
@app.post("/webhook/github")
async def github_webhook(request: dict, background_tasks: BackgroundTasks):
    # Verify webhook signature
    # Extract PR info
    # Queue background analysis
    # Return status
```

### 2. GitHub API Client
```python
class GitHubAPIClient:
    def get_pr_diff(pr_number, repo)
    def get_pr_files(pr_number, repo)
    def post_review(pr_number, repo, review_body)
```

### 3. PR Analysis Orchestrator
```python
async def analyze_pr(pr_number, repo):
    # Get diff
    # Run analysis
    # Format review
    # Post comment
    # Store metadata
```

---

## 🔐 Security Checklist

- [ ] Verify webhook signature (HMAC-SHA256)
- [ ] Validate GitHub token
- [ ] Rate limit API calls
- [ ] Sanitize user input
- [ ] Don't expose secrets in logs
- [ ] Use OAuth for future app installation

---

## 🐛 Troubleshooting Phase 2

### "Webhook not triggering"
- Check webhook URL is accessible
- Verify GitHub can reach your server
- Check webhook secret is correct
- Use ngrok for local testing

### "Analysis doesn't complete"
- Check background task logs
- Verify API keys are set
- Check database connection
- Review error logs

### "PR comment not posted"
- Verify GitHub token has `write:pull_request` scope
- Check repo permissions
- Verify token not expired

---

## 📊 Phase 2 Success Criteria

- [ ] GitHub OAuth app created
- [ ] Webhook configured
- [ ] /webhook/github endpoint receives events
- [ ] Background task spawns
- [ ] Analysis completes
- [ ] Review posted as PR comment
- [ ] PR metadata stored in database
- [ ] Cost tracked for each PR analysis

---

## 🎯 Phase 2 Deliverables

### Working
- ✅ Automatic PR detection
- ✅ Background analysis
- ✅ GitHub API integration
- ✅ PR comment posting
- ✅ Metadata storage
- ✅ Cost per PR tracking

### Visible Results
- Comments on PRs with AI reviews (Phase 5 now active)
- Analysis metrics stored
- Cost dashboard updated per PR

---

## 📈 Next Phase After Phase 2

**Phase 3: RAG Pipeline**
- Embed repository code
- Build knowledge base
- Improve review quality with context
- Estimated: 2 hours

> **Note:** Phase 5 (inline PR comments) is already wired up – webhooks now trigger analysis and post comments on opened/synchronized PRs.

---

## 💡 Tips for Success

1. **Use ngrok for local testing**
   ```bash
   ngrok http 8000
   # Use ngrok URL in webhook
   ```

2. **Test webhook manually**
   ```bash
   curl -X POST http://localhost:8000/webhook/github \
     -H "Content-Type: application/json" \
     -d '{"action": "opened", "pull_request": {...}}'
   ```

3. **Monitor logs**
   - Watch server logs for webhook events
   - Check background task completion
   - Verify database writes

4. **Start simple**
   - Test with basic PR
   - Verify analysis triggers
   - Add comment posting
   - Add metadata storage

---

## 🎉 You're Ready!

Everything is set up. Just:

1. **Create GitHub OAuth app** (5 min)
2. **Configure webhook** (5 min)
3. **Update .env** (2 min)
4. **Test with real PR** (5 min)
5. **Verify comment posted** (1 min)

**Time to automated PR analysis**: 20 minutes ⏱️

---

**Ready? Let's add GitHub integration.** 🚀

Start with: Create GitHub OAuth app at https://github.com/settings/developers
