# Medication Adherence Analysis Tool

## Overview

The Medication Adherence Analysis Tool is an NLP-powered system that analyzes patient conversations from ElevenLabs chatbot interactions to extract meaningful insights about medication adherence. This tool helps medical providers quickly understand patient compliance, identify barriers, and track concerns.

## Features

The analysis extracts the following information from patient conversations:

1. **Medications**: Names and dosages of medications mentioned
2. **Timing Schedule**: When patients take their medications (morning, afternoon, evening, as-needed)
3. **Side Effects**: Reported adverse effects with severity levels
4. **Adherence Difficulties**: Problems preventing proper medication taking (forgetting, cost, access, etc.)
5. **Adherence Strategies**: Methods patients use to remember medications (alarms, pill boxes, routines)
6. **Questions & Concerns**: Patient questions about their medications
7. **Overall Adherence Status**: High-level assessment of medication compliance
8. **Confidence Score**: AI confidence level (0-100) in the analysis
9. **Provider Summary**: Brief summary for quick provider review
10. **Key Concerns**: Most important issues requiring provider attention
11. **Recommendations**: Suggested follow-up actions

## API Endpoints

All endpoints require admin authentication via the `password` query parameter or request body.

### 1. Analyze Conversations

**POST** `/api/v1/medication-analysis/analyze?password=YOUR_ADMIN_PASSWORD`

Performs NLP analysis on patient conversations.

**Request Body:**
```json
{
  "research_id": "PACO-001",
  "start_date": "2025-01-01T00:00:00",
  "end_date": "2025-01-26T23:59:59",
  "model": "gpt-4o"
}
```

**Parameters:**
- `research_id` (required): Patient's research ID
- `start_date` (optional): Start date for conversation analysis
- `end_date` (optional): End date for conversation analysis
- `model` (optional): LLM model to use (default: "gpt-4o")

**Response:**
```json
{
  "analysis_id": 1,
  "research_id": "PACO-001",
  "analysis_date": "2025-01-26T14:30:00Z",
  "analyzed_from": "2025-01-01T00:00:00Z",
  "analyzed_to": "2025-01-26T23:59:59Z",
  "conversation_count": 15,
  "confidence_score": 85,
  "summary": "Patient reports taking medications regularly but experiencing morning drowsiness...",
  "model_used": "gpt-4o",
  "result": {
    "medications": [
      {
        "name": "Metformin",
        "dosage": "500mg",
        "mentioned_by_patient": true
      }
    ],
    "timing_schedule": {
      "morning": ["Metformin"],
      "afternoon": [],
      "evening": ["Blood pressure medication"],
      "as_needed": [],
      "unclear": []
    },
    "side_effects": [
      {
        "medication": "Metformin",
        "effect": "Nausea after taking",
        "severity": "mild"
      }
    ],
    "adherence_difficulties": [
      {
        "type": "forgetting",
        "description": "Sometimes forgets evening dose on weekends"
      }
    ],
    "adherence_strategies": [
      {
        "type": "alarm",
        "description": "Uses phone alarm for morning medications",
        "effectiveness": "working well"
      }
    ],
    "questions_concerns": [
      {
        "topic": "side effects",
        "question": "Will nausea improve over time?",
        "addressed": false
      }
    ],
    "overall_adherence": {
      "taking_medications": true,
      "taking_as_prescribed": true,
      "taking_correct_medications": true
    },
    "key_concerns": [
      "Mild nausea from Metformin",
      "Weekend adherence inconsistency"
    ],
    "recommendations": [
      "Discuss side effect management strategies",
      "Consider weekend reminder system"
    ]
  }
}
```

### 2. Get Latest Analysis

**GET** `/api/v1/medication-analysis/latest/{research_id}?password=YOUR_ADMIN_PASSWORD`

Retrieves the most recent analysis for a patient.

**Response:** Same format as analyze endpoint

### 3. Get Analysis History

**GET** `/api/v1/medication-analysis/history/{research_id}?password=YOUR_ADMIN_PASSWORD&limit=10`

Retrieves historical analyses for a patient.

**Parameters:**
- `research_id` (required): Patient's research ID
- `limit` (optional): Maximum number of analyses to return (default: 10)

