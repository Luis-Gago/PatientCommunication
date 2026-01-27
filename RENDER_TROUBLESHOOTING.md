# Render Deployment Troubleshooting Guide

Comprehensive troubleshooting guide for PaCo deployment on Render.

## Quick Diagnosis

Before diving into specific solutions:

1. **Check Render Dashboard Status**
   - Go to https://dashboard.render.com
   - Look for service status: "Live", "Deploying", or "Failed"
   - Click on service to view logs

2. **Check Service Logs**
   - Click on problematic service
   - Go to "Logs" tab
   - Look for error messages or warnings

3. **Test Connectivity**
   ```bash
   # Test backend
   curl https://paco-api.onrender.com/health
   
   # Test frontend
   curl https://paco-frontend.onrender.com
   ```

---

## Deployment Issues

### Issue: "Build failed" Status

**Symptoms**
- Service shows red "Build failed" status
- Deployment doesn't start

**Possible Causes**

1. **Missing Dependencies**
   - Error: `No module named 'xxx'`
   - Solution: Add package to `requirements.txt` or `package.json`
   - Action: Commit, push, then click "Manual Deploy"

2. **Python Version Mismatch**
   - Error: `SyntaxError` or `ModuleNotFoundError`
   - Solution: Check `runtime.txt` or `render.yaml` has correct version
   - Should be: `python-3.11` or later

3. **Node Version Mismatch**
   - Error: npm or Node syntax errors
   - Solution: Update `package.json` scripts to work with Node 18+

4. **Build Command Syntax Error**
   - Error: Command not found or syntax error in build command
   - Solution: Check `render.yaml` build commands are correct
   - Example: `pip install -r requirements.txt && alembic upgrade head`

**Solutions**
```bash
# Step 1: Check local build works
cd paco-api
pip install -r requirements.txt  # Should not error

# Step 2: Verify Python version
python3 --version  # Should be 3.9+

# Step 3: Commit and push
git add .
git commit -m "Fix build issues"
git push origin main

# Step 4: Manual deploy in Render
# Go to service → Click "Manual Deploy" → Select branch → Deploy
```

### Issue: Deployment Stuck at "Deploying"

**Symptoms**
- Service shows orange "Deploying" status for > 30 minutes
- No error message

**Possible Causes**

1. **Large Dependencies**
   - Installing many packages takes time
   - Wait up to 30 minutes for first deployment

2. **Database Initialization**
   - First-time database provisioning takes time
   - Check `paco-db` service status

3. **Build Process Hanging**
   - Migration taking too long
   - Check logs for progress

**Solutions**
```bash
# Wait at least 30 minutes
# Check logs for progress

# If still stuck after 30+ minutes:
# 1. Go to service → Settings → Click "Pause"
# 2. Wait 30 seconds
# 3. Click "Resume"
# 4. Or click "Manual Deploy" to retry
```

### Issue: "Start failed" or "Start timeout"

**Symptoms**
- Service shows "Start failed" or times out during startup
- Error about command not found

**Possible Causes**

1. **alembic Not Installed**
   - Error: `alembic: command not found`
   - Solution: Ensure `alembic==1.13.1` in requirements.txt

2. **Working Directory Wrong**
   - Error: Database or file not found
   - Solution: Start command assumes correct directory

3. **Port Not Set**
   - Error: Port already in use
   - Solution: Use `$PORT` environment variable (automatic in Render)

**Solutions**
```python
# paco-api/requirements.txt - Add if missing:
alembic==1.13.1
```

Then:
```bash
git add paco-api/requirements.txt
git commit -m "Ensure alembic in requirements"
git push
# Manual Deploy in Render
```

---

## Database Issues

### Issue: "Cannot connect to database"

**Symptoms**
- Backend logs show: `FATAL: database ... does not exist`
- Error: `psycopg2.OperationalError: could not connect`

**Possible Causes**

1. **DATABASE_URL Not Set**
   - Missing environment variable
   - Solution: Add to backend Environment variables

