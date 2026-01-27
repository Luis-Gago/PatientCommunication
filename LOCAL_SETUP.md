# Local Development Setup

Step-by-step guide to run PaCo locally for development.

> **Database Note**: For local development, you can use either local PostgreSQL or Neon PostgreSQL (free). For production deployment, see [DEPLOYMENT.md](DEPLOYMENT.md) which uses Neon PostgreSQL + Railway backend.

## Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+ (installed and running)
- Git

## Step 1: Clone Repository

```bash
git clone https://github.com/your-username/PatientCommunication.git
cd PatientCommunication
```

## Step 2: Database Setup

### Option A: Local PostgreSQL

```bash
# Create database
createdb paco_dev

# Or using psql
psql postgres
CREATE DATABASE paco_dev;
\q
```

### Option B: Neon PostgreSQL (Recommended - Free)

1. Go to https://console.neon.tech
2. Create a free account and new project
3. Copy the connection string from your project dashboard
4. Paste it into your `.env` file

## Step 3: Backend Setup

```bash
cd paco-api

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << 'EOF'
# Database
DATABASE_URL=postgresql://localhost:5432/paco_dev

# Security
JWT_SECRET_KEY=dev_secret_key_change_in_production
ADMIN_PASSWORD=admin123

# AI Services
OPENAI_API_KEY=sk-your-openai-key
ELEVENLABS_API_KEY=your-elevenlabs-key

# CORS
CORS_ORIGINS=["http://localhost:3000"]

# Python
PYTHONPATH=/app
EOF

# Run database migrations
alembic upgrade head

# (Optional) Seed test data
python scripts/seed_research_ids.py

# Start backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be running at: http://localhost:8000

API Docs: http://localhost:8000/docs

## Step 4: Frontend Setup

```bash
# Open new terminal
cd paco-frontend

# Install dependencies
npm install

# Create .env.local
cat > .env.local << 'EOF'
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_ELEVENLABS_AGENT_ID=your_agent_id_here
EOF

# Start development server
npm run dev
```

Frontend will be running at: http://localhost:3000

## Step 5: Create Test Research IDs

### Method A: Using API

```bash
curl -X POST http://localhost:8000/api/v1/admin/research-ids \
  -H "Content-Type: application/json" \
  -d '{
    "password": "admin123",
    "research_id": "TEST_001",
    "notes": "Test patient for development",
    "is_active": true
  }'
```

### Method B: Using Database

```bash
psql paco_dev

INSERT INTO paco_research_ids (research_id, is_active, notes)
VALUES ('TEST_001', true, 'Test patient');

\q
```

### Method C: Using Seed Script

```bash
cd paco-api
python scripts/seed_research_ids.py
```

This creates IDs: `PATIENT_001`, `PATIENT_002`, `PATIENT_003`

## Step 6: Test the Application

1. Visit http://localhost:3000
2. Enter research ID: `TEST_001` or `PATIENT_001`
3. Accept disclaimer
4. Start conversation with ElevenLabs chatbot

## Common Development Commands

### Backend

```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run server with auto-reload
uvicorn app.main:app --reload

# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Check migration status
alembic current

# View migration history
alembic history

# Run Python shell with app context
python
>>> from app.db.base import engine
>>> from app.models.database import *
```

### Frontend

```bash
# Development mode
npm run dev

# Build for production
npm run build

# Run production build locally
npm start

# Lint code
npm run lint

# Type check
npx tsc --noEmit
```

## Environment Variables Explained

### Backend (.env)

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Yes | - |
| `JWT_SECRET_KEY` | Secret key for JWT tokens | Yes | - |
| `ADMIN_PASSWORD` | Password for admin endpoints | Yes | - |
| `OPENAI_API_KEY` | OpenAI API key for medication analysis | Yes | - |
| `ELEVENLABS_API_KEY` | ElevenLabs API key | Yes | - |
| `CORS_ORIGINS` | Allowed frontend origins (JSON array) | Yes | `["http://localhost:3000"]` |
| `PYTHONPATH` | Python module path | No | `/app` |

### Frontend (.env.local)

| Variable | Description | Required |
|----------|-------------|----------|
| `NEXT_PUBLIC_API_URL` | Backend API base URL | Yes |
| `NEXT_PUBLIC_ELEVENLABS_AGENT_ID` | ElevenLabs conversational AI agent ID | Yes |

## Development Tips

### Hot Reload

- **Backend**: FastAPI auto-reloads on file changes (with `--reload`)
- **Frontend**: Next.js auto-reloads on file changes

### Debugging

#### Backend

Add breakpoints using:
```python
import pdb; pdb.set_trace()
```

Or use VS Code debugger with this launch.json:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["app.main:app", "--reload"],
      "cwd": "${workspaceFolder}/paco-api"
    }
  ]
}
```

