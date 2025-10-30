"""
Mock data generator for testing without real Azure services
"""
from typing import List
import uuid
from datetime import datetime, timedelta
from app.models.transcript import TranscriptSegment, MeetingSession


class MockDataGenerator:
    """
    Generate realistic mock meeting data for testing
    """
    
    # Sample conversation scripts
    SAMPLE_CONVERSATIONS = [
        [
            ("Speaker 1", 0, 15, "Good morning everyone. Let's start the meeting."),
            ("Speaker 2", 15, 30, "Thanks for organizing this. I'd like to discuss the Azure integration."),
            ("Speaker 1", 30, 50, "Sure, we've been working on implementing Azure Speech to Text with speaker diarization."),
            ("Speaker 3", 50, 70, "That sounds great. What about the summarization feature?"),
            ("Speaker 1", 70, 95, "We're planning to use Azure OpenAI for timeline-based summarization."),
            ("Speaker 2", 95, 120, "I think we should test it with mock data first before going live."),
            ("Speaker 1", 120, 145, "Absolutely. We need to validate the prompts and response format."),
            ("Speaker 3", 145, 165, "When do you think we can have the first prototype ready?"),
            ("Speaker 1", 165, 185, "I estimate two weeks for the backend Python version."),
            ("Speaker 2", 185, 210, "Perfect. Let's sync again next week to review progress."),
        ],
        [
            ("Speaker 1", 0, 20, "Let's discuss the iOS implementation details."),
            ("Speaker 2", 20, 45, "We need to use CocoaPods to add the Microsoft Cognitive Services Speech SDK."),
            ("Speaker 1", 45, 70, "Right. And we'll need to configure the Azure credentials securely."),
            ("Speaker 3", 70, 95, "Should we store them in the keychain?"),
            ("Speaker 2", 95, 115, "Yes, that's the best practice for iOS apps."),
            ("Speaker 1", 115, 140, "We also need to implement continuous recognition with conversation transcription mode."),
            ("Speaker 3", 140, 165, "Don't forget to enable speaker diarization."),
            ("Speaker 2", 165, 190, "And we need to capture word-level timestamps for the timeline feature."),
            ("Speaker 1", 190, 215, "I'll create the AudioRecordingManager and AzureSpeechService classes."),
            ("Speaker 3", 215, 240, "Great. Let's meet tomorrow to review the initial implementation."),
        ]
    ]
    
    @staticmethod
    def generate_sample_meeting(
        duration_minutes: int = 10,
        conversation_index: int = 0
    ) -> MeetingSession:
        """
        Generate mock meeting data for testing
        
        Args:
            duration_minutes: Total meeting duration in minutes
            conversation_index: Which sample conversation to use (0 or 1)
        
        Returns:
            MeetingSession with mock transcript data
        """
        conversation = MockDataGenerator.SAMPLE_CONVERSATIONS[
            conversation_index % len(MockDataGenerator.SAMPLE_CONVERSATIONS)
        ]
        
        start_time = datetime.now() - timedelta(minutes=duration_minutes)
        segments = []
        
        # Generate segments from conversation
        for speaker, start, end, text in conversation:
            segments.append(TranscriptSegment(
                id=uuid.uuid4(),
                speaker_id=speaker,
                text=text,
                start_time=float(start),
                end_time=float(end),
                confidence=0.92 + (hash(text) % 8) / 100,  # 0.92-0.99
                timestamp=start_time + timedelta(seconds=start)
            ))
        
        # Get unique participants
        participants = list(set(seg.speaker_id for seg in segments))
        participants.sort()
        
        # Calculate actual duration from last segment
        actual_duration = max(seg.end_time for seg in segments) if segments else duration_minutes * 60
        
        return MeetingSession(
            id=uuid.uuid4(),
            start_time=start_time,
            end_time=start_time + timedelta(seconds=actual_duration),
            duration=actual_duration,
            participants=participants,
            transcript=segments,
            audio_file_url=None
        )
    
    @staticmethod
    def generate_long_meeting(duration_minutes: int = 30) -> MeetingSession:
        """
        Generate a longer meeting by repeating and extending conversations
        
        Args:
            duration_minutes: Desired meeting duration
        
        Returns:
            MeetingSession with extended transcript
        """
        start_time = datetime.now() - timedelta(minutes=duration_minutes)
        segments = []
        current_time = 0.0
        
        # Repeat conversations to fill duration
        target_duration = duration_minutes * 60
        conversation_cycle = 0
        
        while current_time < target_duration:
            conversation = MockDataGenerator.SAMPLE_CONVERSATIONS[
                conversation_cycle % len(MockDataGenerator.SAMPLE_CONVERSATIONS)
            ]
            
            for speaker, rel_start, rel_end, text in conversation:
                abs_start = current_time + rel_start
                abs_end = current_time + rel_end
                
                if abs_start >= target_duration:
                    break
                
                # Adjust end time if it exceeds target
                if abs_end > target_duration:
                    abs_end = target_duration
                
                segments.append(TranscriptSegment(
                    id=uuid.uuid4(),
                    speaker_id=speaker,
                    text=text,
                    start_time=abs_start,
                    end_time=abs_end,
                    confidence=0.92 + (hash(text + str(conversation_cycle)) % 8) / 100,
                    timestamp=start_time + timedelta(seconds=abs_start)
                ))
                
                if abs_end >= target_duration:
                    break
            
            # Move to next conversation segment
            last_end = conversation[-1][2]
            current_time += last_end + 5  # Add 5 second pause
            conversation_cycle += 1
        
        participants = list(set(seg.speaker_id for seg in segments))
        participants.sort()
        
        return MeetingSession(
            id=uuid.uuid4(),
            start_time=start_time,
            end_time=start_time + timedelta(seconds=target_duration),
            duration=target_duration,
            participants=participants,
            transcript=segments,
            audio_file_url=None
        )
    
    @staticmethod
    def save_mock_data_to_json(filename: str = "sample_transcript.json", duration_minutes: int = 10):
        """
        Save mock data to JSON file for testing
        
        Args:
            filename: Output filename
            duration_minutes: Meeting duration
        """
        import json
        from pathlib import Path
        
        meeting = MockDataGenerator.generate_sample_meeting(duration_minutes)
        
        # Ensure directory exists
        filepath = Path(filename)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        # Save to JSON
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(meeting.model_dump(mode='json'), f, indent=2, default=str)
        
        print(f"Mock data saved to {filename}")
        return filename
