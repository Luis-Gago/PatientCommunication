"""
Chat and conversation endpoints - ElevenLabs focused
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import httpx
from datetime import datetime

from app.db.base import get_db
from app.models.database import ResearchID, Conversation
from app.schemas.conversation import (
    ConversationHistoryRequest,
    ConversationHistoryResponse,
    MessageResponse,
    MessageSaveRequest,
    MessageSaveResponse,
    ElevenLabsConversationSyncRequest,
    ElevenLabsConversationSyncResponse
)
from app.core.security import get_current_user
from app.services.conversation_service import conversation_service
from app.core.config import get_settings

router = APIRouter()


@router.post("/save-message", response_model=MessageSaveResponse)
async def save_message_from_frontend(
    data: MessageSaveRequest,
    current_user: ResearchID = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Save a single message from the frontend (ElevenLabs).

    This endpoint is used by the frontend to sync messages to the database
    for research data collection.
    """
    # Verify user matches research_id in request
    if current_user.research_id != data.research_id:
        raise HTTPException(status_code=403, detail="Research ID mismatch")

    # Parse timestamp from ISO format
    try:
        timestamp = datetime.fromisoformat(data.timestamp.replace('Z', '+00:00'))
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid timestamp format")

    # Generate conversation_id if using ElevenLabs
    conversation_id = data.elevenlabs_conversation_id or f"conv_{datetime.now().strftime('%Y%m%d%H%M%S')}_{data.research_id}"

    # Get the research_id_fk
    research_user = db.query(ResearchID).filter(ResearchID.research_id == data.research_id).first()
    if not research_user:
        raise HTTPException(status_code=404, detail="Research ID not found")

    # Check for duplicate message (for ElevenLabs messages)
    if data.elevenlabs_message_id and data.elevenlabs_conversation_id:
        existing = db.query(Conversation).filter(
            Conversation.elevenlabs_message_id == data.elevenlabs_message_id,
            Conversation.elevenlabs_conversation_id == data.elevenlabs_conversation_id
        ).first()

        if existing:
            # Message already exists, return success without creating duplicate
            return MessageSaveResponse(
                success=True,
                message_id=existing.id,
                timestamp=existing.timestamp
            )

    # Create conversation record
    message = Conversation(
        research_id_fk=research_user.id,
        conversation_id=conversation_id,
        role=data.role,
        content=data.content,
        timestamp=timestamp,
        provider=data.provider,
        elevenlabs_conversation_id=data.elevenlabs_conversation_id,
        elevenlabs_message_id=data.elevenlabs_message_id
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return MessageSaveResponse(
        success=True,
        message_id=message.id,
        timestamp=message.timestamp
    )


@router.post("/history", response_model=ConversationHistoryResponse)
async def get_conversation_history(
    data: ConversationHistoryRequest,
    current_user: ResearchID = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get conversation history for a research ID"""
    # Verify user matches research_id in request
    if current_user.research_id != data.research_id:
        raise HTTPException(status_code=403, detail="Research ID mismatch")

    messages, total = conversation_service.get_conversation_history(
        db=db,
        research_id=data.research_id,
        conversation_id=data.conversation_id,
        limit=data.limit,
        offset=data.offset
    )

    message_responses = [
        MessageResponse(
            id=msg.id,
            conversation_id=msg.conversation_id,
            role=msg.role,
            content=msg.content,
            timestamp=msg.timestamp,
            model_used=msg.model_used,
            audio_url=msg.audio_url
        )
        for msg in messages
    ]

    return ConversationHistoryResponse(
        messages=message_responses,
        total=total,
        research_id=data.research_id
    )


@router.get("/conversations")
async def get_recent_conversations(
    current_user: ResearchID = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 10
):
    """Get list of recent conversation IDs for current user"""
    conversations = conversation_service.get_recent_conversations(
        db=db,
        research_id=current_user.research_id,
        limit=limit
    )

    return {
        "research_id": current_user.research_id,
        "conversations": conversations
    }


@router.get("/conversations/elevenlabs")
async def get_elevenlabs_conversations(
    current_user: ResearchID = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get list of existing ElevenLabs conversation IDs for current user"""
    elevenlabs_conv_ids = conversation_service.get_existing_elevenlabs_conversations(
        db=db,
        research_id=current_user.research_id
    )

    return {
        "research_id": current_user.research_id,
        "elevenlabs_conversation_ids": elevenlabs_conv_ids
    }


@router.post("/sync-elevenlabs-conversation", response_model=ElevenLabsConversationSyncResponse)
async def sync_elevenlabs_conversation(
    data: ElevenLabsConversationSyncRequest,
    current_user: ResearchID = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Fetch an ElevenLabs conversation transcript and sync it to the database.

    This endpoint retrieves a conversation from the ElevenLabs API using the
    conversation ID and saves all messages to the PostgreSQL database for research purposes.
    """
    # Verify user matches research_id in request
    if current_user.research_id != data.research_id:
        raise HTTPException(status_code=403, detail="Research ID mismatch")

    settings = get_settings()

    try:
        # Fetch conversation from ElevenLabs API
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.elevenlabs.io/v1/convai/conversations/{data.elevenlabs_conversation_id}",
                headers={
                    "xi-api-key": settings.ELEVENLABS_API_KEY
                }
            )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Failed to fetch conversation from ElevenLabs: {response.text}"
                )

            conversation_data = response.json()

        # Get the research_id_fk
        research_user = db.query(ResearchID).filter(
            ResearchID.research_id == data.research_id
        ).first()

        if not research_user:
            raise HTTPException(status_code=404, detail="Research ID not found")

        # Use ElevenLabs conversation_id as our conversation_id
        conversation_id = data.elevenlabs_conversation_id

        # Process and save messages
        messages_synced = 0

        if conversation_data.get("transcript") and isinstance(conversation_data["transcript"], list):
            for message in conversation_data["transcript"]:
                # Parse message fields (ElevenLabs format may vary)
                role = "user" if message.get("role") == "user" else "assistant"
                content = message.get("message") or message.get("text") or ""

                # Skip empty messages
                if not content.strip():
                    continue

                # Parse timestamp
                timestamp_str = message.get("timestamp")
                if timestamp_str:
                    try:
                        timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                    except (ValueError, AttributeError):
                        timestamp = datetime.now()
                else:
                    timestamp = datetime.now()

                # Check if message already exists (avoid duplicates)
                elevenlabs_message_id = message.get("id")
                existing_message = None

                if elevenlabs_message_id:
                    existing_message = db.query(Conversation).filter(
                        Conversation.elevenlabs_message_id == elevenlabs_message_id
                    ).first()

                # Only save if not already in database
                if not existing_message:
                    db_message = Conversation(
                        research_id_fk=research_user.id,
                        conversation_id=conversation_id,
                        role=role,
                        content=content,
                        timestamp=timestamp,
                        provider="elevenlabs",
                        elevenlabs_conversation_id=data.elevenlabs_conversation_id,
                        elevenlabs_message_id=elevenlabs_message_id
                    )
                    db.add(db_message)
                    messages_synced += 1

        db.commit()

        return ElevenLabsConversationSyncResponse(
            success=True,
            messages_synced=messages_synced,
            conversation_id=conversation_id
        )

    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to ElevenLabs API: {str(e)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to sync conversation: {str(e)}")
