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
    QuilamAnalysisResult,
    QuilamDomain,
    QuilamDomains,
    AnalysisHistoryResponse,
    AnalysisHistoryItem
)
from app.services.medication_analysis_service import medication_analysis_service
from app.core.security import verify_admin_password

router = APIRouter()


VALID_FLAGS = {"surfaced", "not surfaced", "concern flagged"}


def parse_domain(domains_data: dict, key: str) -> QuilamDomain:
    """Parse a single QUILAM domain, tolerant of LLM output variance.

    Handles missing keys, explicit nulls, wrong-typed values, and flag
    casing/whitespace. A malformed individual domain degrades to a single
    error domain rather than discarding the whole analysis.
    """
    try:
        d = domains_data.get(key)
        if not isinstance(d, dict):
            d = {}

        raw_flag = d.get("flag") or "not surfaced"
        flag = raw_flag.lower().strip() if isinstance(raw_flag, str) else "not surfaced"
        if flag not in VALID_FLAGS:
            flag = "not surfaced"

        finding = d.get("finding") or "Not discussed"
        if not isinstance(finding, str):
            finding = str(finding)

        details = d.get("details") or []
        if not isinstance(details, list):
            details = [str(details)]
        else:
            details = [str(item) for item in details]

        return QuilamDomain(finding=finding, flag=flag, details=details)
    except (ValueError, TypeError, AttributeError):
        return QuilamDomain(finding="Could not parse this domain.", flag="not surfaced", details=[])


def parse_analysis_result(detailed_analysis: str) -> QuilamAnalysisResult:
    """Parse the QUILAM analysis JSON into structured format"""
    try:
        data = json.loads(detailed_analysis)
        if not isinstance(data, dict):
            raise ValueError("Top-level analysis JSON is not an object")

        domains_data = data.get("domains")
        if not isinstance(domains_data, dict):
            domains_data = {}

        try:
            confidence_score = int(data.get("confidence_score", 0))
        except (ValueError, TypeError):
            confidence_score = 0
        confidence_score = max(0, min(100, confidence_score))

        key_concerns = data.get("key_concerns") or []
        if not isinstance(key_concerns, list):
            key_concerns = [str(key_concerns)]
        else:
            key_concerns = [str(item) for item in key_concerns]

        overall_summary = data.get("overall_summary") or ""
        if not isinstance(overall_summary, str):
            overall_summary = str(overall_summary)

        return QuilamAnalysisResult(
            domains=QuilamDomains(
                general_beliefs=parse_domain(domains_data, "general_beliefs"),
                self_management=parse_domain(domains_data, "self_management"),
                specific_beliefs=parse_domain(domains_data, "specific_beliefs"),
                provider_relationship=parse_domain(domains_data, "provider_relationship")
            ),
            overall_summary=overall_summary,
            key_concerns=key_concerns,
            confidence_score=confidence_score
        )
    except (json.JSONDecodeError, ValueError, TypeError):
        return QuilamAnalysisResult(
            domains=QuilamDomains(
                general_beliefs=QuilamDomain(finding="Error parsing analysis results.", flag="not surfaced"),
                self_management=QuilamDomain(finding="Error parsing analysis results.", flag="not surfaced"),
                specific_beliefs=QuilamDomain(finding="Error parsing analysis results.", flag="not surfaced"),
                provider_relationship=QuilamDomain(finding="Error parsing analysis results.", flag="not surfaced")
            ),
            overall_summary="Error parsing analysis results. Check detailed_analysis field.",
            key_concerns=["Analysis parsing error"],
            confidence_score=0
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

    # Format response — surface each QUILAM domain's flag per analysis
    history_items = []
    for analysis in analyses:
        result = parse_analysis_result(analysis.detailed_analysis)
        history_items.append(
            AnalysisHistoryItem(
                analysis_id=analysis.id,
                analysis_date=analysis.analysis_date,
                analyzed_from=analysis.analyzed_from,
                analyzed_to=analysis.analyzed_to,
                conversation_count=analysis.conversation_count,
                confidence_score=analysis.confidence_score,
                summary=analysis.summary,
                domain_flags={
                    "general_beliefs": result.domains.general_beliefs.flag,
                    "self_management": result.domains.self_management.flag,
                    "specific_beliefs": result.domains.specific_beliefs.flag,
                    "provider_relationship": result.domains.provider_relationship.flag,
                },
            )
        )

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
