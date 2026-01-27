# PaCo - Patient Communication Chatbot

An AI-powered healthcare communication platform for research, featuring ElevenLabs voice conversations, medication adherence analysis, and secure patient data tracking.

> **Database Note**: This project uses **Neon PostgreSQL** (free serverless PostgreSQL) for the database. The backend API is deployed on Railway, giving you the best of both: free database + affordable compute.

## Core Features

- **ElevenLabs Voice Chat**: Natural voice conversations with AI assistant
- **Medication Analysis**: NLP-powered analysis of medication adherence from conversations
- **Research ID System**: Secure authentication for research participants
- **Admin Dashboard**: Manage research IDs and analyze patient data
- **PostgreSQL Database**: Track all conversations for research analysis
- **HIPAA-Aware Design**: Patient safety-first architecture

## Architecture

- **Frontend**: Next.js 14 + TypeScript + Tailwind CSS (Deployed on Vercel)
- **Backend**: FastAPI + Python 3.11 (Deployed on Railway)
- **Database**: Neon PostgreSQL (Free serverless PostgreSQL)
- **AI Services**: ElevenLabs Conversational AI + OpenAI GPT-4

## Quick Start - Local Development

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL database
- ElevenLabs API key
- OpenAI API key (for medication analysis)

### Backend Setup

```bash
# Navigate to backend
cd paco-api

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cat > .env << EOF
DATABASE_URL=postgresql://user:password@localhost:5432/paco_db
JWT_SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
ADMIN_PASSWORD=your_secure_admin_password
OPENAI_API_KEY=sk-...
ELEVENLABS_API_KEY=your_elevenlabs_key
CORS_ORIGINS=["http://localhost:3000"]
EOF

# Run database migrations
alembic upgrade head

# Seed initial research IDs (optional)
python scripts/seed_research_ids.py

# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
# Navigate to frontend
cd paco-frontend

# Install dependencies
npm install

# Set up environment variables
cat > .env.local << EOF
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
NEXT_PUBLIC_ELEVENLABS_AGENT_ID=your_agent_id
EOF

# Start development server
npm run dev
```

Visit http://localhost:3000

## Project Structure

```
PatientCommunication/
├── paco-api/                  # FastAPI backend
│   ├── app/
│   │   ├── api/endpoints/     # API routes
│   │   │   ├── auth.py        # Authentication
│   │   │   ├── chat.py        # ElevenLabs message sync
│   │   │   ├── admin.py       # Admin management
│   │   │   └── medication_analysis.py
│   │   ├── core/              # Configuration & security
│   │   ├── models/            # Database models
│   │   ├── schemas/           # Pydantic schemas
│   │   └── services/          # Business logic
│   ├── alembic/               # Database migrations
│   └── requirements.txt
├── paco-frontend/             # Next.js frontend
│   ├── app/                   # Next.js app directory
│   ├── components/
│   │   ├── ResearchIDScreen.tsx
│   │   ├── DisclaimerScreen.tsx
│   │   └── ElevenLabsWidget.tsx  # Main chat interface
│   ├── lib/api.ts            # API client
│   └── types/                # TypeScript types
└── DEPLOYMENT.md             # Deployment guide
```

## Database Models

- **ResearchID**: Authorized research participants
- **UserSession**: Active JWT sessions
- **DisclaimerAcknowledgment**: Research consent tracking
- **Conversation**: All chat messages (user + assistant)
- **MedicationAdherenceAnalysis**: NLP analysis results

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - Login with research ID
- `POST /api/v1/auth/validate` - Validate research ID
- `POST /api/v1/auth/disclaimer` - Acknowledge disclaimer

### Chat
- `POST /api/v1/chat/save-message` - Save ElevenLabs messages
- `POST /api/v1/chat/sync-elevenlabs-conversation` - Sync full conversation
- `GET /api/v1/chat/conversations/elevenlabs` - List conversations
- `POST /api/v1/chat/history` - Get conversation history

### Admin (Password Protected)
- `POST /api/v1/admin/research-ids` - Create research ID
- `GET /api/v1/admin/research-ids` - List all research IDs
- `PUT /api/v1/admin/research-ids/{id}` - Update research ID
- `DELETE /api/v1/admin/research-ids/{id}` - Deactivate research ID
- `GET /api/v1/admin/stats` - System statistics

### Medication Analysis (Password Protected)
- `POST /api/v1/medication-analysis/analyze` - Analyze adherence

## Environment Variables

### Backend (.env)
```bash
# Database
DATABASE_URL=postgresql://user:password@host:5432/database

# Security
JWT_SECRET_KEY=your_secret_key
ADMIN_PASSWORD=your_admin_password

# APIs
OPENAI_API_KEY=sk-...
ELEVENLABS_API_KEY=...

# CORS
CORS_ORIGINS=["https://your-frontend.vercel.app"]
```

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=https://your-backend.railway.app/api/v1
NEXT_PUBLIC_ELEVENLABS_AGENT_ID=your_agent_id
```

## Security Features

- JWT-based authentication with expiry
- Research ID validation
- Admin password protection for sensitive endpoints
- CORS protection
- SQL injection prevention (SQLAlchemy ORM)
- Secure session management

## Development Commands

### Backend
```bash
# Run migrations
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "description"

# Run tests
pytest

# Format code
black app/
```

### Frontend
```bash
# Development
npm run dev

# Build
npm run build

# Lint
npm run lint
```

## License

MIT License - See LICENSE file for details

## Deployment Costs

**Extremely affordable for research projects!**

- **Database (Neon)**: FREE forever
- **Backend (Railway)**: ~$5-10/month
- **Frontend (Vercel)**: FREE
- **APIs (ElevenLabs + OpenAI)**: $5-30/month depending on usage

**Total: ~$15-40/month** for complete infrastructure

See [COSTS.md](COSTS.md) for detailed breakdown and optimization tips.

## Support

For issues or questions, please open a GitHub issue.