2. **DATABASE_URL Incorrect**
   - Wrong connection string
   - Solution: Copy from `paco-db` Info tab

3. **paco-db Service Not Running**
   - Database service not provisioned
   - Solution: Check `paco-db` status

4. **Connection String Format Wrong**
   - Missing `?sslmode=require` for Render
   - Should be: `postgresql://user:pass@host:5432/db?sslmode=require`

**Solutions**

1. **Verify paco-db Service**
   ```
   Dashboard → paco-db → Info
   Check status is "Available"
   ```

2. **Get Correct Connection String**
   ```
   paco-db service → Info tab
   Look for "External Database URL"
   Copy entire string including ?sslmode=require
   ```

3. **Set DATABASE_URL**
   ```
   paco-api → Environment
   Add: DATABASE_URL = [pasted URL from above]
   Click Save
   ```

4. **Test Connection**
   ```bash
   # Via Render Shell in paco-api:
   psql "$DATABASE_URL" -c "SELECT 1"
   # Should return: 1
   ```

### Issue: "Migrations Failed"

**Symptoms**
- Backend logs show alembic error
- Database tables not created
- Error: `FAILED: Column does not exist`

**Possible Causes**

1. **Migration Files Missing or Corrupted**
   - alembic/versions/ directory empty
   - Solution: Verify migration files are committed

2. **Multiple Migrations Conflicting**
   - Two migrations with same version number
   - Solution: Check alembic/versions/ directory

3. **Database Schema Already Exists**
   - Migration trying to create existing table
   - Solution: Check if data exists in database

**Solutions**

```bash
# Step 1: Check migrations locally
cd paco-api
ls alembic/versions/  # Should show migration files

# Step 2: Test locally
python3 -m pip install -r requirements.txt
alembic upgrade head  # Should succeed

# Step 3: Commit and deploy
git add .
git commit -m "Fix migrations"
git push

# Step 4: Manual deploy in Render
# Or clear database and redeploy
```

### Issue: "Database Connection Timeout"

**Symptoms**
- Error: `connection timeout` or `timeout waiting for connection`
- Backend hangs when trying to query

**Possible Causes**

1. **Too Many Connections**
   - Free tier has limited connections
   - Solution: Restart backend service

2. **Network Timeout**
   - Slow or unstable connection
   - Solution: Retry operation

3. **Database Queries Too Slow**
   - Large queries timing out
   - Solution: Optimize queries or add indexes

**Solutions**

```bash
# Restart backend service
# Dashboard → paco-api → Click "Pause"
# Wait 10 seconds
# Click "Resume"

# Or check for slow queries
# paco-db Shell:
SELECT * FROM pg_stat_statements 
ORDER BY mean_exec_time DESC 
LIMIT 10;
```

---

## Frontend Issues

### Issue: "Cannot GET /" or Blank Page

**Symptoms**
- Frontend shows blank or 404 error
- Browser console shows errors

**Possible Causes**

1. **Build Failed Silently**
   - Frontend not built
   - Check logs

2. **Environment Variables Missing**
   - NEXT_PUBLIC_API_URL not set
   - Frontend can't find backend

3. **Next.js Port Wrong**
   - Default port 3000 not used
   - Solution: Use PORT environment variable

**Solutions**

```bash
# Step 1: Check frontend logs
# Dashboard → paco-frontend → Logs
# Look for build errors

# Step 2: Verify environment variables
# Dashboard → paco-frontend → Environment
# Ensure NEXT_PUBLIC_API_URL is set

# Step 3: Redeploy
# Click "Manual Deploy"
```

### Issue: "Cannot Reach API" / Network Errors

**Symptoms**
- Browser console shows: `Failed to fetch` or CORS error
- Frontend loads but API calls fail

**Possible Causes**

1. **NEXT_PUBLIC_API_URL Incorrect**
   - Wrong backend URL
   - Should be: `https://paco-api.onrender.com/api/v1`

