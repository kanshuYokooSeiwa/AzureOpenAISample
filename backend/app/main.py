"""
FastAPI application for meeting summarization
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import uvicorn

from app.models.transcript import MeetingSession
from app.models.summary import MeetingSummaryResponse
from app.services.summarization_service import SummarizationService
from app.utils.mock_data_generator import MockDataGenerator
from app.config.settings import settings


# Initialize FastAPI app
app = FastAPI(
    title="Meeting Summarization API",
    description="Backend API for Azure Speech-to-Text meeting summarization with timeline-based analysis",
    version="0.1.0"
)

# Configure CORS for iOS app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize service with mock mode based on settings
summarization_service = SummarizationService(use_mock_openai=settings.use_mock_openai)


@app.get("/")
async def root():
    """
    Root endpoint
    """
    return {
        "message": "Meeting Summarization API",
        "version": "0.1.0",
        "endpoints": {
            "health": "/health",
            "summarize": "POST /api/meetings/summarize",
            "mock_data": "GET /api/meetings/mock-data",
            "mock_summary": "GET /api/meetings/mock-summary"
        }
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "mock_mode": settings.use_mock_openai,
        "timeline_interval": settings.timeline_interval_seconds
    }


@app.post("/api/meetings/summarize", response_model=MeetingSummaryResponse)
async def summarize_meeting(meeting: MeetingSession):
    """
    Summarize a meeting transcript with timeline-based summaries
    
    Args:
        meeting: MeetingSession object with transcript segments
    
    Returns:
        MeetingSummaryResponse with timeline summaries and overall summary
    
    Example:
        ```
        POST /api/meetings/summarize
        {
            "id": "550e8400-e29b-41d4-a716-446655440001",
            "start_time": "2025-10-30T10:00:00Z",
            "end_time": "2025-10-30T10:10:00Z",
            "duration": 600.0,
            "participants": ["Speaker 1", "Speaker 2"],
            "transcript": [...]
        }
        ```
    """
    try:
        summary = summarization_service.summarize_meeting(meeting)
        return summary
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating summary: {str(e)}"
        )


@app.get("/api/meetings/mock-data")
async def get_mock_meeting(
    duration_minutes: int = 10,
    conversation_index: int = 0
):
    """
    Get mock meeting data for testing
    
    Args:
        duration_minutes: Meeting duration (default: 10)
        conversation_index: Which sample conversation to use (0 or 1)
    
    Returns:
        MeetingSession with mock transcript data
    """
    try:
        meeting = MockDataGenerator.generate_sample_meeting(
            duration_minutes=duration_minutes,
            conversation_index=conversation_index
        )
        return meeting
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating mock data: {str(e)}"
        )


@app.get("/api/meetings/mock-summary")
async def get_mock_summary(
    duration_minutes: int = 10,
    conversation_index: int = 0
):
    """
    Get complete mock flow: generate meeting data and summarize it
    
    Args:
        duration_minutes: Meeting duration (default: 10)
        conversation_index: Which sample conversation to use (0 or 1)
    
    Returns:
        Dictionary with meeting data and summary
    """
    try:
        # Generate mock meeting
        meeting = MockDataGenerator.generate_sample_meeting(
            duration_minutes=duration_minutes,
            conversation_index=conversation_index
        )
        
        # Generate summary
        summary = summarization_service.summarize_meeting(meeting)
        
        return {
            "meeting": meeting,
            "summary": summary
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating mock summary: {str(e)}"
        )


@app.get("/api/meetings/long-mock-summary")
async def get_long_mock_summary(duration_minutes: int = 30):
    """
    Get summary for a longer meeting (useful for testing multiple timeline segments)
    
    Args:
        duration_minutes: Meeting duration (default: 30)
    
    Returns:
        Dictionary with meeting data and summary
    """
    try:
        # Generate longer mock meeting
        meeting = MockDataGenerator.generate_long_meeting(duration_minutes=duration_minutes)
        
        # Generate summary
        summary = summarization_service.summarize_meeting(meeting)
        
        return {
            "meeting": meeting,
            "summary": summary,
            "timeline_segments": len(summary.timeline_summaries)
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating long mock summary: {str(e)}"
        )


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=True
    )
