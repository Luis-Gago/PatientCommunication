# Render Deployment Setup Guide

Step-by-step guide to deploy PaCo on Render (recommended deployment platform).

## Prerequisites

- GitHub account with code pushed to a repository
- Render account (free: https://render.com)
- ElevenLabs API key (https://elevenlabs.io)
- GROQ API key (https://console.groq.com)
- Email address for all accounts

## Step 1: Prepare Your GitHub Repository

Ensure your code is committed and pushed to GitHub:

```bash
cd PatientCommunication
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

**Important Files for Render:**
- `render.yaml` - Blueprint configuration (in root directory)
- `paco-api/requirements.txt` - Python dependencies
- `paco-api/Procfile` - Alternative start command
- `paco-frontend/package.json` - Node.js dependencies

## Step 2: Create Render Account

1. Go to https://render.com
2. Sign up with GitHub (recommended for easier integration)
3. Verify your email
4. Create a personal account (if prompted)

## Step 3: Deploy Using Blueprint (Recommended)

### Option A: Automated Blueprint Deployment (Easiest)

1. In Render Dashboard, click **"New +" → "Blueprint"**
2. Select your GitHub repository containing `render.yaml`
3. Accept the GitHub authorization if prompted
4. Render will automatically detect and display services from `render.yaml`:
   - `paco-api` (FastAPI Backend)
   - `paco-frontend` (Next.js Frontend)
   - `paco-db` (PostgreSQL Database)
5. Click **"Apply"** to create all services
6. Render will automatically provision everything

### Option B: Manual Service Deployment (More Control)

Skip the blueprint and create services individually.

## Step 4: Configure Environment Variables

After deployment starts (or if using manual deployment), add environment variables:

### For Backend Service (paco-api)

1. Go to Render Dashboard → `paco-api` service
2. Click **"Environment"** tab
3. Add these variables:

| Variable | Value | Type |
|----------|-------|------|
| `DATABASE_URL` | From `paco-db` service connection string | Service Ref |
| `SECRET_KEY` | Generate a random secure key | Secret |
| `GROQ_API_KEY` | Your GROQ API key | Secret |
| `ELEVENLABS_API_KEY` | Your ElevenLabs API key | Secret |
| `CORS_ORIGINS` | `https://paco-frontend.onrender.com` | Fixed string |
| `PYTHONUNBUFFERED` | `true` | Fixed string |

**How to get DATABASE_URL:**
1. Go to `paco-db` service in Render
2. Click **"Info"** tab
3. Find "External Database URL" and copy it
4. Add as environment variable to backend

**How to generate SECRET_KEY:**
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### For Frontend Service (paco-frontend)

1. Go to Render Dashboard → `paco-frontend` service
2. Click **"Environment"** tab
3. Add these variables:

| Variable | Value |
|----------|-------|
| `NEXT_PUBLIC_API_URL` | `https://paco-api.onrender.com/api/v1` |
| `NEXT_PUBLIC_ELEVENLABS_AGENT_ID` | Your ElevenLabs agent ID |

## Step 5: Wait for Deployment

Monitor the deployment progress:

1. **Backend Logs**: Click `paco-api` → **"Logs"** tab
2. **Frontend Logs**: Click `paco-frontend` → **"Logs"** tab
3. **Database**: Click `paco-db` → **"Logs"** tab

Expected steps:
- `paco-db`: Should show "PostgreSQL started successfully"
- `paco-api`: Running migrations → Starting Uvicorn server
- `paco-frontend`: Building Next.js → Starting server

**First deployment typically takes 5-10 minutes.**

## Step 6: Verify Deployment

Once all services show "Live" status:

### Test Backend API

```bash
# Health check
curl https://paco-api.onrender.com/health

# Should return: {"status":"healthy"}
```

### Test Frontend

Open in browser:
```
https://paco-frontend.onrender.com
```

You should see the PaCo application interface.

### View API Documentation

```
https://paco-api.onrender.com/docs
```

## Step 7: Seed Initial Data (Optional)

To add initial research IDs or test data:

1. Click `paco-api` service
2. Click **"Shell"** tab
3. Run:
   ```bash
   cd /opt/render/project/src
   python scripts/seed_research_ids.py
   ```

## Common Deployment URLs

Once deployed, your services will be at:

| Service | URL |
|---------|-----|
| API | `https://paco-api.onrender.com` |
| API Docs | `https://paco-api.onrender.com/docs` |
| Frontend | `https://paco-frontend.onrender.com` |
| Database | Connection via internal Render network |

## Updating Deployed Code

To update your application after deployment:

1. Make changes locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update feature"
   git push origin main
   ```
3. Render will automatically redeploy (if "Auto-Deploy" is enabled)
4. Monitor deployment in "Events" or "Logs" tab

To manually trigger redeployment:
1. Go to service → Click **"Manual Deploy"** button
2. Select branch
3. Click **"Deploy"**

## Troubleshooting

### Deployment Fails at Build Step

**Error**: `pip install failed` or `npm install failed`

**Solution**:
1. Check the error message in Logs
2. Verify dependencies are in `requirements.txt` or `package.json`
3. Check for Python/Node version compatibility
4. Click "Manual Deploy" to retry

### Services Not Starting

**Error**: Backend showing "Build failed" or "Start failed"

**Check**:
1. Logs for specific error messages
2. Environment variables are set correctly
3. DATABASE_URL is valid and accessible
4. Port 8000 (backend) and 3000 (frontend) are not hardcoded

### Frontend Cannot Reach Backend

**Error**: "Cannot connect to API" in browser console

**Solution**:
1. Verify `NEXT_PUBLIC_API_URL` is set to backend service URL
2. Check backend CORS_ORIGINS includes frontend domain
3. Ensure backend is running (check Logs)
4. Test API directly in browser: `https://paco-api.onrender.com/health`

### Database Connection Timeout

**Error**: "Cannot connect to database" in backend logs

**Solution**:
1. Ensure `paco-db` service is "Live" in Render
2. Verify DATABASE_URL environment variable is correct
3. Check connection string format:
   ```
   postgresql://user:password@hostname:5432/database
   ```
4. Ensure no special characters in password (URL-encode if needed)

### Free Tier Service Spins Down

**Symptom**: Service takes 30-60 seconds to respond after inactivity

**This is normal on free tier** - services auto-spin down after 15 minutes of no requests.

**Solutions**:
1. Upgrade to paid plan ($7+/month) for always-on
2. Set up uptime monitoring to keep services active
3. Accept slower cold-start response times

## Performance Tips

### Backend Optimization

1. Use `PYTHONUNBUFFERED=true` for better logging
2. Set appropriate number of workers in Uvicorn
3. Monitor database connections
4. Use environment variables for configuration

### Frontend Optimization

1. Enable Next.js caching where possible
2. Optimize images and assets
3. Use static generation when appropriate

### Database Optimization

1. Monitor query performance
2. Add indexes for frequently queried columns
3. Archive old data if needed

## Monitoring

Monitor your deployment:

1. **Dashboard**: https://dashboard.render.com
2. **Logs**: Each service has a "Logs" tab showing real-time output
3. **Events**: Shows deployment history and status changes
4. **Metrics**: Some metrics available (CPU, memory, etc.)

## Billing

### Free Tier
- 0.5 shared CPU
- 512 MB RAM per service
- Auto-spins down after 15 min of inactivity
- 100 GB/month bandwidth
- Great for development and testing

### Paid Plans (Starting at $7/month per service)
- Dedicated resources
- Always-on (no spin down)
- Priority support
- More reliable for production

## Next Steps

After successful deployment:

1. ✅ Test all features thoroughly
2. ✅ Set up custom domain (optional)
3. ✅ Configure email notifications for errors
4. ✅ Set up monitoring and alerts
5. ✅ Document any custom configurations
6. ✅ Establish backup strategy for database

## Support

- **Render Docs**: https://render.com/docs
- **Render Support**: https://render.com/support
- **GitHub Issues**: Check repository for known issues
- **Community**: Render Discord community

## Quick Reference: Common Commands

```bash
# Generate secure secret key
python3 -c "import secrets; print(secrets.token_hex(32))"

# Test backend connectivity
curl https://paco-api.onrender.com/health

# View live logs
# (Use Render dashboard "Logs" tab)

# Trigger manual deployment
# (Use Render dashboard "Manual Deploy" button)
```
