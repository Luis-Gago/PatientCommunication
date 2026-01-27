# 🚀 PaCo API - Migration from Railway to Render

## Summary of Changes

Your backend has been successfully refactored for Render deployment. All Railway-specific issues have been resolved.

## ✅ What Was Done

### 1. **Created Render Configuration Files**
   - `render.yaml` - Infrastructure as code (Blueprint)
   - `build.sh` - Dependency installation script
   - `start_render.sh` - Startup script with migrations
   - `.renderignore` - Excludes unnecessary files from deployment

### 2. **Fixed Module Import Issues**
   The Railway error `ModuleNotFoundError: No module named 'app.models'` is resolved by:
   - Setting `PYTHONPATH` correctly in `start_render.sh`
   - Using proper Python path configuration

### 3. **Updated Dependencies**
   - Added `gunicorn>=21.2.0` to `requirements.txt` for production

### 4. **Created Documentation**
   - `RENDER_DEPLOYMENT.md` - Comprehensive deployment guide
   - `RENDER_QUICK_START.md` - Quick reference for deployment

## 📁 New Files Created

```
paco-api/
├── render.yaml                 # Render Blueprint configuration
├── build.sh                    # Build script (executable)
├── start_render.sh            # Startup script (executable)
├── .renderignore              # Files to exclude from deployment
├── RENDER_DEPLOYMENT.md       # Full deployment guide
├── RENDER_QUICK_START.md      # Quick reference
└── requirements.txt           # Updated with gunicorn
```

## 🎯 Key Differences: Railway vs Render

| Feature | Railway | Render |
|---------|---------|--------|
| Config File | `railway.toml` | `render.yaml` |
| Build Script | Automatic | `build.sh` |
| Start Script | `start.sh` / Procfile | `start_render.sh` |
| Free Tier | 500 hrs/month | 750 hrs/month |
| Spin Down | Yes (after inactivity) | Yes (after 15 min) |
| Database | PostgreSQL plugin | PostgreSQL service |

## 🚀 Deployment Instructions

### Quick Start (5 minutes)

1. **Push to Git** (if not already done):
   ```bash
   cd /Users/luisgago/PatientCommunication
   git add paco-api/
   git commit -m "Add Render deployment configuration"
   git push
   ```

2. **Go to Render**: https://dashboard.render.com

3. **Create Blueprint**:
   - Click "New +" → "Blueprint"
   - Connect your Git repository
   - Render detects `render.yaml` automatically
   - Click "Apply"

4. **Add Environment Variables** in Render Dashboard:
   ```bash
   GROQ_API_KEY=your_key_here
   ELEVENLABS_API_KEY=your_key_here
   ELEVENLABS_AGENT_ID=your_id_here
   SECRET_KEY=generate_with_command_below
   ```
   
   Generate SECRET_KEY:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

5. **Deploy** - Render builds and deploys automatically (~5-10 minutes)

6. **Test Your API**:
   - Visit: `https://paco-api.onrender.com/docs`
   - Check health: `https://paco-api.onrender.com/`

## 🔧 What Happens During Deployment

### Build Phase (`build.sh`)
```bash
1. Upgrade pip
2. Install requirements.txt dependencies
```

### Start Phase (`start_render.sh`)
```bash
1. Set PYTHONPATH for proper imports
2. Run Alembic migrations: alembic upgrade head
3. Start Uvicorn server on PORT (assigned by Render)
```

## 🐛 Troubleshooting

### The Original Railway Error (Now Fixed)
```
ModuleNotFoundError: No module named 'app.models'
```

**Root Cause**: Railway couldn't find the `app.models` module due to incorrect Python path.

**Solution**: `start_render.sh` properly sets:
```bash
export PYTHONPATH="${PYTHONPATH:+${PYTHONPATH}:}$(pwd)"
```

### Common Render Issues

1. **Slow First Response (Free Tier)**
   - Service spins down after 15 minutes
   - First request: 30-60 seconds to wake up
   - Solution: Upgrade to paid plan ($7/month)

2. **Build Failures**
   - Check logs in Render dashboard
   - Verify `build.sh` has execute permissions
   - Ensure all dependencies in `requirements.txt`

3. **Database Connection Issues**
   - Verify `DATABASE_URL` is set (should be automatic)
   - Check database is in same region as web service
   - Ensure database is running

## 📊 Deployment Architecture

```
Your Git Repo (GitHub/GitLab)
       │
       ▼
   Render Platform
   ┌─────────────────────────────┐
   │                             │
   │  Web Service (paco-api)     │
   │  ┌─────────────────────┐    │
   │  │ build.sh           │    │
   │  │   ↓                │    │
   │  │ start_render.sh    │    │
   │  │   ↓                │    │
   │  │ alembic upgrade    │    │
   │  │   ↓                │    │
   │  │ uvicorn app.main   │    │
   │  └──────────┬──────────┘    │
   │             │                │
   │             ▼                │
   │  PostgreSQL (paco-db)       │
   │  ┌─────────────────────┐    │
   │  │ Database: paco      │    │
   │  │ Auto-connected      │    │
   │  └─────────────────────┘    │
   │                             │
   └─────────────────────────────┘
```

## 🔐 Environment Variables

### Required (You must set):
- `GROQ_API_KEY` - For LLM functionality
- `ELEVENLABS_API_KEY` - For voice synthesis
- `ELEVENLABS_AGENT_ID` - For ElevenLabs agent
- `SECRET_KEY` - For JWT token generation

### Auto-set by Render:
- `DATABASE_URL` - PostgreSQL connection string
- `PORT` - Service port (usually 10000)

### Optional (have defaults):
- `ALGORITHM` - Default: HS256
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Default: 30

## 💰 Cost Comparison

| Plan | Railway | Render |
|------|---------|--------|
| Free | 500 hrs/month | 750 hrs/month |
| Free DB | 1GB storage | 1GB storage |
| Paid Start | $5/month | $7/month |
| Always On | ✓ (paid) | ✓ (paid) |

## 📚 Documentation Files

1. **`RENDER_DEPLOYMENT.md`** - Complete guide with:
   - Detailed deployment steps
   - Troubleshooting section
   - Security best practices
   - Update procedures

2. **`RENDER_QUICK_START.md`** - Quick reference with:
   - Deployment checklist
   - Environment variable list
   - Common issues
   - Quick commands

## 🎉 Next Steps

1. **Deploy to Render** using the quick start guide
2. **Update your frontend** to point to new Render URL
3. **Test all endpoints** to ensure everything works
4. **Set up custom domain** (optional)
5. **Configure monitoring** (Render has built-in logging)

## 🆘 Getting Help

- **Render Docs**: https://render.com/docs
- **Render Community**: https://community.render.com
- **This Project**: Check `RENDER_DEPLOYMENT.md` for detailed info

## ✨ Benefits of Render vs Railway

1. **More free tier hours** (750 vs 500)
2. **Blueprint deployment** (infrastructure as code)
3. **Better documentation** and community support
4. **Simpler pricing** model
5. **Built-in SSL/TLS** certificates
6. **Automatic deploys** from Git
7. **Easy environment management**

---

**You're all set!** 🚀 Follow the Quick Start guide to deploy to Render.

For detailed instructions, see: `RENDER_QUICK_START.md`
For comprehensive guide, see: `RENDER_DEPLOYMENT.md`
