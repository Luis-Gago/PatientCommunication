# PaCo - Patient Communication - Render Deployment Ready

**Status**: ✅ Refactored for Render Deployment  
**Last Updated**: January 27, 2026

PaCo is a multi-user FastAPI backend with Next.js frontend for patient-provider communication with AI-powered medication adherence analysis.

## 🚀 Quick Start - Deploy on Render

### One-Click Blueprint Deployment

1. Push code to GitHub
2. Go to https://render.com/dashboard
3. Click "New +" → "Blueprint"
4. Select your GitHub repository
5. Click "Apply"

That's it! Render will automatically create and deploy:
- ✅ FastAPI backend (paco-api)
- ✅ Next.js frontend (paco-frontend)
- ✅ PostgreSQL database (paco-db)

**See [RENDER_DEPLOYMENT_CHECKLIST.md](RENDER_DEPLOYMENT_CHECKLIST.md) for detailed steps** (~30 minutes)

---

## 📚 Documentation

### Getting Started
- **[RENDER_DEPLOYMENT_CHECKLIST.md](RENDER_DEPLOYMENT_CHECKLIST.md)** - Quick reference checklist ⭐ START HERE
- **[RENDER_SETUP.md](RENDER_SETUP.md)** - Step-by-step setup guide

### Deployment Guides
- **[RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)** - Complete deployment guide
- **[RENDER_TROUBLESHOOTING.md](RENDER_TROUBLESHOOTING.md)** - Troubleshooting common issues

### Migration Guides
- **[RAILWAY_TO_RENDER_MIGRATION.md](RAILWAY_TO_RENDER_MIGRATION.md)** - Migrate from Railway + Neon + Vercel
- **[RENDER_REFACTORING_SUMMARY.md](RENDER_REFACTORING_SUMMARY.md)** - What changed in the refactoring

### Legacy Documentation
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Original Railway deployment guide (legacy)
- **[LOCAL_SETUP.md](LOCAL_SETUP.md)** - Local development setup

---

## 🏗️ Project Structure

```
PatientCommunication/
├── render.yaml                          # Render Blueprint config
├── RENDER_SETUP.md                      # Setup guide
├── RENDER_DEPLOYMENT.md                 # Full deployment guide
├── RENDER_TROUBLESHOOTING.md            # Troubleshooting
├── RAILWAY_TO_RENDER_MIGRATION.md       # Migration guide
├── RENDER_REFACTORING_SUMMARY.md        # What changed
│
├── paco-api/                            # FastAPI Backend
│   ├── app/                             # Main application
│   │   ├── main.py                      # FastAPI app
│   │   ├── core/                        # Config, security
│   │   ├── api/                         # API endpoints
│   │   ├── models/                      # Database models
│   │   ├── schemas/                     # Request/response schemas
│   │   ├── services/                    # Business logic
│   │   └── db/                          # Database setup
│   ├── alembic/                         # Database migrations
│   ├── scripts/                         # Utility scripts
│   ├── requirements.txt                 # Python dependencies
│   ├── build.sh                         # Render build script
│   ├── start.sh                         # Render start script
│   ├── Procfile                         # Process definition
│   └── runtime.txt                      # Python version
│
├── paco-frontend/                       # Next.js Frontend
│   ├── app/                             # Next.js app directory
│   │   ├── layout.tsx                   # Root layout
│   │   ├── page.tsx                     # Main page
│   │   └── globals.css                  # Global styles
│   ├── components/                      # React components
│   ├── lib/                             # Utilities
│   ├── types/                           # TypeScript types
│   ├── package.json                     # Node dependencies
│   ├── render.json                      # Frontend config reference
│   ├── next.config.ts                   # Next.js config
│   └── tsconfig.json                    # TypeScript config
│
└── README.md                            # This file
```

---

## 🎯 Key Features

- **FastAPI Backend** - High-performance Python web framework
- **PostgreSQL Database** - Robust relational database
- **Next.js Frontend** - React framework with SSR
- **Real-time Communication** - WebSocket support
- **AI-Powered Features** - GROQ LLM integration
- **Voice Integration** - ElevenLabs voice API
- **User Authentication** - JWT-based auth
- **Research ID Tracking** - HIPAA-compliant tracking
- **Database Migrations** - Alembic version control

---

## 🔧 Environment Setup

### Required Environment Variables

**Backend (paco-api)**
```
DATABASE_URL=postgresql://user:pass@host:5432/db
SECRET_KEY=[generated-secret-key]
GROQ_API_KEY=[your-groq-api-key]
ELEVENLABS_API_KEY=[your-elevenlabs-key]
CORS_ORIGINS=https://paco-frontend.onrender.com
```

**Frontend (paco-frontend)**
```
NEXT_PUBLIC_API_URL=https://paco-api.onrender.com/api/v1
NEXT_PUBLIC_ELEVENLABS_AGENT_ID=[your-agent-id]
```

See [RENDER_SETUP.md](RENDER_SETUP.md) for detailed environment setup.

---

## 🚀 Deployment Options

### Option 1: Render (Recommended) ⭐
- **Setup Time**: ~30 minutes
- **Cost**: Free tier (limited) or $7+/month
- **Pros**: All-in-one, simple, integrated database
- **Status**: ✅ Ready to deploy

See [RENDER_DEPLOYMENT_CHECKLIST.md](RENDER_DEPLOYMENT_CHECKLIST.md)

### Option 2: Railway (Legacy)
- **Setup Time**: ~45 minutes
- **Cost**: $5+/month
- **Pros**: Familiar if already set up
- **Status**: ✅ Still supported but not recommended

See [DEPLOYMENT.md](DEPLOYMENT.md)

