"""
Pydantic schemas for medication adherence analysis
"""
from pydantic import BaseModel, Field
from typing import Dict, List, Literal, Optional
from datetime import datetime


class QuilamDomain(BaseModel):
    """Finding and flag for a single QUILAM domain"""
    finding: str
    flag: Literal["surfaced", "not surfaced", "concern flagged"]
    details: List[str] = Field(default_factory=list)


class QuilamDomains(BaseModel):
    """All four QUILAM domains"""
    general_beliefs: QuilamDomain
    self_management: QuilamDomain
    specific_beliefs: QuilamDomain
    provider_relationship: QuilamDomain


class QuilamAnalysisResult(BaseModel):
    """Complete QUILAM framework analysis result"""
    domains: QuilamDomains
    overall_summary: str
    key_concerns: List[str] = Field(default_factory=list)
    confidence_score: int = Field(..., ge=0, le=100)


class AnalysisRequest(BaseModel):
    """Request to analyze medication adherence"""
    research_id: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    model: str = "llama-3.3-70b-versatile"

    class Config:
        json_schema_extra = {
            "example": {
                "research_id": "PACO-001",
                "start_date": "2025-01-01T00:00:00",
                "end_date": "2025-01-26T23:59:59",
                "model": "llama-3.3-70b-versatile"
            }
        }


class AnalysisResponse(BaseModel):
    """Response containing QUILAM analysis results and metadata"""
    analysis_id: int
    research_id: str
    analysis_date: datetime
    analyzed_from: datetime
    analyzed_to: datetime
    conversation_count: int
    confidence_score: int
    summary: str
    model_used: str
    result: QuilamAnalysisResult

    class Config:
        from_attributes = True


class AnalysisHistoryItem(BaseModel):
    """Summary of a past analysis, with each QUILAM domain's flag for at-a-glance review"""
    analysis_id: int
    analysis_date: datetime
    analyzed_from: datetime
    analyzed_to: datetime
    conversation_count: int
    confidence_score: int
    summary: str
    # Maps each QUILAM domain key -> its flag (surfaced / not surfaced / concern flagged)
    domain_flags: Dict[str, str] = Field(default_factory=dict)

    class Config:
        from_attributes = True


class AnalysisHistoryResponse(BaseModel):
    """List of past analyses"""
    research_id: str
    analyses: List[AnalysisHistoryItem]
    total_count: int
