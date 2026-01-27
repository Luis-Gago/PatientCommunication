# Migration Guide: Railway → Render

Step-by-step guide to migrate PaCo from Railway to Render.

## Overview

This guide helps you move your deployment from Railway + Neon + Vercel to Render (which includes everything).

**Benefits of Migration:**
- Simpler management (single provider)
- Better free tier
- Integrated PostgreSQL database
- Lower costs for small projects
- More predictable billing

## Prerequisites

- Render account (https://render.com)
- Access to your Railway project
- GitHub repository with latest code
- Your existing Neon database (optional to keep)
- ElevenLabs and GROQ API keys (same as Railway)

## Phase 1: Prepare for Migration

### Step 1: Export Data from Current Database (Optional)

If you want to preserve data from Railway/Neon:

```bash
# From your local machine (with connection to Neon)
pg_dump "postgresql://user:password@host:5432/neondb" > backup.sql

# Or use Neon dashboard for automated backups
```

### Step 2: Verify Your GitHub Repository

Ensure all code is committed and pushed:

```bash
cd PatientCommunication
git status
git add .
git commit -m "Prepare for Render migration"
git push origin main
```

### Step 3: Collect Configuration Values

Gather these from Railway dashboard:
- ✅ GROQ_API_KEY
- ✅ ELEVENLABS_API_KEY
- ✅ SECRET_KEY
- ✅ ADMIN_PASSWORD (if set)
- ✅ Any other custom environment variables

## Phase 2: Deploy on Render

### Step 1: Create Render Project

1. Go to https://render.com/dashboard
2. Click **"New +" → "Blueprint"**
3. Select your GitHub repository
4. Review the services from `render.yaml`:
   - `paco-api` (Backend)
   - `paco-frontend` (Frontend)
   - `paco-db` (PostgreSQL Database)
5. Click **"Apply"**

### Step 2: Wait for Initial Deployment

Monitor the deployment:
- `paco-db`: PostgreSQL initialization
- `paco-api`: Building Python environment + running migrations
- `paco-frontend`: Building Next.js

**Expected time: 10-15 minutes for first deployment**

### Step 3: Add Environment Variables

While deployment is running, add environment variables:

#### Backend Service (paco-api)

Go to `paco-api` → **"Environment"** and add:

```
DATABASE_URL = [Auto-filled from paco-db]
SECRET_KEY = [Your existing secret key or new one]
GROQ_API_KEY = [Your GROQ key]
ELEVENLABS_API_KEY = [Your ElevenLabs key]
CORS_ORIGINS = https://paco-frontend.onrender.com
ADMIN_PASSWORD = [Your admin password if needed]
PYTHONUNBUFFERED = true
```

#### Frontend Service (paco-frontend)

Go to `paco-frontend` → **"Environment"** and add:

```
NEXT_PUBLIC_API_URL = https://paco-api.onrender.com/api/v1
NEXT_PUBLIC_ELEVENLABS_AGENT_ID = [Your agent ID]
```

### Step 4: Wait for Full Deployment

Check the status:
1. `paco-api`: Should show "Live" with health check passing
2. `paco-frontend`: Should show "Live"
3. `paco-db`: Should show "Available"

## Phase 3: Migrate Data (Optional)

### Option A: Restore from Neon/Railway Backup

If you exported data earlier:

1. Get Render database connection:
   - Go to `paco-db` service → **"Info"** tab
   - Copy the "External Database URL"

2. Restore backup:
   ```bash
   psql "[Render Database URL]" < backup.sql
   ```

### Option B: Start Fresh

1. Run seed script (if available):
   ```bash
   # Via Render Shell
   cd /opt/render/project/src
   python scripts/seed_research_ids.py
   ```

2. Create admin user:
   ```bash
   # Via API or database directly
   ```

## Phase 4: Verify Migration

### Test API

```bash
# Health check
curl https://paco-api.onrender.com/health

# Should return: {"status":"healthy"}
```

### Test Frontend

Open: https://paco-frontend.onrender.com

Verify:
- ✅ Frontend loads without errors
- ✅ Can interact with the UI
- ✅ Can connect to backend
- ✅ Voice features work (if configured)

### Test Database

Via Render Shell (in paco-api service):

```bash
# Connect to database
psql "$DATABASE_URL"

# Run basic query
SELECT COUNT(*) FROM "ResearchID";
SELECT COUNT(*) FROM "User";

# Exit
\q
```

## Phase 5: Cleanup

### Disable Old Services (Keep as Backup)

1. **Railway Backend**: 
   - Go to Railway dashboard
   - Service → Settings → "Pause"
   - Or leave running for 1-2 weeks as backup

2. **Vercel Frontend**:
   - Go to Vercel dashboard
   - Project → Settings → "Pause"
   - Or let it continue running (cheap to maintain)

3. **Neon Database**:
   - Optional: Keep as backup
   - Or delete to stop charges

### Update DNS/Domain (If Using Custom Domain)

Update your domain to point to Render URLs:
- Backend: `paco-api.onrender.com`
- Frontend: `paco-frontend.onrender.com`

Or set up custom domains in Render dashboard.

## Common Issues During Migration

### Database Connection Fails

**Issue**: Backend shows "Cannot connect to database"

**Solution**:
1. Verify DATABASE_URL is set in environment variables
2. Ensure `paco-db` is showing "Available"
3. Check connection string format (must include `?sslmode=require`)
4. Test with Render Shell:
   ```bash
   psql "$DATABASE_URL" -c "SELECT 1"
   ```

### Frontend Cannot Reach Backend

**Issue**: Frontend shows connection errors

**Solution**:
1. Verify `NEXT_PUBLIC_API_URL` in frontend environment
2. Check backend CORS settings include frontend domain
3. Test backend directly: `https://paco-api.onrender.com/health`
4. Check browser console for detailed errors

### Migrations Fail

**Issue**: "alembic: command not found" or migration errors

**Solution**:
1. Ensure `alembic==1.13.1` in `requirements.txt`
2. Check backend logs for specific errors
3. May need to manually run migrations via Shell:
   ```bash
   cd /opt/render/project/src
   alembic upgrade head
   ```

### Services Won't Start

**Issue**: Services show "Build failed" or "Start failed"

**Solution**:
1. Check logs for specific error
2. Verify all environment variables are set
3. Check Python/Node version compatibility
4. Try "Manual Deploy" to retry build

## Rollback Plan

If migration has issues:

### Quick Rollback (< 1 hour)

1. Keep Railway services running
2. Update DNS/domain back to Railway URLs
3. Disable Render services (click "Pause")
4. Resume Railway services

### Data Rollback

If data was corrupted:
1. Restore from backup to Neon
2. Update Railway to use restored Neon database
3. Restart Railway services

## Post-Migration Checklist

- [ ] All services showing "Live" status
- [ ] API health check passing
- [ ] Frontend loads without errors
- [ ] Database connection working
- [ ] Can perform core user actions
- [ ] Voice features functional
- [ ] Monitoring/logging in place
- [ ] Old services disabled or backed up
- [ ] Team notified of new URLs (if applicable)
- [ ] DNS/custom domain updated (if applicable)

## Performance Monitoring

After migration, monitor:

1. **Backend Logs**: https://dashboard.render.com → `paco-api` → "Logs"
2. **Database Performance**: Query new database directly
3. **Response Times**: Monitor API response times
4. **Error Rates**: Track 4xx/5xx errors

## Cost Comparison

### Old Setup (Railway + Neon + Vercel)
- Railway backend: $5/month (minimum)
- Neon database: Free tier or $15+/month
- Vercel frontend: Free
- **Total: $5-20/month**

### New Setup (Render)
- Free tier: $0 (with limitations)
- Paid tier: $7/service/month = $21+/month
- **Total: $0-21/month depending on tier**

**Note**: Free tier on Render suitable for dev/testing. Upgrade to paid tier ($7+/month per service) for production with guaranteed uptime.

## Getting Help

- **Render Documentation**: https://render.com/docs
- **Render Support**: https://render.com/support
- **GitHub Issues**: Check repository for migration issues
- **Community**: Render Discord

## Next Steps

1. ✅ Complete initial verification
2. ✅ Monitor for 24-48 hours
3. ✅ Train team on new Render deployment process
4. ✅ Update internal documentation
5. ✅ Plan maintenance and backup strategy
6. ✅ Consider upgrading to paid plan for production stability
