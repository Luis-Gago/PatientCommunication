"""
Medication adherence analysis endpoints for medical providers
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import json

from app.db.base import get_db
from app.models.database import ResearchID
from app.schemas.medication_analysis import (
    AnalysisRequest,
    AnalysisResponse,
    AnalysisResult,
    AnalysisHistoryResponse,
    AnalysisHistoryItem,
    MedicationInfo,
    TimingSchedule,
    SideEffect,
    AdherenceDifficulty,
    AdherenceStrategy,
    QuestionConcern,
    OverallAdherence
)
from app.services.medication_analysis_service import medication_analysis_service
from app.core.security import verify_admin_password

router = APIRouter()


def parse_analysis_result(detailed_analysis: str) -> AnalysisResult:
    """Parse the detailed analysis JSON into structured format"""
    try:
        data = json.loads(detailed_analysis)
        
        return AnalysisResult(
            medications=[MedicationInfo(**med) for med in data.get("medications", [])],
            timing_schedule=TimingSchedule(**data.get("timing_schedule", {})),
            side_effects=[SideEffect(**se) for se in data.get("side_effects", [])],
            adherence_difficulties=[
                AdherenceDifficulty(**diff) for diff in data.get("adherence_difficulties", [])
            ],
            adherence_strategies=[
                AdherenceStrategy(**strat) for strat in data.get("adherence_strategies", [])
            ],
            questions_concerns=[
                QuestionConcern(**qc) for qc in data.get("questions_concerns", [])
            ],
            overall_adherence=OverallAdherence(**data.get("overall_adherence", {})),
            confidence_score=data.get("confidence_score", 0),
            summary=data.get("summary", ""),
            key_concerns=data.get("key_concerns", []),
            recommendations=data.get("recommendations", [])
        )
    except (json.JSONDecodeError, ValueError) as e:
        # Return a minimal result if parsing fails
        return AnalysisResult(
            medications=[],
            timing_schedule=TimingSchedule(),
            side_effects=[],
            adherence_difficulties=[],
            adherence_strategies=[],
            questions_concerns=[],
            overall_adherence=OverallAdherence(),
            confidence_score=0,
            summary="Error parsing analysis results. Check detailed_analysis field.",
            key_concerns=["Analysis parsing error"],
            recommendations=["Re-run analysis"]
        )


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_medication_adherence(
    request: AnalysisRequest,
    admin_password: str = Depends(verify_admin_password),
    db: Session = Depends(get_db)
):
    """
    Analyze medication adherence from patient conversations.
    
    This endpoint uses NLP to extract:
    - Medications being taken
    - Timing/schedule
    - Side effects
    - Adherence difficulties
    - Adherence strategies
    - Questions and concerns
    
    Requires admin authentication.
    """
    try:
        # Perform analysis
        analysis = await medication_analysis_service.analyze_medication_adherence(
            db=db,
            research_id=request.research_id,
            start_date=request.start_date,
            end_date=request.end_date,
            model=request.model
        )

        # Parse detailed analysis
        result = parse_analysis_result(analysis.detailed_analysis)

        return AnalysisResponse(
            analysis_id=analysis.id,
            research_id=request.research_id,
            analysis_date=analysis.analysis_date,
            analyzed_from=analysis.analyzed_from,
            analyzed_to=analysis.analyzed_to,
            conversation_count=analysis.conversation_count,
            confidence_score=analysis.confidence_score,
            summary=analysis.summary,
            model_used=analysis.model_used,
            result=result
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


@router.get("/history/{research_id}", response_model=AnalysisHistoryResponse)
async def get_analysis_history(
    research_id: str,
    limit: int = 10,
    admin_password: str = Depends(verify_admin_password),
    db: Session = Depends(get_db)
):
    """
    Get historical medication adherence analyses for a patient.
    
    Returns up to `limit` most recent analyses.
    Requires admin authentication.
    """
    # Verify research ID exists
    research_user = db.query(ResearchID).filter(
        ResearchID.research_id == research_id
    ).first()

    if not research_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Research ID {research_id} not found"
        )

    # Get analysis history
    analyses = medication_analysis_service.get_analysis_history(
        db=db,
        research_id=research_id,
        limit=limit
    )

    # Format response
    history_items = [
        AnalysisHistoryItem(
            analysis_id=analysis.id,
            analysis_date=analysis.analysis_date,
            analyzed_from=analysis.analyzed_from,
            analyzed_to=analysis.analyzed_to,
            conversation_count=analysis.conversation_count,
            confidence_score=analysis.confidence_score,
            summary=analysis.summary,
            is_taking_medications=analysis.is_taking_medications,
            taking_as_prescribed=analysis.taking_as_prescribed
        )
        for analysis in analyses
    ]

    return AnalysisHistoryResponse(
        research_id=research_id,
        analyses=history_items,
        total_count=len(history_items)
    )


@router.get("/latest/{research_id}", response_model=AnalysisResponse)
async def get_latest_analysis(
    research_id: str,
    admin_password: str = Depends(verify_admin_password),
    db: Session = Depends(get_db)
):
    """
    Get the most recent medication adherence analysis for a patient.
    
    Requires admin authentication.
    """
    # Get latest analysis
    analysis = medication_analysis_service.get_latest_analysis(
        db=db,
        research_id=research_id
    )

    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No analyses found for research ID {research_id}"
        )

    # Parse detailed analysis
    result = parse_analysis_result(analysis.detailed_analysis)

    return AnalysisResponse(
        analysis_id=analysis.id,
        research_id=research_id,
        analysis_date=analysis.analysis_date,
        analyzed_from=analysis.analyzed_from,
        analyzed_to=analysis.analyzed_to,
        conversation_count=analysis.conversation_count,
        confidence_score=analysis.confidence_score,
        summary=analysis.summary,
        model_used=analysis.model_used,
        result=result
    )


@router.get("/transcript/{research_id}")
async def get_conversation_transcript(
    research_id: str,
    admin_password: str = Depends(verify_admin_password),
    db: Session = Depends(get_db)
):
    """
    Get the raw conversation transcript for a patient.
    
    Useful for providers who want to review the original conversations.
    Requires admin authentication.
    """
    try:
        transcript, count, earliest, latest = (
            medication_analysis_service.get_conversation_transcript(
                db=db,
                research_id=research_id
            )
        )

        return {
            "research_id": research_id,
            "message_count": count,
            "earliest_message": earliest.isoformat(),
            "latest_message": latest.isoformat(),
            "transcript": transcript
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
