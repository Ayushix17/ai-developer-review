# 🚀 Render Deployment Checklist

## Step 1: GitHub Repository
✅ **Done** – Code committed to main branch with:
- `.github/workflows/deploy.yml` – CI/CD pipeline
- `render.yaml` – Service configuration
- Backend with all phases (RAG, PR analysis, feedback, extension)

## Step 2: Create Render Account
1. Go to https://render.com (free to start)
2. Sign up with GitHub (1 click)

## Step 3: Create Web Service
1. Dashboard → **New** → **Web Service**
2. Connect GitHub repository
3. Select branch: `main`
4. Configure:
   - **Name**: `ai-reviewer-backend`
   - **Runtime**: `Python 3`
   - **Build Command**: Render reads `render.yaml` automatically
   - **Start Command**: Render reads `render.yaml` automatically
   - **Region**: Oregon (US) or your preference

## Step 4: Set Environment Variables
In Render dashboard, go to **Environment**:
```
OPENAI_API_KEY=<your-openai-key>
GITHUB_TOKEN=<your-github-token>
ANTHROPIC_API_KEY=<optional-anthropic-key>
```

Get these from:
- **OpenAI API Key**: https://platform.openai.com/api-keys
- **GitHub Token**: https://github.com/settings/tokens (repo access)

## Step 5: Deploy
- Click **Create Web Service**
- Render automatically deploys on git push to `main`
- Check logs in Render dashboard

## Step 6: Verify Deployment
Once deployed (takes ~2-3 min):
```bash
curl https://<your-service>.onrender.com/health
```

Should return: `{"status":"healthy"}`

## Step 7 (Optional): GitHub Actions Auto-Deploy Hook
To enable automatic deployments on git push:
1. In Render: Settings → **Deploy Hook**
2. Copy the webhook URL
3. In GitHub: Settings → Secrets → **New Secret**
   - Name: `RENDER_DEPLOY_HOOK`
   - Value: Paste Render webhook URL

Now pushes to `main` auto-trigger deployments! 🎉

## Pricing
- **Free Tier**: 750 compute hours/month (~1 service always-on)
- **Paid**: $7+/month for better uptime

---

### Troubleshooting

**Build fails**: Check backend `requirements.txt` – ensure all imports are listed
**Timeout**: Increase build timeout in Render settings
**Env vars not loading**: Restart service after adding them

**Need support?** 
- Render Docs: https://render.com/docs
- VS Code Extension: Configure to point to your live service URL
