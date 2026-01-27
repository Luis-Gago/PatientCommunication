# ✅ Render Deployment Checklist

Use this checklist to ensure a successful deployment to Render.

## 📋 Pre-Deployment Checklist

### Repository Setup
- [ ] Code is in a Git repository (GitHub, GitLab, or Bitbucket)
- [ ] Latest changes are committed and pushed
- [ ] All Render files are present:
  - [ ] `render.yaml`
  - [ ] `build.sh`
  - [ ] `start_render.sh`
  - [ ] `requirements.txt`
  - [ ] `.renderignore`

### Environment Variables Ready
- [ ] GROQ_API_KEY obtained
- [ ] ELEVENLABS_API_KEY obtained
- [ ] ELEVENLABS_AGENT_ID obtained
- [ ] SECRET_KEY generated (run: `python -c "import secrets; print(secrets.token_urlsafe(32))"`)
- [ ] All variables documented in `.env.render` file

### Account Setup
- [ ] Render account created (https://render.com)
- [ ] Git provider connected to Render
- [ ] Payment method added (if using paid tier)

## 🚀 Deployment Checklist

### Step 1: Create Blueprint
- [ ] Go to Render Dashboard
- [ ] Click "New +" → "Blueprint"
- [ ] Select your Git repository
- [ ] Verify `render.yaml` is detected
- [ ] Review configuration preview

### Step 2: Configure Environment
- [ ] Add GROQ_API_KEY
- [ ] Add ELEVENLABS_API_KEY
- [ ] Add ELEVENLABS_AGENT_ID
- [ ] Add SECRET_KEY
- [ ] Verify DATABASE_URL will be auto-set
- [ ] Verify PORT will be auto-set

### Step 3: Deploy
- [ ] Click "Apply" to start deployment
- [ ] Monitor build logs
- [ ] Wait for "Live" status (~5-10 minutes)

## ✓ Post-Deployment Verification

### Basic Health Checks
- [ ] Service shows "Live" in Render dashboard
- [ ] Visit service URL (e.g., https://paco-api.onrender.com)
- [ ] Check health endpoint: `GET /`
- [ ] Check API docs: `GET /docs`
- [ ] No errors in service logs

### Database Verification
- [ ] Database shows "Available" in Render dashboard
- [ ] Migrations ran successfully (check logs for "alembic upgrade head")
- [ ] No database connection errors in logs

### API Endpoint Testing
- [ ] Test authentication endpoint: `POST /auth/login`
  ```bash
  curl -X POST "https://paco-api.onrender.com/auth/login" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=test&password=test"
  ```

- [ ] Test health endpoint: `GET /`
  ```bash
  curl "https://paco-api.onrender.com/"
  ```

- [ ] Test API documentation loads: `GET /docs`
  ```bash
  curl "https://paco-api.onrender.com/docs"
  ```

### External Service Integration
- [ ] Groq API key works (check logs for LLM responses)
- [ ] ElevenLabs API key works (test voice endpoint)
- [ ] No API authentication errors

## 🔧 Configuration Verification

### Environment Variables
- [ ] All required variables are set
- [ ] No sensitive data in logs
- [ ] DATABASE_URL is auto-populated
- [ ] PORT is set correctly

### Service Settings
- [ ] Region matches database region (Oregon)
- [ ] Build command is `./build.sh`
- [ ] Start command is `./start_render.sh`
- [ ] Auto-deploy is enabled (for continuous deployment)

### Database Settings
- [ ] Database is in correct region
- [ ] Database name is `paco`
- [ ] Connection is internal (not public)
- [ ] Backups enabled (if paid plan)

## 📱 Frontend Integration Checklist

### Update Frontend Configuration
- [ ] Update API_URL to Render URL
- [ ] Update WebSocket URL if using voice features
- [ ] Test CORS settings
- [ ] Verify authentication flow works
- [ ] Test all API endpoints from frontend

### Frontend Files to Update
```javascript
// Example: Update in paco-frontend/lib/api.ts or similar
const API_URL = 'https://paco-api.onrender.com'
```

- [ ] Find and update API base URL
- [ ] Update WebSocket connection URL
- [ ] Redeploy frontend
- [ ] Test end-to-end flow

## 🎯 Performance Verification

### Free Tier Considerations
- [ ] Understand 15-minute spin-down behavior
- [ ] First request may take 30-60 seconds
- [ ] Consider upgrade if always-on is needed

### Load Testing (Optional)
- [ ] Test with multiple simultaneous requests
- [ ] Monitor response times
- [ ] Check database connection pool

## 📊 Monitoring Setup

### Render Dashboard
- [ ] Bookmark service URL
- [ ] Bookmark logs page
- [ ] Set up email notifications (if available)

### Logging
- [ ] Review logs for any warnings
- [ ] No repeated errors
- [ ] Migrations log clean
- [ ] Application startup logs clean

## 🔐 Security Checklist

### Secrets Management
- [ ] No secrets in code
- [ ] All secrets in environment variables
- [ ] SECRET_KEY is strong and unique
- [ ] API keys are valid and active

### Access Control
- [ ] JWT authentication working
- [ ] Token expiration configured
- [ ] CORS configured for frontend domain

### HTTPS
- [ ] All endpoints use HTTPS
- [ ] SSL certificate active (auto by Render)
- [ ] No mixed content warnings

## 📚 Documentation Updated

### Project Documentation
- [ ] README updated with Render URL
- [ ] API documentation reflects production URL
- [ ] Architecture diagrams updated
- [ ] Deployment guide accessible to team

### Team Communication
- [ ] Team notified of new deployment
- [ ] Production URL shared
- [ ] Access credentials distributed securely
- [ ] Support contacts documented

## 🆘 Troubleshooting Ready

### Common Issues Prepared For
- [ ] Know how to view logs
- [ ] Know how to restart service
- [ ] Know how to rollback deployment
- [ ] Have backup contact for Render support

### Emergency Contacts
- [ ] Render support: https://render.com/support
- [ ] Team lead contact: __________
- [ ] Database admin: __________

## 🎉 Success Criteria

All of these should be ✓ before considering deployment successful:
- [ ] Service is Live
- [ ] All health checks pass
- [ ] Frontend can connect to backend
- [ ] Authentication works
- [ ] Database queries work
- [ ] External API integrations work
- [ ] No errors in logs
- [ ] Team has been notified
- [ ] Documentation updated

---

## 📝 Notes Section

Add any deployment-specific notes here:

**Deployment Date:** _____________

**Service URL:** _____________

**Database URL:** _____________

**Deployed By:** _____________

**Version/Commit:** _____________

**Issues Encountered:** 
- 

**Resolutions:**
- 

**Next Steps:**
- 

---

## 🔄 For Next Deployment

Things to remember for next time:
- [ ] Review this checklist
- [ ] Check for Render platform updates
- [ ] Review dependency updates
- [ ] Test in staging first (if applicable)
- [ ] Schedule deployment during low-traffic window

---

**Last Updated:** January 27, 2026
**Checklist Version:** 1.0
