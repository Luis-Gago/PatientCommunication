# PaCo System Architecture

## Overview

PaCo is a healthcare research platform that enables natural voice conversations between patients and an AI assistant, with comprehensive medication adherence analysis capabilities. The system is designed with patient safety, data security, and research compliance as primary concerns.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend                             │
│                  (Next.js + TypeScript)                      │
│                    Vercel Deployment                         │
│                                                              │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ Research ID │→ │  Disclaimer  │→ │ ElevenLabs Widget│  │
│  │   Screen    │  │    Screen    │  │   (Voice Chat)   │  │
│  └─────────────┘  └──────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                          ↓ HTTPS
┌─────────────────────────────────────────────────────────────┐
│                      Backend API                             │
│                   (FastAPI + Python)                         │
│                   Railway Deployment                         │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌────────────┐  ┌──────────┐ │
│  │   Auth   │  │   Chat   │  │   Admin    │  │  Med AI  │ │
│  │ Endpoints│  │ Endpoints│  │ Endpoints  │  │ Analysis │ │
│  └──────────┘  └──────────┘  └────────────┘  └──────────┘ │
│       ↓             ↓              ↓               ↓        │
│  ┌───────────────────────────────────────────────────────┐ │
│  │              Services Layer                            │ │
│  │  - Conversation Service                                │ │
│  │  - Medication Analysis Service                         │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                    PostgreSQL Database                       │
│                   (Railway Managed)                          │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │ Research IDs │  │Conversations │  │  Medication     │  │
│  │   & Auth     │  │  & Messages  │  │  Analysis       │  │
│  └──────────────┘  └──────────────┘  └─────────────────┘  │
└─────────────────────────────────────────────────────────────┘

External Services:
┌──────────────┐  ┌──────────────┐
│  ElevenLabs  │  │    OpenAI    │
│   Voice AI   │  │   GPT-4 API  │
│   (Conv AI)  │  │  (Analysis)  │
└──────────────┘  └──────────────┘
```

## Technology Stack

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: React Hooks
- **Deployment**: Vercel
- **Key Libraries**:
  - ElevenLabs Conversational AI Widget
  - next/script for third-party scripts

### Backend
- **Framework**: FastAPI 0.104+
- **Language**: Python 3.11
- **Database ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **Authentication**: JWT (python-jose)
- **Deployment**: Railway
- **Key Libraries**:
  - httpx (async HTTP client)
  - pydantic (data validation)
  - passlib (password hashing)

### Database
- **System**: PostgreSQL 14+
- **Hosting**: Railway Managed PostgreSQL
- **Backup**: Automatic daily backups

### External APIs
- **ElevenLabs**: Conversational AI (voice chat)
- **OpenAI**: GPT-4 (medication analysis)

## Database Schema

### Core Tables

#### paco_research_ids
```sql
id               SERIAL PRIMARY KEY
research_id      VARCHAR(50) UNIQUE NOT NULL
created_at       TIMESTAMP WITH TIME ZONE
is_active        BOOLEAN DEFAULT TRUE
notes            TEXT
```

#### paco_conversations
```sql
id                          SERIAL PRIMARY KEY
research_id_fk              INTEGER REFERENCES paco_research_ids(id)
conversation_id             VARCHAR(255) NOT NULL
timestamp                   TIMESTAMP WITH TIME ZONE
role                        VARCHAR(20) NOT NULL
content                     TEXT NOT NULL
provider                    VARCHAR(20)
elevenlabs_conversation_id  VARCHAR(255)
elevenlabs_message_id       VARCHAR(255)
```

#### paco_medication_adherence
```sql
id                      SERIAL PRIMARY KEY
research_id_fk          INTEGER REFERENCES paco_research_ids(id)
analysis_date           TIMESTAMP WITH TIME ZONE
analyzed_from           TIMESTAMP WITH TIME ZONE
analyzed_to             TIMESTAMP WITH TIME ZONE
detailed_analysis       JSONB
confidence_score        FLOAT
```

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
- `GET /api/v1/medication-analysis/history/{research_id}` - Get analysis history

## Security Architecture

### Authentication
- **JWT Tokens**: 24-hour expiration
- **Research IDs**: Validated against database
- **Admin Endpoints**: Password-protected
- **Session Tracking**: Active sessions in database

### Data Protection
- **HTTPS Only**: All traffic encrypted
- **CORS**: Restricted to approved origins
- **SQL Injection**: Prevented by SQLAlchemy ORM
- **Input Validation**: Pydantic schemas

## Deployment

### Railway (Backend)
- Automatic deployment from GitHub
- Database migrations on startup
- Health checks enabled
- Auto-scaling

### Vercel (Frontend)
- Automatic deployment from GitHub
- CDN distribution
- Edge network
- Serverless functions

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.