#### Frontend

Use browser DevTools:
- Console for logs
- Network tab for API calls
- React DevTools extension

### Database Tools

#### View Database

```bash
# Connect to database
psql paco_dev

# List tables
\dt

# View table structure
\d paco_research_ids

# Query data
SELECT * FROM paco_research_ids;
SELECT * FROM paco_conversations ORDER BY timestamp DESC LIMIT 10;

# Exit
\q
```

#### GUI Tools

- **pgAdmin**: https://www.pgadmin.org/
- **DBeaver**: https://dbeaver.io/
- **TablePlus**: https://tableplus.com/

### Testing API Endpoints

Use the interactive API docs at http://localhost:8000/docs

Or use curl:

```bash
# Health check
curl http://localhost:8000/health

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"research_id": "TEST_001"}'

# Get conversation history
TOKEN="your_jwt_token"
curl http://localhost:8000/api/v1/chat/history \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "research_id": "TEST_001",
    "conversation_id": "conv_123",
    "limit": 20
  }'
```

## Project Structure

```
PatientCommunication/
├── paco-api/                    # Backend (FastAPI)
│   ├── alembic/                 # Database migrations
│   │   └── versions/            # Migration files
│   ├── app/
│   │   ├── api/endpoints/       # API routes
│   │   │   ├── auth.py          # Authentication
│   │   │   ├── chat.py          # Chat/conversation
│   │   │   ├── admin.py         # Admin management
│   │   │   └── medication_analysis.py
│   │   ├── core/                # Config & security
│   │   │   ├── config.py
│   │   │   └── security.py
│   │   ├── models/              # Database models
│   │   │   └── database.py
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── services/            # Business logic
│   │   │   ├── conversation_service.py
│   │   │   └── medication_analysis_service.py
│   │   ├── db/                  # Database setup
│   │   └── main.py              # FastAPI app
│   ├── scripts/                 # Utility scripts
│   ├── requirements.txt
│   ├── alembic.ini
│   └── .env                     # Environment variables
│
├── paco-frontend/               # Frontend (Next.js)
│   ├── app/                     # Next.js app directory
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   └── page.tsx             # Main app component
│   ├── components/              # React components
│   │   ├── ResearchIDScreen.tsx
│   │   ├── DisclaimerScreen.tsx
│   │   └── ElevenLabsWidget.tsx # Main chat interface
│   ├── lib/
│   │   └── api.ts               # API client functions
│   ├── types/
│   │   └── index.ts             # TypeScript types
│   ├── package.json
│   └── .env.local               # Environment variables
│
├── README.md                    # Main documentation
├── DEPLOYMENT.md                # Deployment guide
├── LOCAL_SETUP.md               # This file
└── architecture.md              # System architecture
```

## Troubleshooting

### Backend won't start

**Error: "No module named 'app'"**
```bash
# Make sure you're in paco-api directory
cd paco-api

# Verify PYTHONPATH
export PYTHONPATH=$(pwd)
```

**Error: "Could not connect to database"**
```bash
# Check PostgreSQL is running
pg_isready

# Verify DATABASE_URL in .env
cat .env | grep DATABASE_URL

# Test connection
psql $DATABASE_URL
```

**Error: "Migration failed"**
```bash
# Reset database (WARNING: deletes all data)
alembic downgrade base
alembic upgrade head

# Or recreate database
dropdb paco_dev
createdb paco_dev
alembic upgrade head
```

### Frontend issues

**Error: "API connection failed"**
1. Check backend is running: `curl http://localhost:8000/health`
2. Verify `NEXT_PUBLIC_API_URL` in `.env.local`
3. Check browser console for CORS errors

**Error: "ElevenLabs widget not loading"**
1. Verify `NEXT_PUBLIC_ELEVENLABS_AGENT_ID` is set
2. Check ElevenLabs API key is valid in backend
3. Open browser DevTools → Console for errors

### Database issues

**Reset database completely**
```bash
# Drop and recreate
dropdb paco_dev
createdb paco_dev

# Run migrations
cd paco-api
alembic upgrade head

# Seed test data
python scripts/seed_research_ids.py
```

## Next Steps

- Read [architecture.md](architecture.md) to understand the system design
- Review [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- Check API documentation at http://localhost:8000/docs
- Explore the database schema in `paco-api/app/models/database.py`

## Getting Help

- Check the [README.md](README.md) for general information
- Review FastAPI docs: https://fastapi.tiangolo.com/
- Review Next.js docs: https://nextjs.org/docs
- Open an issue on GitHub for bugs

Happy coding! 🚀
