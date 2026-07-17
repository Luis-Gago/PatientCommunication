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

    ANALYSIS_PROMPT = """You are a clinical research analyst reviewing a patient conversation transcript to assess medication adherence using the QUILAM framework.

Analyze the conversation and fill out the four QUILAM domains below. For each domain, write a brief finding summarizing what the patient shared, and assign a flag.

Flag definitions:
- "surfaced": The topic came up and no significant concern was identified.
- "not surfaced": The topic did not come up in this conversation.
- "concern flagged": A concern in this domain was identified that warrants provider attention.

---

Domain 1 - General Beliefs About Treatment
Items to assess:
- Does the patient feel doctors overprescribe medication?
- Does the patient worry about long-term side effects of their medication?
- Does the patient trust medical treatments more or less than natural remedies?

Domain 2 - Self-Management of Treatment (Unintentional Nonadherence)
Items to assess:
- Does the patient forget to refill prescriptions?
- Does the patient sometimes not have their medication available when they need it?
- Does the patient have difficulty managing multiple medications?

Domain 3 - Specific Beliefs About Treatment (Intentional Nonadherence)
Items to assess:
- Does the patient feel socially uncomfortable taking medication in front of others?
- Is the patient sometimes negligent about taking their medication?
- Has the patient reduced or stopped their medication without telling their doctor because they felt worse?

Domain 4 - Patient/Healthcare System Relationship
Items to assess:
- Does the patient feel they make decisions together with their doctor?
- Does the patient understand their healthcare provider's instructions?
- Did the patient's doctor explain how to properly treat their illness?
- Is the patient satisfied with their treatment overall?

---

Conversation Transcript:
{conversation_transcript}

---

Output Format (JSON only, no additional text):
{{
  "domains": {{
    "general_beliefs": {{
      "finding": "What the patient shared about their general beliefs, or 'Not discussed' if this did not come up.",
      "flag": "surfaced or not surfaced or concern flagged",
      "details": ["Specific items or direct quotes from the conversation that support the finding"]
    }},
    "self_management": {{
      "finding": "What the patient shared about day-to-day self-management challenges, or 'Not discussed'.",
      "flag": "surfaced or not surfaced or concern flagged",
      "details": ["Specific items or direct quotes"]
    }},
    "specific_beliefs": {{
      "finding": "What the patient shared about intentional decisions to skip, reduce, or stop medication, or 'Not discussed'.",
      "flag": "surfaced or not surfaced or concern flagged",
      "details": ["Specific items or direct quotes"]
    }},
    "provider_relationship": {{
      "finding": "What the patient shared about their relationship with their healthcare team, or 'Not discussed'.",
      "flag": "surfaced or not surfaced or concern flagged",
      "details": ["Specific items or direct quotes"]
    }}
  }},
  "overall_summary": "2-3 sentence summary of the patient's medication adherence situation for the provider.",
  "key_concerns": ["Most important concerns for the provider to follow up on"],
  "confidence_score": 0-100
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
            confidence_score=analysis_data.get("confidence_score", 0),
            summary=analysis_data.get("overall_summary", "Analysis completed."),
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