2. **Backend CORS Not Allowing Frontend**
   - Error: `Access-Control-Allow-Origin header missing`
   - Solution: Add frontend URL to CORS_ORIGINS

3. **Backend Service Not Running**
   - paco-api service down
   - Solution: Check paco-api status and logs

4. **Network Connectivity**
   - Internet connection issue
   - Solution: Check browser network tab

**Solutions**

```bash
# Step 1: Verify NEXT_PUBLIC_API_URL
# paco-frontend → Environment
# Check: NEXT_PUBLIC_API_URL = https://paco-api.onrender.com/api/v1

# Step 2: Test backend health
curl https://paco-api.onrender.com/health
# Should return: {"status":"healthy"}

# Step 3: Check CORS_ORIGINS
# paco-api → Environment
# Check: CORS_ORIGINS includes frontend domain

# Step 4: Check browser network tab
# DevTools → Network
# Look for failed requests to API
```

### Issue: Voice Widget Not Working

**Symptoms**
- ElevenLabs widget doesn't appear
- Error in console about agent

**Possible Causes**

1. **NEXT_PUBLIC_ELEVENLABS_AGENT_ID Not Set**
   - Environment variable missing
   - Solution: Add to frontend environment

2. **ElevenLabs API Key Wrong**
   - Backend has wrong key
   - Solution: Verify in backend environment

3. **API Integration Issue**
   - Backend not properly configured
   - Check logs

**Solutions**

```bash
# Step 1: Verify frontend environment
# paco-frontend → Environment
# NEXT_PUBLIC_ELEVENLABS_AGENT_ID must be set

# Step 2: Verify backend environment
# paco-api → Environment
# ELEVENLABS_API_KEY must be set

# Step 3: Check browser console
# DevTools → Console
# Look for specific error messages

# Step 4: Test backend endpoint
curl https://paco-api.onrender.com/api/v1/health
```

---

## Performance Issues

### Issue: Slow Response Times

**Symptoms**
- Pages take > 10 seconds to load
- API requests very slow

**Possible Causes**

1. **Cold Start (Free Tier)**
   - First request after 15+ minutes of inactivity
   - Normal on free tier: 30-60 seconds first request
   - Solution: Upgrade to paid tier

2. **Database Queries Too Slow**
   - Large dataset or missing indexes
   - Solution: Optimize queries or add indexes

3. **Limited Resources**
   - Free tier: 0.5 CPU, 512MB RAM
   - Solution: Upgrade to paid tier

**Solutions**

```bash
# For free tier slowness - this is normal
# Upgrade to paid tier for consistent performance
# Go to service → Settings → Plan → Change to Paid

# For slow queries:
# Connect to database and check:
EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';
```

### Issue: "Service Out of Memory" Error

**Symptoms**
- Error: `Out of memory: Kill process`
- Service keeps restarting

**Possible Causes**

1. **Memory Leak**
   - Application using too much memory
   - Solution: Check code for leaks

2. **Large Dataset Operations**
   - Processing too much data at once
   - Solution: Paginate or batch process

3. **Insufficient Resources**
   - Free tier only has 512MB
   - Solution: Upgrade to paid tier

**Solutions**

```bash
# Step 1: Increase resources
# Service → Settings → Plan → Upgrade to Paid

# Step 2: Optimize code
# Look for memory-heavy operations
# Use pagination for large queries

# Step 3: Monitor memory usage
# In Render Shell:
free -h
```

---

## Auto-Deploy / GitHub Integration Issues

### Issue: "Repository Not Found" or Authorization Error

**Symptoms**
- Cannot connect GitHub repository
- Error during blueprint creation

**Possible Causes**

1. **GitHub Account Not Connected**
   - Render doesn't have GitHub access
   - Solution: Reconnect GitHub account

2. **Repository Private**
   - Render can't access private repo
   - Solution: Use GitHub token or make repo public

