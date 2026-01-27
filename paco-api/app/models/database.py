"""
SQLAlchemy models for database tables
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class ResearchID(Base):
    """Authorized research IDs for user access"""
    __tablename__ = "paco_research_ids"

    id = Column(Integer, primary_key=True, index=True)
    research_id = Column(String(50), unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True, nullable=False)
    notes = Column(Text, nullable=True)

    # Relationships
    sessions = relationship("UserSession", back_populates="research_user")
    disclaimers = relationship("DisclaimerAcknowledgment", back_populates="research_user")
    conversations = relationship("Conversation", back_populates="research_user")


class UserSession(Base):
    """Active user sessions with JWT tokens"""
    __tablename__ = "paco_user_sessions"

    id = Column(Integer, primary_key=True, index=True)
    research_id_fk = Column(Integer, ForeignKey("paco_research_ids.id"), nullable=False)
    session_token = Column(String(500), unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_active = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(Text, nullable=True)

    # Relationships
    research_user = relationship("ResearchID", back_populates="sessions")


class DisclaimerAcknowledgment(Base):
    """Track when users acknowledge the research disclaimer"""
    __tablename__ = "paco_disclaimer_acknowledgments"

    id = Column(Integer, primary_key=True, index=True)
    research_id_fk = Column(Integer, ForeignKey("paco_research_ids.id"), nullable=False)
    acknowledged_at = Column(DateTime(timezone=True), server_default=func.now())
    ip_address = Column(String(50), nullable=True)
    disclaimer_version = Column(String(10), default="1.0")

    # Relationships
    research_user = relationship("ResearchID", back_populates="disclaimers")


class Conversation(Base):
    """Chat messages for all users"""
    __tablename__ = "paco_conversations"

    id = Column(Integer, primary_key=True, index=True)
    research_id_fk = Column(Integer, ForeignKey("paco_research_ids.id"), nullable=False)
    conversation_id = Column(String(255), nullable=False, index=True)  # Format: conv_YYYYMMDDHHMMSS_RESEARCHID
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    role = Column(String(20), nullable=False)  # 'user', 'assistant', 'system'
    content = Column(Text, nullable=False)
    model_used = Column(String(100), nullable=True)  # Track which LLM was used
    audio_url = Column(String(500), nullable=True)  # Path to TTS audio file if generated

    # Provider tracking
    provider = Column(String(20), default="openai", nullable=True)  # 'elevenlabs' or 'openai'

    # ElevenLabs-specific fields
    elevenlabs_conversation_id = Column(String(255), nullable=True)
    elevenlabs_message_id = Column(String(255), nullable=True)

    # Relationships
    research_user = relationship("ResearchID", back_populates="conversations")

    # Indexes for efficient queries
    __table_args__ = (
        Index('ix_conversation_research_timestamp', 'conversation_id', 'timestamp'),
        Index('ix_research_timestamp', 'research_id_fk', 'timestamp'),
    )


class MedicationAdherenceAnalysis(Base):
    """NLP analysis results for medication adherence from conversations"""
    __tablename__ = "paco_medication_adherence"

    id = Column(Integer, primary_key=True, index=True)
    research_id_fk = Column(Integer, ForeignKey("paco_research_ids.id"), nullable=False)
    
    # Analysis metadata
    analysis_date = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    analyzed_from = Column(DateTime(timezone=True), nullable=False)  # Start of conversation period
    analyzed_to = Column(DateTime(timezone=True), nullable=False)  # End of conversation period
    conversation_count = Column(Integer, default=0)  # Number of conversations analyzed
    
    # Medication adherence findings
    is_taking_medications = Column(Boolean, nullable=True)  # Null = unclear/not discussed
    taking_as_prescribed = Column(Boolean, nullable=True)
    taking_correct_medications = Column(Boolean, nullable=True)
    
    # Detailed insights (stored as text for provider review)
    adherence_barriers = Column(Text, nullable=True)  # Issues preventing adherence
    adherence_strategies = Column(Text, nullable=True)  # What patient does to remember/take meds
    side_effects = Column(Text, nullable=True)  # Reported side effects
    medication_list = Column(Text, nullable=True)  # Medications mentioned by patient
    
    # Confidence and summary
    confidence_score = Column(Integer, default=0)  # 0-100 confidence in analysis
    summary = Column(Text, nullable=False)  # Executive summary for provider
    detailed_analysis = Column(Text, nullable=True)  # Full NLP analysis output
    
    # Model tracking
    model_used = Column(String(100), nullable=True)  # Which LLM performed the analysis
    
    # Relationships
    research_user = relationship("ResearchID", backref="adherence_analyses")
    
    # Indexes
    __table_args__ = (
        Index('ix_adherence_research_date', 'research_id_fk', 'analysis_date'),
    )
