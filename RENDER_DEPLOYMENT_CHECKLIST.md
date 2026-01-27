# Render Deployment Checklist

Quick checklist for deploying PaCo on Render.

## Pre-Deployment (5 minutes)

- [ ] Code pushed to GitHub
- [ ] `render.yaml` exists in root directory
- [ ] All dependencies in `paco-api/requirements.txt`
- [ ] All dependencies in `paco-frontend/package.json`
- [ ] Render account created at https://render.com
- [ ] GitHub connected to Render account

## Environment Variables (2 minutes)

Collect these before deployment:

```
GROQ_API_KEY = [from console.groq.com]
ELEVENLABS_API_KEY = [from elevenlabs.io]
ELEVENLABS_AGENT_ID = [from your agent]
SECRET_KEY = [generate with: python3 -c "import secrets; print(secrets.token_hex(32))"]
ADMIN_PASSWORD = [choose a strong password]
```

## Deployment Steps (10-15 minutes)

1. **Create Blueprint**
   - [ ] Go to https://dashboard.render.com
   - [ ] Click "New +" → "Blueprint"
   - [ ] Select GitHub repository
   - [ ] Click "Apply"

2. **Monitor Initial Build**
   - [ ] Watch logs for `paco-db` (database)
   - [ ] Watch logs for `paco-api` (backend)
   - [ ] Watch logs for `paco-frontend` (frontend)
   - [ ] Wait until all show "Live" status

3. **Add Environment Variables to Backend**
   - [ ] Click `paco-api` service
   - [ ] Click "Environment" tab
   - [ ] Add DATABASE_URL from `paco-db` Info tab
   - [ ] Add SECRET_KEY
   - [ ] Add GROQ_API_KEY
   - [ ] Add ELEVENLABS_API_KEY
   - [ ] Add CORS_ORIGINS = https://paco-frontend.onrender.com
   - [ ] Add PYTHONUNBUFFERED = true
   - [ ] Click "Save" (triggers redeploy)

4. **Add Environment Variables to Frontend**
   - [ ] Click `paco-frontend` service
   - [ ] Click "Environment" tab
   - [ ] Add NEXT_PUBLIC_API_URL = https://paco-api.onrender.com/api/v1
   - [ ] Add NEXT_PUBLIC_ELEVENLABS_AGENT_ID
   - [ ] Click "Save" (triggers redeploy)

5. **Wait for Redeploy**
   - [ ] Backend logs show "Uvicorn running"
   - [ ] Frontend logs show "ready - started server on"
   - [ ] Both services show "Live" status

## Verification (5 minutes)

Test your deployment:

```bash
# Test backend health
curl https://paco-api.onrender.com/health

# Open API docs
https://paco-api.onrender.com/docs

# Open frontend
https://paco-frontend.onrender.com

# Test basic functionality
- [ ] Frontend loads
- [ ] Can interact with UI
- [ ] Voice widget appears (if configured)
```

## Post-Deployment (5 minutes)

- [ ] Set up monitoring (optional)
- [ ] Test all features work
- [ ] Document deployment details
- [ ] Save backup of environment variables
- [ ] Share URLs with team/users

## Troubleshooting Quick Fixes

**If services won't deploy:**
1. Check logs for specific error
2. Click "Manual Deploy" to retry
3. Verify environment variables are set
4. Check GitHub connection

**If database won't start:**
1. Check `paco-db` logs
2. May need 2-3 minutes to initialize
3. No action needed - it will start automatically

**If backend can't connect to database:**
1. Verify DATABASE_URL is set
2. Check it includes `?sslmode=require`
3. Copy full URL from paco-db Info tab

**If frontend can't reach backend:**
1. Verify NEXT_PUBLIC_API_URL is correct
2. Check backend is running (test /health)
3. Check CORS_ORIGINS includes frontend domain

## Important URLs

| Service | URL |
|---------|-----|
| Dashboard | https://dashboard.render.com |
| API Base | https://paco-api.onrender.com |
| API Docs | https://paco-api.onrender.com/docs |
| Frontend | https://paco-frontend.onrender.com |

## Important Notes

- **Free tier services auto-spin down** after 15 minutes of inactivity (30-60 sec cold start)
- **First request takes longer** due to container startup
- **Database is always-on** even on free tier
- **Logs available 24/7** in Render dashboard
- **Automatic deploys** triggered by GitHub pushes (if enabled)

## Getting Help

- **Documentation**: https://render.com/docs
- **API Status**: https://status.render.com
- **Support**: https://render.com/support

---

**Total Time**: ~30 minutes for first-time deployment
**Success Indicators**: 
- ✅ All services show "Live"
- ✅ `/health` endpoint responds
- ✅ Frontend loads without errors
- ✅ Can interact with application
