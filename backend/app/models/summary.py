"""
Summary response models for timeline-based meeting summarization
"""
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class TimelineSummary(BaseModel):
    """
    Summary for a specific time segment of the meeting
    """
    time_range: str = Field(..., description="Time range (e.g., '0:00 - 5:00')")
    start_time: float = Field(..., description="Start time in seconds")
    end_time: float = Field(..., description="End time in seconds")
    speakers: List[str] = Field(..., description="Speakers active in this segment")
    key_points: List[str] = Field(..., description="Main points discussed")
    topics: List[str] = Field(..., description="Topics covered")
    action_items: List[str] = Field(default_factory=list, description="Action items identified")

    class Config:
        json_schema_extra = {
            "example": {
                "time_range": "0:00 - 5:00",
                "start_time": 0.0,
                "end_time": 300.0,
                "speakers": ["Speaker 1", "Speaker 2"],
                "key_points": [
                    "Discussed Azure Speech to Text integration",
                    "Reviewed speaker diarization capabilities"
                ],
                "topics": ["Azure Integration", "Technical Discussion"],
                "action_items": ["Prepare mock data for testing"]
            }
        }


class MeetingSummaryResponse(BaseModel):
    """
    Complete meeting summary with timeline-based breakdown
    """
    meeting_id: str = Field(..., description="Meeting UUID")
    generated_at: datetime = Field(default_factory=datetime.now, description="Summary generation timestamp")
    total_duration: float = Field(..., description="Total meeting duration in seconds")
    timeline_summaries: List[TimelineSummary] = Field(..., description="Time-segmented summaries")
    overall_summary: str = Field(..., description="Overall meeting summary")
    key_decisions: List[str] = Field(default_factory=list, description="Key decisions made")
    follow_up_actions: List[str] = Field(default_factory=list, description="Follow-up actions required")

    class Config:
        json_schema_extra = {
            "example": {
                "meeting_id": "550e8400-e29b-41d4-a716-446655440001",
                "generated_at": "2025-10-30T10:15:00Z",
                "total_duration": 600.0,
                "timeline_summaries": [],
                "overall_summary": "Team discussed Azure integration and testing strategy.",
                "key_decisions": ["Use Python for backend prototype"],
                "follow_up_actions": ["Complete prototype in 2 weeks"]
            }
        }
