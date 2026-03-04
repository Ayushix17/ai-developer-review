# Deployment Checklist

This checklist guides you through full end-to-end deployment of the AI Developer Review project.

## 1. Prepare Repository
- [ ] Ensure code is pushed to GitHub (`Ayushix17/ai-developer-review`).
- [ ] Confirm all branches are merged to `main`.
- [ ] Add `RENDER_DEPLOY_HOOK` (if using Render) or similar webhook secret.

## 2. Local Environment (Optional)
- [ ] Clone repository:
  ```bash
  git clone https://github.com/Ayushix17/ai-developer-review.git
  cd "Major Project(8th Semester)"
  ```
- [ ] Backend setup:
  ```bash
  # note: backend is where code lives
  cd backend
  python -m venv venv
  # activate venv
  venv\Scripts\activate  # Windows
  # or `source venv/bin/activate` on macOS/Linux
  pip install -r ../requirements.txt
  cp .env.example .env
  # edit .env with API keys
  ```
- [ ] Start server:
  ```bash
  uvicorn app.main:app --reload
  ```
- [ ] Verify health and analyze endpoints.

## 3. Docker Deployment
- [ ] Build image: `docker build -t ai-reviewer-backend ./backend`
- [ ] Run container:
  ```bash
  docker run -p 8000:8000 \
    -e OPENAI_API_KEY=$OPENAI_API_KEY \
    -e GITHUB_TOKEN=$GITHUB_TOKEN \
    ai-reviewer-backend
  ```
- [ ] Or use `docker-compose up -d`.

## 4. Cloud Hosting Options
### Render (Recommended)
- [ ] Create Render account and connect GitHub repo.
- [ ] Add environment variables (OPENAI_API_KEY, GITHUB_TOKEN, etc.).
- [ ] Set build command (`cd backend && pip install -r ../requirements.txt`).
- [ ] Set start command (`cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000`).
- [ ] Add `RENDER_DEPLOY_HOOK` secret in GitHub.
- [ ] Deploy and check health endpoint.

### Railway
- [ ] Install `railway` CLI and login.
- [ ] `railway init` in repo.
- [ ] Set environment variables with `railway variables set`.
- [ ] `railway up` to deploy.

### AWS EC2
- [ ] Launch t3.micro instance, install Docker.
- [ ] Clone repo, build/run inside Docker.
- [ ] (Optional) configure Nginx reverse proxy.

### Streamlit Cloud Frontend (Optional)
- [ ] Create Streamlit Cloud account at [share.streamlit.io](https://share.streamlit.io).
- [ ] Deploy `streamlit_app.py` to Streamlit Cloud (free).
- [ ] Configure Backend URL in app settings (point to deployed FastAPI backend).
- [ ] Test code analysis, RAG, and feedback features.
- [ ] (Optional) Add Streamlit Cloud secrets for sensitive variables.

## 5. CI/CD Pipeline
- [ ] Ensure `.github/workflows/deploy.yml` exists with build/test/deploy steps.
- [ ] Enable GitHub Actions in repo settings.
- [ ] Add necessary secrets (RENDER_DEPLOY_HOOK, etc.).
- [ ] Push to `main` to trigger pipeline.

## 6. Post-Deployment
- [ ] Test endpoints on live URL (`/health`, `/analyze`).
- [ ] Configure VS Code extension to point to deployed backend.
- [ ] Monitor logs (Render/Railway dashboard).
- [ ] Add additional environment variables as needed (LLM_PROVIDER, phase flags).

## 7. Optional Enhancements
- [ ] Set up DNS/custom domain.
- [ ] Enable HTTPS/SSL if not handled by provider.
- [ ] Configure autoscaling/quota checks.

---

Keep this checklist updated as the project evolves.