### Option 3: Local Development
- **Setup Time**: ~20 minutes
- **Cost**: Free
- **Pros**: Full control, easy debugging
- **Status**: ✅ Supported

See [LOCAL_SETUP.md](LOCAL_SETUP.md)

---

## 📋 Deployment Checklist

### Pre-Deployment
- [ ] Code committed and pushed to GitHub
- [ ] `render.yaml` exists in root directory
- [ ] Collect API keys (GROQ, ElevenLabs)
- [ ] Generate SECRET_KEY
- [ ] Render account created

### Deployment
- [ ] Create Blueprint from render.yaml
- [ ] Set environment variables
- [ ] Wait for services to deploy
- [ ] Verify all services show "Live"

### Post-Deployment
- [ ] Test health endpoint: `/health`
- [ ] Test API docs: `/docs`
- [ ] Open frontend in browser
- [ ] Test basic functionality
- [ ] Monitor logs for 24-48 hours

See [RENDER_DEPLOYMENT_CHECKLIST.md](RENDER_DEPLOYMENT_CHECKLIST.md) for complete checklist.

---

## 🐛 Troubleshooting

### Common Issues

**Services won't deploy**
- Check logs in Render dashboard
- Verify environment variables are set
- Ensure all dependencies are in requirements.txt/package.json

**Database connection fails**
- Verify DATABASE_URL is set correctly
- Check paco-db service is "Available"
- Test connection via Render Shell

**Frontend can't reach backend**
- Verify NEXT_PUBLIC_API_URL is correct
- Check backend CORS_ORIGINS includes frontend domain
- Test backend health endpoint: `curl https://paco-api.onrender.com/health`

**See [RENDER_TROUBLESHOOTING.md](RENDER_TROUBLESHOOTING.md) for comprehensive troubleshooting guide**

---

## 📖 API Documentation

Once deployed, access API documentation at:
```
https://paco-api.onrender.com/docs        # Swagger UI
https://paco-api.onrender.com/redoc       # ReDoc
```

### Key Endpoints

- `GET /health` - Health check
- `GET /docs` - API documentation
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/chat/message` - Send message
- `POST /api/v1/medication-analysis/analyze` - Medication analysis

---

## 🔐 Security Notes

- **Never commit `.env` files** - Use Render environment variables
- **Keep API keys secure** - Don't share or expose in logs
- **Use HTTPS only** - Render provides free SSL/TLS
- **CORS configured** - Only allows specified frontend domain
- **JWT authentication** - Secure token-based auth

---

## 📊 Monitoring & Maintenance

### Monitor Your Deployment

1. **Render Dashboard**: https://dashboard.render.com
2. **View Logs**: Service → Logs tab
3. **Check Status**: Service status page
4. **Monitor Events**: Service → Events tab

### Regular Maintenance

- Review logs weekly for errors
- Monitor database performance
- Keep dependencies updated
- Backup database periodically
- Update API keys if compromised

---

## 💰 Cost Breakdown

### Free Tier (Suitable for Dev/Testing)
- Backend: $0 (auto-spins down, 30-60s cold start)
- Frontend: $0 (auto-spins down, 30-60s cold start)
- Database: $0 (PostgreSQL included, always-on)
- **Total: $0/month** ⚠️ (with limitations)

### Paid Tier (Recommended for Production)
- Backend: $7+/month (always-on, better resources)
- Frontend: $7+/month (always-on, better resources)
- Database: Included (always-on)
- **Total: $14+/month**

See [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) for cost comparison.

---

## 🔄 Update & Redeploy

### To update your deployment:

1. Make code changes locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update message"
   git push origin main
   ```
3. Render automatically redeploys (if auto-deploy enabled)
4. Or manually trigger in dashboard

---

## 📞 Support & Resources

- **Render Docs**: https://render.com/docs
- **Render Support**: https://render.com/support
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Next.js Docs**: https://nextjs.org/docs
- **PostgreSQL Docs**: https://www.postgresql.org/docs

---

## 🎓 Learning Resources

### Backend (FastAPI)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/en/20/orm/quickstart.html)
- [Alembic Migrations](https://alembic.sqlalchemy.org/en/latest/)

### Frontend (Next.js)
- [Next.js Getting Started](https://nextjs.org/docs/getting-started)
- [React Hooks](https://react.dev/reference/react/hooks)
- [Tailwind CSS](https://tailwindcss.com/docs)

### Database (PostgreSQL)
- [PostgreSQL Tutorial](https://www.postgresql.org/docs/current/tutorial.html)
- [Connection Strings](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING)

---

## 📝 License

[Add your license information here]

---

## 🤝 Contributing

[Add contribution guidelines]

---

## 📜 Version History

### v1.0.0 - January 27, 2026
- ✅ Refactored for Render deployment
- ✅ Added comprehensive documentation
- ✅ Created migration guides from Railway
- ✅ Added troubleshooting guides
- ✅ Automated Blueprint deployment support

### v0.x.x (Railway)
- Legacy Railway + Neon + Vercel deployment
- See [DEPLOYMENT.md](DEPLOYMENT.md) for details

---

## 🎯 Next Steps

1. **Read the Quick Start**: [RENDER_DEPLOYMENT_CHECKLIST.md](RENDER_DEPLOYMENT_CHECKLIST.md)
2. **Follow Setup Guide**: [RENDER_SETUP.md](RENDER_SETUP.md)
3. **Deploy to Render**: Create Blueprint with render.yaml
4. **Test Deployment**: Verify all services working
5. **Monitor Performance**: Check logs and metrics

---

**Questions?** See [RENDER_TROUBLESHOOTING.md](RENDER_TROUBLESHOOTING.md) or check Render documentation.

**Happy Deploying! 🚀**
