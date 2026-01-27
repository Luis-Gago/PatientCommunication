# Railway Fork Configuration Checklist

## Critical: Railway Must Point to YOUR Fork

### 1. Check Railway GitHub Connection

**In Railway Dashboard → Project Settings → GitHub:**

- ✅ **Repository**: Should be `Luis-Gago/PatientCommunication` 
- ❌ **NOT**: `DrDavidL/pad` (the upstream/original repo)

**If it shows the wrong repo:**
1. Disconnect the GitHub integration
2. Reconnect and select YOUR fork: `Luis-Gago/PatientCommunication`
3. Set branch to `main`

### 2. Root Directory Configuration

**Railway Settings → Root Directory:**
- Must be: `paco-api`

### 3. Environment Variables (May Be Missing from Fork)

These might not have transferred from the original project:

```bash
# Required Variables
DATABASE_URL=postgresql://...       # Your Neon or Railway Postgres URL
JWT_SECRET_KEY=...                  # Generate new one
ADMIN_PASSWORD=...                  # Your admin password
GROQ_API_KEY=gsk_...               # Your Groq API key
ELEVENLABS_API_KEY=...             # Your ElevenLabs key

# Optional but Recommended
CORS_ORIGINS=["https://your-frontend.vercel.app"]
PYTHONPATH=/app                     # Fixed in railway.toml
```

### 4. Deployment Triggers

**Railway Settings → Deploys:**
- Watch for: Branch `main` in `Luis-Gago/PatientCommunication`
- Root directory: `paco-api`
- Auto-deploy: Enabled (recommended)

## Common Fork Issues

### Issue 1: Railway Deploying Old Upstream Code
**Symptom**: Changes you make don't appear in deployment
**Fix**: Verify GitHub connection points to YOUR fork

### Issue 2: Missing Environment Variables
**Symptom**: Deployment fails with missing secrets/keys
**Fix**: Manually add all env vars (they don't copy from upstream)

### Issue 3: Wrong Branch Being Deployed
**Symptom**: Old code keeps deploying
**Fix**: Set deployment branch to `main` in your fork

## How to Verify Railway Configuration

1. **Check Deployment Logs**:
   - Look for: `Cloning repository Luis-Gago/PatientCommunication`
   - If it says `DrDavidL/pad`, wrong repo is connected!

2. **Check Current Commit**:
   - Railway should show commit: `143e323 - more ai slop for deployment...`
   - This is YOUR latest commit, not upstream's

3. **Test Environment Variables**:
   - Add a test endpoint to verify DATABASE_URL is YOUR database
   - Check that JWT_SECRET_KEY is not from original project

## Re-linking Railway to Your Fork

If Railway is connected to the wrong repo:

### Option A: Fresh Railway Project (Recommended)
1. Create NEW Railway project
2. Connect to `Luis-Gago/PatientCommunication`
3. Set root directory: `paco-api`
4. Add all environment variables fresh
5. Deploy

### Option B: Reconnect Existing Project
1. Railway Dashboard → Settings
2. Scroll to "Danger Zone"
3. Disconnect GitHub Integration
4. Reconnect → Select `Luis-Gago/PatientCommunication`
5. Reconfigure root directory and branch
6. Trigger new deployment

## Environment Variables to Generate Fresh

Since this is a fork, DON'T reuse the original project's secrets:

```bash
# Generate new JWT secret
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Set new admin password
# Use a password manager or generate strong password

# Use YOUR Groq API key
# From: https://console.groq.com/

# Use YOUR ElevenLabs API key  
# From: https://elevenlabs.io/app/settings
```

## Verify Deployment Success

After fixing the configuration:

1. **Check Logs**: Should see successful alembic migration
2. **Test Health Endpoint**: `curl https://your-app.railway.app/health`
3. **Verify Database**: Check it's connecting to YOUR Neon database
4. **Test API**: Try creating a research ID via `/api/v1/admin/research-ids`

## Fork-Specific Best Practices

1. **Never share environment variables** between fork and upstream
2. **Use separate databases** (your own Neon instance)
3. **Keep Railway connected to YOUR fork**, not upstream
4. **Document your changes** that differ from upstream
5. **Update README** with your deployment URLs

## Current Status

- ✅ Code fixes applied (railway.toml, env.py)
- ⚠️ Need to verify Railway points to `Luis-Gago/PatientCommunication`
- ⚠️ Need to verify environment variables are YOUR keys, not upstream's
- ⚠️ Need to verify DATABASE_URL points to YOUR database

## Next Steps

1. Log into Railway Dashboard
2. Verify GitHub connection shows YOUR fork
3. Check all environment variables are yours
4. Trigger a fresh deployment
5. Monitor logs for success
