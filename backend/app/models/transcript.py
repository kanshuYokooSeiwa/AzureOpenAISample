"""
Transcript data models matching iOS implementation
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import UUID, uuid4


class TranscriptSegment(BaseModel):
    """
    Individual transcript segment from Azure Speech-to-Text
    Matches iOS TranscriptSegment structure
    """
    id: UUID = Field(default_factory=uuid4)
    speaker_id: str = Field(..., description="Speaker identifier (e.g., 'Speaker 1', 'Speaker 2')")
    text: str = Field(..., description="Transcribed text content")
    start_time: float = Field(..., description="Start time in seconds from meeting start")
    end_time: float = Field(..., description="End time in seconds from meeting start")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score from speech recognition")
    timestamp: datetime = Field(default_factory=datetime.now, description="Absolute timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "speaker_id": "Speaker 1",
                "text": "Good morning everyone. Let's start the meeting.",
                "start_time": 0.0,
                "end_time": 15.0,
                "confidence": 0.95,
                "timestamp": "2025-10-30T10:00:00Z"
            }
        }


class MeetingSession(BaseModel):
    """
    Complete meeting session with transcript
    Matches iOS MeetingSession structure
    """
    id: UUID = Field(default_factory=uuid4)
    start_time: datetime = Field(..., description="Meeting start time")
    end_time: Optional[datetime] = Field(None, description="Meeting end time")
    duration: float = Field(..., description="Total duration in seconds")
    participants: List[str] = Field(..., description="List of speaker IDs")
    transcript: List[TranscriptSegment] = Field(..., description="All transcript segments")
    audio_file_url: Optional[str] = Field(None, description="Optional audio file URL")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440001",
                "start_time": "2025-10-30T10:00:00Z",
                "end_time": "2025-10-30T10:10:00Z",
                "duration": 600.0,
                "participants": ["Speaker 1", "Speaker 2", "Speaker 3"],
                "transcript": [],
                "audio_file_url": None
            }
        }
