# Railway Deployment Fix Guide

## Problem
`ModuleNotFoundError: No module named 'app.models'` during Alembic migration on Railway.

## Root Cause
Railway was running Alembic migrations without the correct PYTHONPATH set, so Python couldn't locate the `app` module.

## Solutions Applied

### 1. Updated `railway.toml`
- Added `PYTHONPATH` environment variable configuration
- This ensures Railway sets the path before running any commands

### 2. Enhanced `alembic/env.py`
- More robust sys.path manipulation
- Better debug output to troubleshoot deployment issues

## Railway Dashboard Configuration

**CRITICAL**: In your Railway dashboard, verify these settings:

### Project Settings
1. **Root Directory**: Must be set to `paco-api`
   - Settings → Root Directory → `paco-api`
   
2. **Environment Variables**: Add if not already set:
   ```
   PYTHONPATH=/app
   DATABASE_URL=<your-postgres-connection-string>
   SECRET_KEY=<your-secret-key>
   GROQ_API_KEY=<your-groq-key>
   ```

3. **Build Settings**:
   - Builder: Nixpacks (automatic)
   - Build Command: (leave empty, handled by nixpacks)
   - Start Command: `bash start.sh` (already in railway.toml)

## Deployment Steps

1. Commit and push these changes:
   ```bash
   git add paco-api/railway.toml paco-api/alembic/env.py
   git commit -m "Fix Railway PYTHONPATH for alembic migrations"
   git push
   ```

2. Railway will auto-deploy (if connected to GitHub)

3. Monitor logs for the debug output from `env.py`:
   - Look for "DEBUG - Parent dir (should contain 'app' module)"
   - Verify it shows `/app` 
   - Check "'app' directory exists" shows True

## If Still Failing

If you still get the module error after these fixes:

### Alternative Fix: Use Dockerfile
Railway's Nixpacks might have path issues. Create a `Dockerfile` in `paco-api/`:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Set PYTHONPATH
ENV PYTHONPATH=/app

# Make start script executable
RUN chmod +x start.sh

# Expose port
EXPOSE 8000

# Run start script
CMD ["bash", "start.sh"]
```

Then in Railway Settings:
- Builder: Dockerfile
- Dockerfile Path: paco-api/Dockerfile

## Railway vs Render

**Recommendation**: Stay with Railway for now. This is a fixable configuration issue.

### Railway Pros:
- Better free tier compute
- Faster deployments
- Built-in PostgreSQL with better performance
- No cold starts

### Render Pros:
- More stable/predictable builds
- Better documentation
- Slightly easier configuration

**Bottom line**: The fixes above should resolve your issue. Only switch to Render if Railway continues to fail after trying the Dockerfile approach.

## Testing Locally

Verify the fix works locally:

```bash
cd paco-api
export PYTHONPATH=/Users/luisgago/PatientCommunication/paco-api
alembic upgrade head
```

This should run without errors.
