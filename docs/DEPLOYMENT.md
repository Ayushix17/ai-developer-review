# Deployment Guide

## Phase 1: Local Development

### Prerequisites
- Python 3.10+
- Node.js 16+
- Git
- Docker (optional)

### Setup

```bash
# Clone repository
git clone https://github.com/yourusername/ai-code-reviewer.git
cd "Major Project(8th Semester)"

# Backend setup
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit with your API keys
nano .env

# Run backend
uvicorn app.main:app --reload
```

Backend will be available at `http://localhost:8000`

### API Testing

```bash
# Health check
curl http://localhost:8000/health

# Analyze code
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "diffs": [{
      "file_name": "test.py",
      "file_path": "test.py",
      "language": "python",
      "new_code": "def hello():\n    print(\"world\")"
    }]
  }'
```

## Phase 2: Docker Deployment

### Build and Run

```bash
# Build image
docker build -t ai-reviewer-backend ./backend

# Run container
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -e GITHUB_TOKEN=$GITHUB_TOKEN \
  ai-reviewer-backend
```

### Docker Compose

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down
```

## Phase 3: Cloud Deployment

### Render.com

1. **Create Render account**: https://render.com

2. **Connect GitHub repository**:
   - New → Web Service
   - Select repository
   - Select branch

3. **Configure**:
   - Name: `ai-reviewer-backend`
   - Runtime: Python 3.11
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

4. **Set environment variables**:
   ```
   OPENAI_API_KEY=<your-key>
   GITHUB_TOKEN=<your-token>
   LLM_PROVIDER=openai
   ```

5. **Deploy**: Push to repository, Render auto-deploys

**Cost**: ~$7/month for basic tier

### Railway.app

1. **Install Railway CLI**:
   ```bash
   npm i -g @railway/cli
   ```

2. **Login**:
   ```bash
   railway login
   ```

3. **Create project**:
   ```bash
   railway init
   ```

4. **Add environment variables**:
   ```bash
   railway variables set OPENAI_API_KEY=<key>
   railway variables set GITHUB_TOKEN=<token>
   ```

5. **Deploy**:
   ```bash
   railway up
   ```

### AWS EC2

1. **Launch EC2 instance**:
   ```bash
   # Amazon Linux 2
   # t3.micro (free tier eligible)
   ```

2. **SSH into instance**:
   ```bash
   ssh -i your-key.pem ec2-user@your-instance-ip
   ```

3. **Install dependencies**:
   ```bash
   sudo yum update
   sudo yum install python3 python3-pip docker git
   
   # Start Docker
   sudo systemctl start docker
   sudo usermod -a -G docker ec2-user
   ```

4. **Clone and run**:
   ```bash
   git clone https://github.com/yourusername/ai-code-reviewer.git
   cd ai-code-reviewer/backend
   
   # Create .env with API keys
   
   # Build and run
   docker build -t ai-reviewer .
   docker run -p 80:8000 \
     -e OPENAI_API_KEY=$OPENAI_API_KEY \
     -e GITHUB_TOKEN=$GITHUB_TOKEN \
     ai-reviewer
   ```

5. **Setup reverse proxy (Nginx)**:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

## Phase 4: GitHub Actions CI/CD

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Render

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Render
        run: |
          curl -X POST https://api.render.com/deploy/srv-${{ secrets.RENDER_SERVICE_ID }}?key=${{ secrets.RENDER_API_KEY }}
```

## Phase 5: Database Setup

### PostgreSQL

```bash
# Install PostgreSQL
docker run -d \
  --name postgres \
  -e POSTGRES_USER=developer \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=ai_reviews \
  -p 5432:5432 \
  postgres:15

# Connect
psql -h localhost -U developer -d ai_reviews

# Create tables
CREATE TABLE pr_metadata (
  id SERIAL PRIMARY KEY,
  pr_number INT,
  repository VARCHAR(255),
  title VARCHAR(255),
  author VARCHAR(255),
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

CREATE TABLE metrics (
  id SERIAL PRIMARY KEY,
  pr_number INT,
  tokens_used INT,
  cost DECIMAL(10, 4),
  latency_ms INT,
  created_at TIMESTAMP
);

CREATE TABLE feedback (
  id SERIAL PRIMARY KEY,
  pr_number INT,
  comment_id INT,
  feedback VARCHAR(20),
  created_at TIMESTAMP
);
```

## Phase 6: GitHub Webhook Setup

1. **Go to repository settings** → Webhooks

2. **Add webhook**:
   - Payload URL: `https://your-domain.com/webhook/github`
   - Content type: `application/json`
   - Events: `Pull requests`
   - Secret: Generate random string, set `GITHUB_WEBHOOK_SECRET`

3. **Test webhook**:
   - GitHub will send test payload
   - Check backend logs for receipt

## Phase 7: VS Code Extension

### Local Testing

```bash
cd vscode-extension
npm install
npm run compile

# Press F5 to debug in VS Code
```

### Publish to Marketplace

```bash
# Create publisher account
vsce create-publisher <name>

# Package extension
vsce package

# Publish
vsce publish
```

## Monitoring

### Render Dashboard
- View logs
- Monitor response times
- Set up alerts

### Railway Dashboard
- Real-time metrics
- Usage statistics
- Cost tracking

### Local Metrics
```bash
curl http://localhost:8000/metrics
```

Returns: token usage, cost, latency stats

## Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.10+

# Check dependencies
pip list | grep fastapi

# Run with verbose
uvicorn app.main:app --reload --log-level debug
```

### GitHub webhook not triggering
- Verify webhook URL is correct
- Check GitHub Webhook delivery logs
- Verify `GITHUB_WEBHOOK_SECRET` matches

### High latency
- Check LLM provider response times
- Verify network connectivity
- Scale backend (horizontal)

### Out of budget
- Switch to cheaper model (gpt-3.5-turbo)
- Reduce context window
- Enable AST-only mode

## Cost Estimates (Monthly)

| Service | Free | Paid |
|---------|------|------|
| Render | - | $7 |
| Railway | $5 | $15+ |
| AWS EC2 | Yes | $10+ |
| OpenAI API | - | $20-100 |
| PostgreSQL | - | $10-20 |
| **Total** | **Free** | **$50-150** |
