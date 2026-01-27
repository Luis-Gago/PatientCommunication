# PaCo API - Render Deployment Guide

This guide explains how to deploy the PaCo (Patient Communication) backend API to Render.

## Prerequisites

- A Render account (sign up at https://render.com)
- Your code pushed to a Git repository (GitHub, GitLab, or Bitbucket)
- Environment variables ready (API keys, secrets, etc.)

## Deployment Steps

### 1. Prepare Your Repository

Ensure your repository contains these Render-specific files (already included):
- `render.yaml` - Render Blueprint configuration
- `build.sh` - Build script for installing dependencies
- `start_render.sh` - Startup script for running migrations and starting the server
- `requirements.txt` - Python dependencies

### 2. Create a New Web Service on Render

#### Option A: Using Render Blueprint (Recommended)

1. Go to your Render Dashboard
2. Click "New" → "Blueprint"
3. Connect your Git repository
4. Render will automatically detect the `render.yaml` file
5. Review the configuration and click "Apply"

This will create:
- A PostgreSQL database (`paco-db`)
- A web service (`paco-api`) connected to the database

#### Option B: Manual Setup

1. **Create PostgreSQL Database:**
   - Go to Render Dashboard
   - Click "New" → "PostgreSQL"
   - Name: `paco-db`
   - Database Name: `paco`
   - Region: Oregon (or your preferred region)
   - Plan: Free (or paid)
   - Click "Create Database"

2. **Create Web Service:**
   - Click "New" → "Web Service"
   - Connect your Git repository
   - Configure:
     - Name: `paco-api`
     - Region: Oregon (same as database)
     - Runtime: Python 3
     - Build Command: `./build.sh`
     - Start Command: `./start_render.sh`
     - Plan: Free (or paid)

### 3. Configure Environment Variables

In your Render Web Service settings, add these environment variables:

#### Auto-Generated Variables
These are set automatically if using Blueprint:
- `DATABASE_URL` - Auto-populated from the database connection

#### Required Variables (You must add these)
```
GROQ_API_KEY=your_groq_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
ELEVENLABS_AGENT_ID=your_elevenlabs_agent_id_here
SECRET_KEY=your_secret_key_for_jwt_here
```

#### Optional Variables (have defaults)
```
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

To generate a secure `SECRET_KEY`, run:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 4. Deploy

- If using Blueprint, click "Apply" to deploy both database and web service
- If manual setup, the service will deploy automatically after configuration
- Monitor the deployment logs in the Render dashboard
- First deployment may take 5-10 minutes

### 5. Verify Deployment

Once deployed:
1. Check the service logs for any errors
2. Visit your service URL (e.g., `https://paco-api.onrender.com`)
3. Test the health endpoint: `https://your-service.onrender.com/`
4. Check API documentation: `https://your-service.onrender.com/docs`

## Deployment Architecture

```
┌─────────────────────┐
│  Git Repository     │
│  (GitHub/GitLab)    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Render Platform    │
├─────────────────────┤
│                     │
│  ┌───────────────┐  │
│  │  Web Service  │  │
│  │  (paco-api)   │  │
│  │               │  │
│  │  Port: 8000   │  │
│  └───────┬───────┘  │
│          │          │
│          ▼          │
│  ┌───────────────┐  │
│  │  PostgreSQL   │  │
│  │  (paco-db)    │  │
│  └───────────────┘  │
│                     │
└─────────────────────┘
```

## How It Works

### Build Process (`build.sh`)
1. Upgrades pip
2. Installs all Python dependencies from `requirements.txt`

### Startup Process (`start_render.sh`)
1. Sets up `PYTHONPATH` for proper module imports
2. Runs Alembic database migrations
3. Starts Uvicorn server on the assigned port

### Database Migrations
- Migrations run automatically on every deployment
- Uses Alembic to manage schema changes
- Database schema is kept in sync with code

## Troubleshooting

### Import Errors
If you see `ModuleNotFoundError`:
- Check that `PYTHONPATH` is set in `start_render.sh`
- Verify all `__init__.py` files exist in your packages
- Review the deployment logs

### Database Connection Issues
- Verify `DATABASE_URL` environment variable is set
- Check database is in the same region as web service
- Ensure database is running (check Render dashboard)

### Migration Failures
- Check migration files in `alembic/versions/`
- Review Alembic configuration in `alembic.ini` and `alembic/env.py`
- Check database connection string format

### Service Won't Start
- Review logs in Render dashboard
- Verify all required environment variables are set
- Check that scripts have execute permissions (should be set by Git)

## Updating Your Deployment

### Code Updates
1. Push changes to your Git repository
2. Render automatically detects the push
3. Triggers a new build and deployment
4. New version goes live after successful build

### Environment Variables
1. Go to your service in Render dashboard
2. Navigate to "Environment" tab
3. Add/modify variables
4. Click "Save Changes"
5. Service will automatically redeploy

### Manual Redeploy
1. Go to your service in Render dashboard
2. Click "Manual Deploy" → "Deploy latest commit"

## Cost Considerations

### Free Tier Limitations
- Web services spin down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds
- 750 hours/month of runtime
- PostgreSQL: 90 days retention, 1GB storage

### Upgrading
Consider upgrading to paid plans for:
- Always-on services (no spin-down)
- More compute resources
- Longer database retention
- Automatic daily backups
- Priority support

## Support

- Render Documentation: https://render.com/docs
- Render Community: https://community.render.com
- Project Issues: [Your repository issues page]

## Security Best Practices

1. **Never commit secrets** - Use environment variables
2. **Rotate keys regularly** - Update API keys periodically
3. **Use HTTPS** - Render provides SSL/TLS automatically
4. **Monitor logs** - Check for suspicious activity
5. **Keep dependencies updated** - Run `pip list --outdated` regularly

## Next Steps

After successful deployment:
1. Set up custom domain (optional)
2. Configure CORS for your frontend
3. Set up monitoring and alerts
4. Configure backup strategy
5. Plan for scaling (if needed)
