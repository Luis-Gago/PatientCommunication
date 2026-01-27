# Deployment Guide - Neon + Railway + Vercel

Complete guide for deploying PaCo with Neon database (free), Railway backend, and Vercel frontend.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Database Setup (Neon PostgreSQL - Free)](#database-setup)
3. [Backend Deployment (Railway)](#backend-deployment)
4. [Frontend Deployment (Vercel)](#frontend-deployment)
5. [Post-Deployment Setup](#post-deployment-setup)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before starting, ensure you have:

- GitHub account (for code hosting)
- Neon account (https://console.neon.tech) - **FREE**
- Railway account (https://railway.app) - $5/month for backend
- Vercel account (https://vercel.com) - FREE for frontend
- ElevenLabs API key (https://elevenlabs.io)
- OpenAI API key (https://platform.openai.com)
- Git installed locally
- Your code pushed to a GitHub repository

---

## Database Setup (Neon PostgreSQL - Free)

### Step 1: Create Neon Account

1. Go to https://console.neon.tech
2. Sign up with GitHub (recommended) or email
3. Verify your email if needed

### Step 2: Create Database Project

1. Click "Create Project" or "New Project"
2. Choose a project name (e.g., "paco-production")
3. Select a region (choose closest to your Railway region)
4. Select PostgreSQL version: 16 (recommended)
5. Click "Create Project"

### Step 3: Get Connection String

1. In your Neon project dashboard, find the "Connection Details" section
2. Select "Connection string" tab
3. Copy the connection string - it looks like:
   ```
   postgresql://username:password@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```
4. Save this securely - you'll need it for Railway configuration

### Step 4: (Optional) Create Database Branch

Neon allows database branching for dev/staging:
1. Go to "Branches" tab
2. Click "Create branch"
3. Name it "development" or "staging"
4. Use different connection strings for different environments

---

## Backend Deployment (Railway)

### Step 1: Prepare Railway Configuration Files

Create/verify these files in your `paco-api/` directory:

**railway.toml**
```toml
[build]
builder = "nixpacks"
buildCommand = "pip install -r requirements.txt"

[deploy]
startCommand = "export PYTHONPATH=/app:$PYTHONPATH && alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT"
restartPolicyType = "on_failure"
restartPolicyMaxRetries = 10
```

**Procfile** (optional backup)
```
web: export PYTHONPATH=/app:$PYTHONPATH && alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**runtime.txt**
```
python-3.11.0
```

### Step 2: Deploy to Railway

1. Go to Railway dashboard
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Choose the `paco-api` directory as root

### Step 3: Configure Environment Variables

In Railway project settings → Variables, add:

```bash
# Database - Paste your Neon connection string from Step 3 above
DATABASE_URL=postgresql://username:password@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require

# Security
JWT_SECRET_KEY=<generate-with-command-below>
ADMIN_PASSWORD=<your-secure-password>

# AI Services
OPENAI_API_KEY=sk-...
ELEVENLABS_API_KEY=...

# CORS - Update after Vercel deployment
CORS_ORIGINS=["https://your-app.vercel.app"]

# Python path
PYTHONPATH=/app
```

**Generate JWT Secret:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 4: Set Root Directory

1. In Railway Settings → "Service"
2. Set "Root Directory" to `paco-api`
3. Click "Save"

### Step 5: Deploy

1. Railway will auto-deploy on push
2. Check "Deployments" tab for build logs
3. Wait for "Success" status
4. Click on deployment → "View Logs" to verify

### Step 6: Get Your Backend URL

1. Go to "Settings" tab
2. Under "Networking" → "Public Networking"
3. Click "Generate Domain"
4. Copy the URL (e.g., `https://your-app.up.railway.app`)

### Step 7: Verify Deployment

Test your backend:
```bash
curl https://your-app.up.railway.app/health
# Should return: {"status":"healthy"}

curl https://your-app.up.railway.app/
# Should return: {"message":"PaCo API","version":"1.0.0","docs":"/docs"}
```

Visit API docs: `https://your-app.up.railway.app/docs`

---

## Frontend Deployment (Vercel)

### Step 1: Prepare Vercel Configuration

Create `vercel.json` in project root:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "paco-frontend/package.json",
      "use": "@vercel/next"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "paco-frontend/$1"
    }
  ],
  "buildCommand": "cd paco-frontend && npm install && npm run build",
  "outputDirectory": "paco-frontend/.next",
  "framework": "nextjs",
  "installCommand": "cd paco-frontend && npm install"
}
```

### Step 2: Deploy to Vercel

#### Option A: Vercel Dashboard

1. Go to https://vercel.com/dashboard
2. Click "Add New" → "Project"
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: Next.js
   - **Root Directory**: `paco-frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

#### Option B: Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Navigate to frontend
cd paco-frontend

# Deploy
vercel --prod
```

### Step 3: Configure Environment Variables

In Vercel Project Settings → Environment Variables:

```bash
NEXT_PUBLIC_API_URL=https://your-app.up.railway.app/api/v1
NEXT_PUBLIC_ELEVENLABS_AGENT_ID=your_agent_id
```

**Important**: `NEXT_PUBLIC_` prefix is required for client-side variables.

### Step 4: Redeploy

After adding environment variables:
1. Go to "Deployments" tab
2. Click "..." on latest deployment
3. Select "Redeploy"
4. Check "Use existing Build Cache" → Click "Redeploy"

### Step 5: Get Your Frontend URL

1. Vercel will provide a URL: `https://your-app.vercel.app`
2. Copy this URL

---

## Post-Deployment Setup

### Step 1: Update CORS Origins

1. Go back to Railway backend
2. Update `CORS_ORIGINS` environment variable:
   ```
   CORS_ORIGINS=["https://your-app.vercel.app"]
   ```
3. Redeploy backend

### Step 2: Create Research IDs

You need to create initial research IDs for users to access the system.

#### Method A: API Call (Recommended)

```bash
curl -X POST https://your-app.up.railway.app/api/v1/admin/research-ids \
  -H "Content-Type: application/json" \
  -d '{
    "password": "your_admin_password",
    "research_id": "PATIENT_001",
    "notes": "Test patient",
    "is_active": true
  }'
```

#### Method B: Direct Database Access (Neon)

1. Go to https://console.neon.tech
2. Navigate to your project
3. Click "SQL Editor" in the left sidebar
4. Run SQL:
```sql
INSERT INTO paco_research_ids (research_id, is_active, notes)
VALUES ('PATIENT_001', true, 'Test patient');
```

### Step 3: Test Complete Flow

1. Visit your Vercel URL: `https://your-app.vercel.app`
2. Enter a research ID you created
3. Accept the disclaimer
4. Start a conversation
5. Verify messages save to database

### Step 4: Configure ElevenLabs Agent

1. Go to ElevenLabs dashboard
2. Create or edit your Conversational AI agent
3. Set the system prompt for PaCo (from `paco-api/app/prompts.py`)
4. Copy the Agent ID
5. Update in Vercel environment variables

---

## Environment Variables Reference

### Railway (Backend)

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | Neon PostgreSQL connection string | `postgresql://user:pass@ep-xxx.neon.tech/neondb?sslmode=require` |
| `JWT_SECRET_KEY` | Secret for JWT tokens | Generate with: `secrets.token_urlsafe(32)` |
| `ADMIN_PASSWORD` | Admin endpoint password | Strong password |
| `OPENAI_API_KEY` | OpenAI API key | `sk-...` |
| `ELEVENLABS_API_KEY` | ElevenLabs API key | Your key |
| `CORS_ORIGINS` | Allowed frontend origins | `["https://your-app.vercel.app"]` |
| `PYTHONPATH` | Python module path | `/app` |

### Vercel (Frontend)

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `https://your-app.railway.app/api/v1` |
| `NEXT_PUBLIC_ELEVENLABS_AGENT_ID` | ElevenLabs agent ID | Your agent ID |

---

## Troubleshooting

### Backend Issues

#### Database Connection Failed

```bash
# Check DATABASE_URL format
echo $DATABASE_URL
# Should be: postgresql://user:password@host:port/database

# Test connection
curl https://your-app.up.railway.app/health
```

#### Migrations Not Running

```bash
# Check Railway logs
# Look for: "alembic upgrade head"

# Manual migration via Railway CLI
railway run alembic upgrade head
```

#### CORS Errors

```bash
# Verify CORS_ORIGINS includes your frontend URL
# Format must be JSON array: ["https://domain.com"]

# Check Railway logs for CORS_ORIGINS value on startup
```

### Frontend Issues

#### API Connection Failed

1. Check browser console for errors
2. Verify `NEXT_PUBLIC_API_URL` is set correctly
3. Test backend directly:
   ```bash
   curl https://your-backend.railway.app/health
   ```

#### ElevenLabs Widget Not Loading

1. Verify `NEXT_PUBLIC_ELEVENLABS_AGENT_ID` is set
2. Check browser console for errors
3. Verify ElevenLabs API key is valid in backend

#### Environment Variables Not Working

- Redeploy after adding variables
- Ensure `NEXT_PUBLIC_` prefix for client-side vars
- Check Vercel deployment logs

### Database Issues

#### Reset Database (Neon)

1. Go to https://console.neon.tech
2. Navigate to your project → SQL Editor
3. Run:
```sql
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
```

Then redeploy backend on Railway to run migrations.

#### Check Tables (Neon)

1. Go to Neon console → SQL Editor
2. Run:
```sql
SELECT * FROM alembic_version;
SELECT * FROM paco_research_ids;
SELECT * FROM paco_conversations LIMIT 10;
```

---

## Continuous Deployment

### Automatic Deployments

Both Railway and Vercel support automatic deployments:

1. **Railway**: Auto-deploys on push to `main` branch
2. **Vercel**: Auto-deploys on push to `main` branch

### Manual Deployments

**Railway:**
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link project
railway link

# Deploy
railway up
```

**Vercel:**
```bash
# From paco-frontend directory
vercel --prod
```

---

## Production Checklist

Before going live:

- [ ] Set strong `ADMIN_PASSWORD`
- [ ] Generate secure `JWT_SECRET_KEY`
- [ ] Configure proper CORS origins
- [ ] Set up database backups (Railway has automatic backups)
- [ ] Test all API endpoints
- [ ] Verify medication analysis works
- [ ] Test research ID flow end-to-end
- [ ] Set up monitoring/logging
- [ ] Document research ID creation process
- [ ] Train administrators on the system

---

## Monitoring & Logs

### Railway Logs

```bash
# View logs
railway logs

# Follow logs
railway logs -f
```

Or view in Railway dashboard → Deployments → View Logs

### Vercel Logs

View in Vercel dashboard → Project → Logs

Or use Vercel CLI:
```bash
vercel logs your-deployment-url
```

---

## Backup & Recovery

### Database Backup (Neon)

Neon provides multiple backup options:

#### Point-in-Time Restore (Free Tier)
- Neon automatically tracks all changes
- Can restore to any point in the last 7 days (free tier)
- 30 days for paid plans

#### Manual Backup

```bash
# Export database using pg_dump
pg_dump "postgresql://user:pass@ep-xxx.neon.tech/neondb?sslmode=require" > backup.sql

# Restore
psql "postgresql://user:pass@ep-xxx.neon.tech/neondb?sslmode=require" < backup.sql
```

#### Database Branching (Recommended)
1. Go to Neon console → Branches
2. Create a branch from production
3. This creates an instant copy for testing/backup
4. Free on all plans!

---

## Scaling

### Neon Database

- ✅ Automatically scales compute
- ✅ Auto-suspend after 5 minutes of inactivity (saves resources)
- ✅ Instant branching for dev/staging
- ✅ Free tier: 512 MB storage
- ✅ Paid plans: Scale up to hundreds of GB

### Railway (Backend)

- Auto-scales based on traffic
- Adjust resources in Settings → Resources
- Monitor usage in Metrics tab
- Pay only for what you use

### Vercel (Frontend)

- Auto-scales automatically
- No configuration needed
- Serverless architecture
- Free for personal projects

---

## Support

- **Neon**: https://neon.tech/docs
- **Railway**: https://railway.app/help
- **Vercel**: https://vercel.com/support
- **GitHub Issues**: Open an issue in your repository

---

## Cost Summary

### Monthly Costs (Estimated)

- **Neon Database**: $0 (Free forever)
- **Railway Backend**: ~$5-10 (usage-based, depends on traffic)
- **Vercel Frontend**: $0 (Free for personal/hobby projects)
- **ElevenLabs**: Varies by usage
- **OpenAI**: Varies by API calls

**Total: ~$5-10/month** (plus API usage)

---

## Summary

You now have:
- ✅ Neon PostgreSQL database (FREE)
- ✅ FastAPI backend on Railway with auto-migrations
- ✅ Next.js frontend on Vercel (FREE)
- ✅ Continuous deployment on all platforms
- ✅ Environment variables configured
- ✅ CORS properly set up
- ✅ Research IDs created

**Best of all: Only ~$5-10/month for the entire infrastructure!** 🎉

Your application is live and ready for research participants!
