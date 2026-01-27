# Railway Deployment Fix ✅

## Problem
Railway was failing with `ModuleNotFoundError: No module named 'app.models'` during Alembic migrations.

## Root Cause
The PYTHONPATH environment variable wasn't being properly applied during the startup command execution, causing Python to not find the `app` module when Alembic tried to run migrations.

## Solution
Created a robust startup script (`start.sh`) that:
1. Explicitly sets the working directory
2. Exports PYTHONPATH=/app before running any commands
3. Runs Alembic migrations with proper error handling
4. Starts uvicorn server
5. Includes debug output for troubleshooting

## Changes Made

### 1. Created `paco-api/start.sh`
A bash script that handles the entire startup process with proper environment setup.

### 2. Updated `paco-api/railway.toml`
Changed from inline command to using the startup script:
```toml
startCommand = "bash start.sh"
```

## Deployment Steps

### Step 1: Push Changes to GitHub
```bash
cd /Users/luisgago/PatientCommunication
git add paco-api/start.sh paco-api/railway.toml
git commit -m "Fix Railway PYTHONPATH issue with startup script"
git push origin main
```

### Step 2: Railway Will Auto-Deploy
Railway will automatically detect the push and redeploy.

### Step 3: Monitor Deployment
1. Go to Railway dashboard → Your project
2. Click on "Deployments" tab
3. Watch the logs for:
   - "Working directory: /app"
   - "Running Alembic migrations..."
   - "Migrations completed successfully"
   - "Starting uvicorn server..."

### Step 4: Verify Deployment
Once deployed, test:
```bash
curl https://your-railway-url.railway.app/health
# Should return: {"status":"healthy"}

curl https://your-railway-url.railway.app/
# Should return: {"message":"PaCo API","version":"1.0.0","docs":"/docs"}
```

## Environment Variables (Already Configured ✅)

Your Railway environment variables are correctly set:
- ✅ `DATABASE_URL` - Neon PostgreSQL connection
- ✅ `SECRET_KEY` - JWT secret
- ✅ `ADMIN_PASSWORD` - Admin endpoint password
- ✅ `GROQ_API_KEY` - Groq AI for medication analysis
- ✅ `ELEVENLABS_API_KEY` - ElevenLabs voice AI
- ✅ `CORS_ORIGINS` - Frontend origins (comma-separated)
- ✅ `PYTHONPATH` - Python module path

## What to Update After Vercel Deployment

Once you deploy the frontend to Vercel and get your URL (e.g., `https://paco-frontend-abc123.vercel.app`), update in Railway:

```bash
CORS_ORIGINS=http://localhost:3000,https://paco-frontend-abc123.vercel.app,https://paco-frontend-abc123-*.vercel.app
```

The `*` pattern allows preview deployments to work too!

## Troubleshooting

### If migrations still fail:
1. Check Railway logs for the debug output from start.sh
2. Verify "Root Directory" in Railway Settings is set to `paco-api`
3. Ensure all environment variables are set correctly

### If PYTHONPATH errors persist:
The start.sh script explicitly sets it, so this should be resolved. If issues continue, check the logs for the exact error.

### Database connection issues:
- Verify your Neon database is active
- Test the connection string format (should have `sslmode=require`)
- Check Neon console for any connection limits

## Next Steps

1. ✅ Commit and push changes (see Step 1 above)
2. ⏳ Wait for Railway auto-deployment
3. ✅ Test the health endpoint
4. ✅ Deploy frontend to Vercel
5. ✅ Update CORS_ORIGINS with Vercel URL
6. 🎉 Your app is live!

## Cost Reminder

With Groq AI (FREE) instead of OpenAI:
- **Monthly Total**: ~$10-15
  - Neon: $0 (Free)
  - Railway: $5-10
  - Vercel: $0 (Free)
  - ElevenLabs: $5-22
  - Groq: $0 (Free!)

Perfect for research projects! 🎓