3. **Wrong Repository Selected**
   - Selected wrong GitHub account

**Solutions**

```bash
# Step 1: Disconnect and reconnect GitHub
# Render Dashboard → Settings → Connected Services
# Click GitHub → Disconnect → Reconnect

# Step 2: Verify GitHub access
# Go to GitHub Settings → Applications
# Check Render has permission

# Step 3: Use GitHub token if needed
# Render Settings → GitHub Token
# Paste personal access token
```

### Issue: Push to GitHub Doesn't Trigger Deploy

**Symptoms**
- Pushed code to GitHub
- Render service doesn't redeploy

**Possible Causes**

1. **Auto-Deploy Disabled**
   - Manual deploy only
   - Solution: Enable auto-deploy in settings

2. **Wrong Branch**
   - Deploy watches main/master, pushed to different
   - Solution: Push to correct branch

3. **GitHub Webhook Not Configured**
   - Render not receiving push notifications
   - Solution: Reconnect GitHub

**Solutions**

```bash
# Enable auto-deploy:
# Service → Settings → Auto-Deploy
# Toggle "Auto-deploy commit" to ON

# Verify branch:
# Service → Settings → Branch
# Should match your GitHub branch name

# Manual deploy if needed:
# Service → Click "Manual Deploy"
```

---

## Common Error Messages

| Error Message | Cause | Solution |
|---|---|---|
| `ModuleNotFoundError: No module named 'xxx'` | Dependency missing | Add to requirements.txt |
| `FATAL: database does not exist` | DATABASE_URL wrong/not set | Check environment variables |
| `alembic: command not found` | alembic not installed | Ensure in requirements.txt |
| `Address already in use` | Port conflict | Use $PORT environment variable |
| `Cannot connect to API` | Backend down or CORS issue | Check backend status, CORS settings |
| `Connection timeout` | Database unreachable | Check paco-db service, SSLMODE |
| `Out of memory` | Memory exhausted | Upgrade plan or optimize code |
| `Start failed` | Command error | Check logs, verify environment variables |
| `Build failed` | Build command error | Check logs, fix dependencies |
| `CORS policy: No 'Access-Control-Allow-Origin'` | CORS not configured | Add frontend URL to CORS_ORIGINS |

---

## Testing Endpoints

### Backend Health Checks

```bash
# Health check endpoint
curl https://paco-api.onrender.com/health

# API documentation
curl https://paco-api.onrender.com/docs

# Root endpoint
curl https://paco-api.onrender.com/
```

### Database Connection Test

```bash
# Via Render Shell in paco-api:
psql "$DATABASE_URL" -c "SELECT 1"

# List tables:
psql "$DATABASE_URL" -c "\dt"

# Test specific query:
psql "$DATABASE_URL" -c "SELECT COUNT(*) FROM \"User\";"
```

### Frontend Connectivity

```bash
# Check frontend loads
curl https://paco-frontend.onrender.com

# Check network requests
# In browser: DevTools → Network tab → Reload
```

---

## Getting Help

1. **Check Logs First**
   - Most issues visible in Render logs
   - Service → Logs tab

2. **Render Status Page**
   - Check if Render platform has issues
   - https://status.render.com

3. **Render Support**
   - For account/billing issues
   - https://render.com/support

4. **Community**
   - Render Discord for peer help
   - Stack Overflow for general questions

5. **GitHub Issues**
   - Check project repository for known issues

---

## Escalation Path

If basic troubleshooting doesn't work:

1. **Collect Information**
   - Save error messages and logs
   - Screenshot of dashboard
   - List of steps you took

2. **Check Render Status**
   - Is the platform having issues?

3. **Search Known Issues**
   - GitHub issues
   - Stack Overflow
   - Render documentation

4. **Contact Support**
   - Render Support: https://render.com/support
   - Include collected information
   - Describe reproduction steps

---

**Last Updated**: January 27, 2026
**Applies To**: PaCo v1.0.0+ on Render