**Response:**
```json
{
  "research_id": "PACO-001",
  "total_count": 5,
  "analyses": [
    {
      "analysis_id": 5,
      "analysis_date": "2025-01-26T14:30:00Z",
      "analyzed_from": "2025-01-20T00:00:00Z",
      "analyzed_to": "2025-01-26T23:59:59Z",
      "conversation_count": 8,
      "confidence_score": 85,
      "summary": "Recent analysis summary...",
      "is_taking_medications": true,
      "taking_as_prescribed": true
    }
  ]
}
```

### 4. Get Conversation Transcript

**GET** `/api/v1/medication-analysis/transcript/{research_id}?password=YOUR_ADMIN_PASSWORD`

Retrieves raw conversation transcript for provider review.

**Response:**
```json
{
  "research_id": "PACO-001",
  "message_count": 42,
  "earliest_message": "2025-01-01T10:00:00",
  "latest_message": "2025-01-26T15:30:00",
  "transcript": "[2025-01-01 10:00:00] USER: Hello...\n\n[2025-01-01 10:00:15] ASSISTANT: Hi! I'm here to..."
}
```

## Setup

### 1. Install Dependencies

The required dependencies should already be in your `requirements.txt`:
- openai
- sqlalchemy
- pydantic
- fastapi

### 2. Run Database Migration

```bash
cd paco-api
alembic upgrade head
```

This creates the `paco_medication_adherence` table.

### 3. Set Admin Password

Ensure your `.env` file has an `ADMIN_PASSWORD` set:

```env
ADMIN_PASSWORD=your_secure_admin_password
```

### 4. Restart API Server

```bash
# Development
uvicorn app.main:app --reload

# Production (Railway)
# Will restart automatically on deploy
```

## Usage Examples

### Using curl

```bash
# Analyze recent conversations
curl -X POST "http://localhost:8000/api/v1/medication-analysis/analyze?password=admin123" \
  -H "Content-Type: application/json" \
  -d '{
    "research_id": "PACO-001",
    "start_date": "2025-01-01T00:00:00",
    "end_date": "2025-01-26T23:59:59"
  }'

# Get latest analysis
curl "http://localhost:8000/api/v1/medication-analysis/latest/PACO-001?password=admin123"

# Get analysis history
curl "http://localhost:8000/api/v1/medication-analysis/history/PACO-001?password=admin123&limit=5"
```

### Using Python

```python
import requests

API_URL = "http://localhost:8000/api/v1/medication-analysis"
ADMIN_PASSWORD = "admin123"

# Analyze conversations
response = requests.post(
    f"{API_URL}/analyze",
    params={"password": ADMIN_PASSWORD},
    json={
        "research_id": "PACO-001",
        "start_date": "2025-01-01T00:00:00",
        "end_date": "2025-01-26T23:59:59",
        "model": "gpt-4o"
    }
)
analysis = response.json()
print(f"Summary: {analysis['summary']}")
print(f"Confidence: {analysis['confidence_score']}%")

# Get medications
for med in analysis['result']['medications']:
    print(f"- {med['name']} {med.get('dosage', '')}")
```

### Using JavaScript/TypeScript

```typescript
const API_URL = 'http://localhost:8000/api/v1/medication-analysis';
const ADMIN_PASSWORD = 'admin123';

async function analyzePatient(researchId: string) {
  const response = await fetch(
    `${API_URL}/analyze?password=${ADMIN_PASSWORD}`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        research_id: researchId,
        model: 'gpt-4o'
      })
    }
  );
  
  const analysis = await response.json();
  return analysis;
}

// Get latest analysis
async function getLatestAnalysis(researchId: string) {
  const response = await fetch(
    `${API_URL}/latest/${researchId}?password=${ADMIN_PASSWORD}`
  );
  return await response.json();
}
```

## Architecture

### Components

1. **medication_analysis_service.py**: Core service handling NLP analysis
   - Retrieves conversation transcripts from database
   - Formats prompts for LLM analysis
   - Parses and structures LLM responses
   - Stores analysis results

2. **medication_analysis.py** (endpoints): REST API endpoints
   - Analyze endpoint: Triggers new analysis
   - Latest endpoint: Retrieves most recent analysis
   - History endpoint: Lists past analyses
   - Transcript endpoint: Returns raw conversations

3. **medication_analysis.py** (schemas): Pydantic models
   - Request/response validation
   - Data structure definitions
   - Type safety

