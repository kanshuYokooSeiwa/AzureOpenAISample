"""
Business logic for meeting summarization
"""
from typing import List
from datetime import datetime
from app.models.transcript import MeetingSession, TranscriptSegment
from app.models.summary import TimelineSummary, MeetingSummaryResponse
from app.services.azure_openai_service import AzureOpenAIService
from app.config.settings import settings


class SummarizationService:
    """
    Service for generating timeline-based meeting summaries
    """
    
    def __init__(self, use_mock_openai: bool = False):
        """
        Initialize summarization service
        
        Args:
            use_mock_openai: If True, use mock OpenAI responses for testing
        """
        self.openai_service = AzureOpenAIService(use_mock=use_mock_openai)
        self.timeline_interval = settings.timeline_interval_seconds
    
    def summarize_meeting(self, meeting: MeetingSession) -> MeetingSummaryResponse:
        """
        Generate timeline-based summary for entire meeting
        
        Args:
            meeting: MeetingSession with transcript data
        
        Returns:
            MeetingSummaryResponse with timeline summaries and overall summary
        """
        # Split transcript into time segments
        timeline_segments = self._split_into_timelines(meeting.transcript, meeting.duration)
        
        # Generate summary for each timeline
        timeline_summaries = []
        for segment_data in timeline_segments:
            summary = self._summarize_timeline_segment(segment_data)
            timeline_summaries.append(summary)
        
        # Generate overall summary
        overall_data = self.openai_service.generate_overall_summary(timeline_summaries)
        
        return MeetingSummaryResponse(
            meeting_id=str(meeting.id),
            generated_at=datetime.now(),
            total_duration=meeting.duration,
            timeline_summaries=timeline_summaries,
            overall_summary=overall_data.get("overall_summary", "No summary available"),
            key_decisions=overall_data.get("key_decisions", []),
            follow_up_actions=overall_data.get("follow_up_actions", [])
        )
    
    def _split_into_timelines(
        self,
        segments: List[TranscriptSegment],
        total_duration: float
    ) -> List[dict]:
        """
        Split transcript into time-based segments
        
        Args:
            segments: All transcript segments
            total_duration: Total meeting duration in seconds
        
        Returns:
            List of dictionaries with start_time, end_time, and segments
        """
        timelines = []
        current_time = 0.0
        
        while current_time < total_duration:
            end_time = min(current_time + self.timeline_interval, total_duration)
            
            # Get segments in this time range
            range_segments = [
                s for s in segments 
                if s.start_time >= current_time and s.start_time < end_time
            ]
            
            # Only add timeline if there are segments in it
            if range_segments:
                timelines.append({
                    "start_time": current_time,
                    "end_time": end_time,
                    "segments": range_segments
                })
            
            current_time = end_time
        
        return timelines
    
    def _summarize_timeline_segment(self, segment_data: dict) -> TimelineSummary:
        """
        Generate summary for a single timeline segment
        
        Args:
            segment_data: Dictionary with start_time, end_time, and segments
        
        Returns:
            TimelineSummary with key points, topics, and action items
        """
        start = segment_data["start_time"]
        end = segment_data["end_time"]
        segments = segment_data["segments"]
        
        # Format time range
        time_range = f"{self._format_time(start)} - {self._format_time(end)}"
        
        # Combine transcript text with speaker labels
        transcript_text = "\n".join([
            f"{seg.speaker_id}: {seg.text}" for seg in segments
        ])
        
        # Get unique speakers in this segment
        speakers = list(set(seg.speaker_id for seg in segments))
        speakers.sort()
        
        # Generate summary using OpenAI
        summary_data = self.openai_service.generate_timeline_summary(
            transcript_text,
            time_range,
            speakers
        )
        
        return TimelineSummary(
            time_range=time_range,
            start_time=start,
            end_time=end,
            speakers=speakers,
            key_points=summary_data.get("key_points", []),
            topics=summary_data.get("topics", []),
            action_items=summary_data.get("action_items", [])
        )
    
    @staticmethod
    def _format_time(seconds: float) -> str:
        """
        Format seconds to MM:SS or H:MM:SS
        
        Args:
            seconds: Time in seconds
        
        Returns:
            Formatted time string
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes}:{secs:02d}"
