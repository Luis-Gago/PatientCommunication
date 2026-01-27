"""
Medication adherence analysis service using NLP
"""
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
import json

from app.models.database import (
    Conversation, 
    ResearchID, 
    MedicationAdherenceAnalysis
)
from app.services.llm_service import llm_service


class MedicationAnalysisService:
    """Service for analyzing medication adherence from conversations"""

    ANALYSIS_PROMPT = """You are a medical data analyst tasked with extracting medication adherence information from patient conversations.

Analyze the following conversation transcript and extract structured information about:

1. **Medications**: List all medications mentioned (name, dosage if mentioned)
2. **Timing**: When the patient takes their medications (morning, evening, with meals, etc.)
3. **Side Effects**: Any adverse effects or symptoms the patient reports
4. **Adherence Difficulties**: Problems the patient has taking medications as prescribed (forgetting, cost, access, confusion, etc.)
5. **Adherence Strategies**: Methods the patient uses to remember/take medications (alarms, pill boxes, routines, etc.)
6. **Questions/Concerns**: Any questions or concerns the patient has expressed about their medications

**Conversation Transcript:**
{conversation_transcript}

**Instructions:**
- Be specific and quote relevant parts of the conversation
- If information is not mentioned, state "Not discussed" for that category
- Use a confidence score (0-100) to indicate how certain you are about the information
- Provide a brief summary suitable for a medical provider to quickly understand the patient's adherence status

**Output Format (JSON):**
{{
  "medications": [
    {{"name": "medication name", "dosage": "dosage if mentioned", "mentioned_by_patient": true/false}}
  ],
  "timing_schedule": {{
    "morning": ["list of medications"],
    "afternoon": ["list of medications"],
    "evening": ["list of medications"],
    "as_needed": ["list of medications"],
    "unclear": ["list of medications"]
  }},
  "side_effects": [
    {{"medication": "medication name or 'unclear'", "effect": "description", "severity": "mild/moderate/severe"}}
  ],
  "adherence_difficulties": [
    {{"type": "forgetting/cost/access/side_effects/complexity/other", "description": "detailed description"}}
  ],
  "adherence_strategies": [
    {{"type": "alarm/pill_box/routine/caregiver_help/other", "description": "detailed description", "effectiveness": "working well/somewhat helpful/not working"}}
  ],
  "questions_concerns": [
    {{"topic": "topic area", "question": "patient's question or concern", "addressed": true/false}}
  ],
  "overall_adherence": {{
    "taking_medications": true/false/unclear,
    "taking_as_prescribed": true/false/unclear,
    "taking_correct_medications": true/false/unclear
  }},
  "confidence_score": 0-100,
  "summary": "Brief 2-3 sentence summary for medical provider",
  "key_concerns": ["List of 3-5 most important concerns for provider to know"],
  "recommendations": ["Suggested follow-up actions based on the conversation"]
}}

Respond ONLY with valid JSON, no additional text."""

    @staticmethod
    def get_conversation_transcript(
        db: Session,
        research_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> tuple[str, int, datetime, datetime]:
        """
        Retrieve conversation transcript for a research ID
        Returns: (transcript, message_count, earliest_date, latest_date)
        """
        research_user = db.query(ResearchID).filter(
            ResearchID.research_id == research_id
        ).first()

        if not research_user:
            raise ValueError(f"Research ID {research_id} not found")

        # Build query
        query = db.query(Conversation).filter(
            Conversation.research_id_fk == research_user.id
        )

        # Apply date filters
        if start_date:
            query = query.filter(Conversation.timestamp >= start_date)
        if end_date:
            query = query.filter(Conversation.timestamp <= end_date)

        # Get messages ordered by timestamp
        messages = query.order_by(Conversation.timestamp).all()

        if not messages:
            raise ValueError(f"No conversations found for research ID {research_id}")

        # Build transcript
        transcript_parts = []
        for msg in messages:
            role_label = msg.role.upper()
            timestamp_str = msg.timestamp.strftime("%Y-%m-%d %H:%M:%S")
            transcript_parts.append(
                f"[{timestamp_str}] {role_label}: {msg.content}"
            )

        transcript = "\n\n".join(transcript_parts)
        earliest = min(msg.timestamp for msg in messages)
        latest = max(msg.timestamp for msg in messages)

        return transcript, len(messages), earliest, latest

    @staticmethod
    async def analyze_medication_adherence(
        db: Session,
        research_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        model: str = "llama-3.3-70b-versatile"
    ) -> MedicationAdherenceAnalysis:
        """
        Analyze medication adherence from conversations using NLP (Groq AI)
        
        Args:
            db: Database session
            research_id: Patient's research ID
            start_date: Optional start date for analysis
            end_date: Optional end date for analysis
            model: Groq model to use for analysis (default: llama-3.3-70b-versatile)
            
        Returns:
            MedicationAdherenceAnalysis object with results
        """
        # Get research user
        research_user = db.query(ResearchID).filter(
            ResearchID.research_id == research_id
        ).first()

        if not research_user:
            raise ValueError(f"Research ID {research_id} not found")

        # Get conversation transcript
        transcript, message_count, earliest, latest = (
            MedicationAnalysisService.get_conversation_transcript(
                db, research_id, start_date, end_date
            )
        )

        # Prepare prompt
        prompt = MedicationAnalysisService.ANALYSIS_PROMPT.format(
            conversation_transcript=transcript
        )

        # Call LLM for analysis
        messages = [
            {"role": "system", "content": "You are a medical data analyst specializing in medication adherence analysis."},
            {"role": "user", "content": prompt}
        ]

        response = await llm_service.get_chat_completion(
            model=model,
            messages=messages,
            max_tokens=4000
        )

        # Parse JSON response
        try:
            # Try to extract JSON if LLM added extra text
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                response = response[json_start:json_end]
            
            analysis_data = json.loads(response)
        except json.JSONDecodeError as e:
            # If JSON parsing fails, create a basic structure
            analysis_data = {
                "summary": "Error parsing LLM response. Raw response stored in detailed_analysis.",
                "confidence_score": 0,
                "overall_adherence": {
                    "taking_medications": None,
                    "taking_as_prescribed": None,
                    "taking_correct_medications": None
                }
            }

        # Create analysis record
        analysis = MedicationAdherenceAnalysis(
            research_id_fk=research_user.id,
            analyzed_from=earliest,
            analyzed_to=latest,
            conversation_count=message_count,
            is_taking_medications=analysis_data.get("overall_adherence", {}).get("taking_medications"),
            taking_as_prescribed=analysis_data.get("overall_adherence", {}).get("taking_as_prescribed"),
            taking_correct_medications=analysis_data.get("overall_adherence", {}).get("taking_correct_medications"),
            adherence_barriers=json.dumps(analysis_data.get("adherence_difficulties", [])),
            adherence_strategies=json.dumps(analysis_data.get("adherence_strategies", [])),
            side_effects=json.dumps(analysis_data.get("side_effects", [])),
            medication_list=json.dumps(analysis_data.get("medications", [])),
            confidence_score=analysis_data.get("confidence_score", 0),
            summary=analysis_data.get("summary", "Analysis completed."),
            detailed_analysis=response,
            model_used=model
        )

        db.add(analysis)
        db.commit()
        db.refresh(analysis)

        return analysis

    @staticmethod
    def get_latest_analysis(
        db: Session,
        research_id: str
    ) -> Optional[MedicationAdherenceAnalysis]:
        """Get the most recent analysis for a research ID"""
        research_user = db.query(ResearchID).filter(
            ResearchID.research_id == research_id
        ).first()

        if not research_user:
            return None

        return db.query(MedicationAdherenceAnalysis).filter(
            MedicationAdherenceAnalysis.research_id_fk == research_user.id
        ).order_by(desc(MedicationAdherenceAnalysis.analysis_date)).first()

    @staticmethod
    def get_analysis_history(
        db: Session,
        research_id: str,
        limit: int = 10
    ) -> List[MedicationAdherenceAnalysis]:
        """Get analysis history for a research ID"""
        research_user = db.query(ResearchID).filter(
            ResearchID.research_id == research_id
        ).first()

        if not research_user:
            return []

        return db.query(MedicationAdherenceAnalysis).filter(
            MedicationAdherenceAnalysis.research_id_fk == research_user.id
        ).order_by(desc(MedicationAdherenceAnalysis.analysis_date)).limit(limit).all()


# Singleton instance
medication_analysis_service = MedicationAnalysisService()
