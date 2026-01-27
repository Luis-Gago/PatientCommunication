# Render Deployment - Quick Reference

## 🚀 Quick Deploy Checklist

### Before Deploying:
- [ ] Push code to Git repository
- [ ] Have GROQ_API_KEY ready
- [ ] Have ELEVENLABS_API_KEY ready
- [ ] Have ELEVENLABS_AGENT_ID ready
- [ ] Generate SECRET_KEY: `python -c "import secrets; print(secrets.token_urlsafe(32))"`

### Deploy Steps:
1. **Sign in to Render**: https://dashboard.render.com
2. **Click "New +" → "Blueprint"**
3. **Connect repository** (GitHub/GitLab/Bitbucket)
4. **Render detects `render.yaml`** automatically
5. **Add environment variables**:
   - GROQ_API_KEY
   - ELEVENLABS_API_KEY
   - ELEVENLABS_AGENT_ID
   - SECRET_KEY
6. **Click "Apply"** - Creates database + web service
7. **Wait for deployment** (~5-10 minutes)
8. **Test your API**: `https://your-service.onrender.com/docs`

### Your Service URLs:
- API: `https://paco-api.onrender.com` (will be your actual URL)
- Docs: `https://paco-api.onrender.com/docs`
- Health: `https://paco-api.onrender.com/`

## 📝 Environment Variables Required

```bash
# LLM & Voice
GROQ_API_KEY=gsk_...
ELEVENLABS_API_KEY=...
ELEVENLABS_AGENT_ID=...

# Security
SECRET_KEY=... # Generate with: python -c "import secrets; print(secrets.token_urlsafe(32))"
ALGORITHM=HS256  # Optional, defaults to HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30  # Optional, defaults to 30

# Database (auto-populated by Render)
DATABASE_URL=postgresql://...  # Set automatically
```

## 🔧 Files Created for Render

- `render.yaml` - Blueprint configuration (infrastructure as code)
- `build.sh` - Build script (installs dependencies)
- `start_render.sh` - Startup script (migrations + server)
- `RENDER_DEPLOYMENT.md` - Full documentation

## 🔄 Updating Your App

### After Code Changes:
1. Commit and push to your repository
2. Render auto-deploys the new version
3. Check deployment logs in dashboard

### Updating Environment Variables:
1. Dashboard → Your Service → Environment
2. Edit variables
3. Save (triggers redeploy)

## ⚠️ Common Issues

### "ModuleNotFoundError: No module named 'app.models'"
- Fixed! `start_render.sh` sets `PYTHONPATH` correctly

### Service takes long to respond
- Free tier spins down after 15 minutes inactivity
- First request after spin-down: 30-60 seconds
- Solution: Upgrade to paid plan for always-on

### Migration fails
- Check DATABASE_URL is set
- Verify database is running
- Check logs in Render dashboard

## 💰 Pricing

**Free Tier:**
- 750 hours/month
- Spins down after 15 min inactive
- Perfect for testing/development

**Starter ($7/month):**
- Always on (no spin-down)
- 0.5 GB RAM
- Good for production

See: https://render.com/pricing

## 📚 More Help

- Full Guide: See `RENDER_DEPLOYMENT.md`
- Render Docs: https://render.com/docs
- Support: https://community.render.com