4. **database.py** (models): SQLAlchemy model
   - `MedicationAdherenceAnalysis` table
   - Relationships with ResearchID
   - Indexes for efficient queries

### NLP Analysis Flow

```
1. Provider requests analysis
         ↓
2. Service retrieves conversations from DB
         ↓
3. Formats transcript with timestamps
         ↓
4. Sends to LLM (GPT-4o) with structured prompt
         ↓
5. LLM analyzes and returns JSON
         ↓
6. Service parses and validates response
         ↓
7. Stores results in paco_medication_adherence table
         ↓
8. Returns structured analysis to provider
```

## Database Schema

### paco_medication_adherence Table

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| research_id_fk | INTEGER | Foreign key to paco_research_ids |
| analysis_date | TIMESTAMP | When analysis was performed |
| analyzed_from | TIMESTAMP | Start of analyzed period |
| analyzed_to | TIMESTAMP | End of analyzed period |
| conversation_count | INTEGER | Number of messages analyzed |
| is_taking_medications | BOOLEAN | Patient taking meds (true/false/null) |
| taking_as_prescribed | BOOLEAN | Taking as prescribed |
| taking_correct_medications | BOOLEAN | Taking correct medications |
| adherence_barriers | TEXT | JSON array of difficulties |
| adherence_strategies | TEXT | JSON array of strategies |
| side_effects | TEXT | JSON array of side effects |
| medication_list | TEXT | JSON array of medications |
| confidence_score | INTEGER | Analysis confidence (0-100) |
| summary | TEXT | Provider summary |
| detailed_analysis | TEXT | Full JSON analysis |
| model_used | VARCHAR(100) | LLM model used |

### Indexes

- `ix_adherence_research_date`: (research_id_fk, analysis_date)
- `ix_adherence_analysis_date`: (analysis_date)

## Security

- **Authentication**: All endpoints require admin password
- **Authorization**: Admin-only access ensures patient privacy
- **Data Storage**: Analysis results stored securely in database
- **HIPAA Considerations**: 
  - No PHI in logs
  - Secure database connections
  - Admin password should be strong and rotated regularly

## LLM Models Supported

The system supports multiple LLM models through the `llm_service`:

- **gpt-4o** (recommended): Best accuracy for medical text analysis
- **gpt-4o-mini**: Faster, lower cost, slightly less accurate
- **llama-3.3-70b-versatile**: Groq-hosted, fast inference
- **o3-mini**: OpenAI's reasoning model

## Cost Considerations

- **GPT-4o**: ~$0.005-0.015 per analysis (depending on conversation length)
- **GPT-4o-mini**: ~$0.001-0.003 per analysis
- **Groq models**: Free tier available, very fast

Typical conversation (20-30 messages) costs $0.01-0.02 with GPT-4o.

## Limitations

1. **Accuracy**: NLP analysis depends on conversation quality and LLM performance
2. **Confidence**: Low confidence scores may require human review
3. **Context**: Analysis limited to available conversation data
4. **Language**: Best results with clear, structured conversations
5. **Medical Advice**: This is an analysis tool, not a replacement for clinical judgment

## Future Enhancements

Potential improvements:
- [ ] Multi-language support
- [ ] Trend analysis across multiple analyses
- [ ] Automated alerts for concerning patterns
- [ ] Integration with EHR systems
- [ ] Patient-facing summaries
- [ ] Medication interaction checking
- [ ] Visual dashboards for providers

## Troubleshooting

### "No conversations found"
- Check that the research_id exists
- Verify date range includes conversations
- Check database connectivity

### "Invalid admin password"
- Verify ADMIN_PASSWORD in environment
- Check password parameter in request
- Ensure no extra whitespace in password

### Low confidence scores
- Conversations may be too brief
- Patient may not have discussed medications
- Try analyzing longer time period

### JSON parsing errors
- LLM may have returned invalid JSON
- Check `detailed_analysis` field for raw response
- Try different model (e.g., gpt-4o vs gpt-4o-mini)

## Support

For issues or questions:
1. Check API logs: `railway logs` or local console
2. Review database: Check paco_medication_adherence table
3. Test with transcript endpoint first
4. Verify OpenAI API key is valid

## License

Part of the PaCo (Patient Communication) system.
