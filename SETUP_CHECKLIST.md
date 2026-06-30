# PaCo — Local Setup Checklist

Things a new developer needs to run PaCo locally. The environment (Python 3.12 venv +
dependencies) is already built and verified on this machine; what remains is supplying
secrets that are **not** stored in the repo.

## 🔴 Required — backend will not start without these

| Item | Env variable | Where to get it |
|------|-------------|-----------------|
| Database connection string (incl. password) | `DATABASE_URL` | Render dashboard → `paco-api` service → Environment, **or** the Neon console. The existing study DB is `ep-wandering-sea-a5xid0o5.us-east-2.aws.neon.tech/neondb` (user `neondb_owner`). |
| Groq API key | `GROQ_API_KEY` | https://console.groq.com |
| Gemini API key | `GEMINI_API_KEY` | https://aistudio.google.com/apikey |
| OpenAI API key | `OPENAI_API_KEY` | https://platform.openai.com/api-keys |

> At least one LLM key is mandatory; this project uses all three (fallback order: Gemini → OpenAI → Groq).

## 🟡 Required for voice features

| Item | Env variable | Notes |
|------|-------------|-------|
| ElevenLabs API key | `ELEVENLABS_API_KEY` (backend) + `NEXT_PUBLIC_ELEVENLABS_API_KEY` (frontend) | https://elevenlabs.io |
| ElevenLabs Agent ID | `ELEVENLABS_AGENT_ID` (backend) + `NEXT_PUBLIC_ELEVENLABS_AGENT_ID` (frontend) | The Conversational AI agent for this study |

## 🟢 Account/login access to request

- **Render** — backend host + production env vars (and the `DATABASE_URL`)
- **Vercel** — frontend host + its env vars
- **Neon** — the database (connection string, backups, SQL access)
- **ElevenLabs** — to view/manage the conversational agent
- (Optional) the production `SECRET_KEY`, only if you need local JWTs to match production

## ⚪ You do NOT need to ask anyone for these

- `SECRET_KEY` — generate locally: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
- `ADMIN_PASSWORD` — pick any value (used by the admin API)
- `ALGORITHM`, token expiry, `CORS_ORIGINS`, ElevenLabs voice/model IDs — defaults exist
- Research login IDs (RID001–RID005) — seeded into the DB by `scripts/seed_research_ids.py`

## ❓ Ask the team explicitly

> Is there a separate **dev/staging database**, or is `ep-wandering-sea-a5xid0o5` the **live study database**?

If it's the live DB with real research data, do **not** point local dev at it (migrations/seed
scripts could modify it). Request a dev database or permission to create a fresh empty one.

---

## Repository fixes already applied

`paco-api/requirements.txt` was internally broken (the multi-LLM commit added Gemini/OpenAI
providers the app imports on startup, but their packages and a compatible `httpx` were missing).
Fixed on this machine:

- `httpx==0.27.0` → `httpx>=0.28.1` (required by `google-genai`)
- `websockets==12.0` → `websockets>=13.0` (required by `google-genai`)
- `groq==0.5.0` → `groq>=0.13.0` (old groq breaks on httpx ≥ 0.28: `proxies` kwarg removed)
- added `openai>=1.30.0` and `google-genai>=1.0.0` (imported by the code, previously undeclared)

These changes should be committed and reflected in the Render build.

## Run order (once secrets are in `.env`)

```powershell
cd paco-api
# .venv already created with Python 3.12
.\.venv\Scripts\Activate.ps1
$env:PYTHONIOENCODING="utf-8"   # Windows: avoids emoji-in-print crash at startup
alembic upgrade head            # create tables
python scripts\seed_research_ids.py
uvicorn app.main:app --reload --port 8000

# frontend (separate terminal)
cd ..\paco-frontend
npm install
npm run dev                     # http://localhost:3000
```
