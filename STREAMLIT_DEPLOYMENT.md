# Streamlit Deployment Guide

Deploy the AI Code Reviewer Streamlit frontend to **Streamlit Cloud** (free) or self-hosted.

## Option 1: Streamlit Cloud (Recommended - Free)

### Prerequisites
- Streamlit Cloud account ([streamlit.io](https://streamlit.io))
- GitHub account with the repository pushed

### Step 1: Push Code to GitHub
Ensure `streamlit_app.py` is committed and pushed to `main`:
```bash
git add streamlit_app.py requirements.txt
git commit -m "feat: add streamlit frontend"
git push origin main
```

### Step 2: Create Streamlit Cloud App
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **Create app**
3. Select **GitHub repository**: `Ayushix17/ai-developer-review`
4. Select **Branch**: `main`
5. Set **Main file path**: `streamlit_app.py`
6. Click **Deploy**

### Step 3: Configure Secrets (Optional but Recommended)
If you want to store sensitive data in Streamlit Cloud:

1. After deployment, click the **»** menu (top right) → **Settings**
2. Go to **Secrets** tab
3. Add your environment variables:
   ```toml
   BACKEND_URL = "https://your-backend-url.railway.app"
   OPENAI_API_KEY = "sk-..."
   GITHUB_TOKEN = "ghp_..."
   ```

### Step 4: Configure Frontend in App
1. Open the deployed app
2. In the sidebar, set **Backend URL** to your deployed FastAPI backend:
   - If using Railway: `https://your-service.railway.app`
   - If using Render: `https://your-service.onrender.com`
   - If local testing: `http://localhost:8000`

### Step 5: Test the App
- Try the **Code Analysis** tab with sample code
- Try **RAG Pipeline** with a GitHub repo
- Submit feedback in the **Feedback** tab

---

## Option 2: Self-Hosted (Docker)

### Prerequisites
- Docker installed
- Docker Hub account (optional, for image hosting)

### Step 1: Create Dockerfile for Streamlit
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY streamlit_app.py .

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Save as `Streamlit.dockerfile` in the repo root.

### Step 2: Build & Run Locally
```bash
docker build -f Streamlit.dockerfile -t ai-reviewer-frontend .
docker run -p 8501:8501 \
  -e BACKEND_URL="http://backend:8000" \
  ai-reviewer-frontend
```

Access at `http://localhost:8501`

### Step 3: Deploy to Cloud
**Render:**
1. Create new Web Service on [render.com](https://render.com)
2. Connect your GitHub repo
3. Set **Build command**: `pip install -r requirements.txt`
4. Set **Start command**: `streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0`
5. Add environment variables
6. Deploy

**Railway:**
1. `railway init` → select the repo
2. Set environment variables:
   ```bash
   railway variables set BACKEND_URL="https://your-backend.railway.app"
   ```
3. `railway up`

---

## Option 3: Docker Compose (Both Services)

Create `docker-compose.yml` at repo root:
```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      OPENAI_API_KEY: "${OPENAI_API_KEY}"
      GITHUB_TOKEN: "${GITHUB_TOKEN}"
    networks:
      - ai-reviewer

  frontend:
    build:
      context: .
      dockerfile: Streamlit.dockerfile
    ports:
      - "8501:8501"
    environment:
      BACKEND_URL: "http://backend:8000"
    depends_on:
      - backend
    networks:
      - ai-reviewer

networks:
  ai-reviewer:
    driver: bridge
```

Run:
```bash
docker-compose up
```

Access:
- Frontend: `http://localhost:8501`
- Backend: `http://localhost:8000`

---

## Configuration

### Backend URL
The Streamlit app connects to FastAPI via the **Backend URL** in the sidebar. Set this to:
- **Local testing**: `http://localhost:8000`
- **Railway**: `https://your-service-name.railway.app`
- **Render**: `https://your-service-name.onrender.com`
- **AWS EC2**: `http://your-ec2-ip:8000`

### Environment Variables
If using Streamlit Cloud secrets, they're automatically available in the app. Otherwise, create a `.streamlit/secrets.toml`:
```toml
backend_url = "https://your-backend.railway.app"
openai_api_key = "sk-..."
```

---

## Troubleshooting

### "Cannot connect to backend"
- Verify backend is running and accessible
- Check Backend URL in sidebar
- Ensure CORS is enabled on backend (it is in the FastAPI app)

### Streamlit Cloud slow
- Use free tier for development
- Upgrade to Streamlit+ for production
- Use CDN for static assets

### Secrets not loading
- In Streamlit Cloud: go to Settings → Secrets
- Check `.streamlit/secrets.toml` for local development
- Reload the app after changing secrets

---

## Next Steps

1. ✅ Backend deployed on Railway/Render
2. ✅ Streamlit frontend deployed on Streamlit Cloud
3. Configure GitHub webhook (optional for auto-deployment)
4. Monitor logs and usage
5. Add custom domain (Streamlit+)

**You now have a full-stack AI Code Reviewer app!** 🚀
