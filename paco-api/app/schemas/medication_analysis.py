"""
Pydantic schemas for medication adherence analysis
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class MedicationInfo(BaseModel):
    """Information about a specific medication"""
    name: str
    dosage: Optional[str] = None
    mentioned_by_patient: bool = True


class TimingSchedule(BaseModel):
    """When medications are taken"""
    morning: List[str] = Field(default_factory=list)
    afternoon: List[str] = Field(default_factory=list)
    evening: List[str] = Field(default_factory=list)
    as_needed: List[str] = Field(default_factory=list)
    unclear: List[str] = Field(default_factory=list)


class SideEffect(BaseModel):
    """Side effect information"""
    medication: str
    effect: str
    severity: str = Field(..., pattern="^(mild|moderate|severe)$")


class AdherenceDifficulty(BaseModel):
    """Difficulties with medication adherence"""
    type: str
    description: str


class AdherenceStrategy(BaseModel):
    """Strategies used to improve adherence"""
    type: str
    description: str
    effectiveness: str = Field(..., pattern="^(working well|somewhat helpful|not working)$")


class QuestionConcern(BaseModel):
    """Patient questions or concerns"""
    topic: str
    question: str
    addressed: bool = False


class OverallAdherence(BaseModel):
    """Overall adherence status"""
    taking_medications: Optional[bool] = None
    taking_as_prescribed: Optional[bool] = None
    taking_correct_medications: Optional[bool] = None


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


class AnalysisResult(BaseModel):
    """Complete analysis result"""
    medications: List[MedicationInfo]
    timing_schedule: TimingSchedule
    side_effects: List[SideEffect]
    adherence_difficulties: List[AdherenceDifficulty]
    adherence_strategies: List[AdherenceStrategy]
    questions_concerns: List[QuestionConcern]
    overall_adherence: OverallAdherence
    confidence_score: int = Field(..., ge=0, le=100)
    summary: str
    key_concerns: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)


class AnalysisResponse(BaseModel):
    """Response containing analysis results and metadata"""
    analysis_id: int
    research_id: str
    analysis_date: datetime
    analyzed_from: datetime
    analyzed_to: datetime
    conversation_count: int
    confidence_score: int
    summary: str
    model_used: str
    result: AnalysisResult

    class Config:
        from_attributes = True


class AnalysisHistoryItem(BaseModel):
    """Summary of a past analysis"""
    analysis_id: int
    analysis_date: datetime
    analyzed_from: datetime
    analyzed_to: datetime
    conversation_count: int
    confidence_score: int
    summary: str
    is_taking_medications: Optional[bool]
    taking_as_prescribed: Optional[bool]

    class Config:
        from_attributes = True


class AnalysisHistoryResponse(BaseModel):
    """List of past analyses"""
    research_id: str
    analyses: List[AnalysisHistoryItem]
    total_count: int
