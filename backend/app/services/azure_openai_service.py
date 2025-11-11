"""
Azure OpenAI service wrapper with mock support
"""
from openai import AzureOpenAI
from typing import List, Dict, Any
import json
from app.config.settings import settings
from app.models.summary import TimelineSummary


class AzureOpenAIService:
    """
    Wrapper for Azure OpenAI API with mock mode for testing
    """
    
    def __init__(self, use_mock: bool = False):
        """
        Initialize Azure OpenAI service
        
        Args:
            use_mock: If True, use mock responses instead of API calls
        """
        self.use_mock = use_mock or settings.use_mock_openai
        
        if not self.use_mock:
            try:
                self.client = AzureOpenAI(
                    azure_endpoint=settings.azure_openai_endpoint,
                    api_key=settings.azure_openai_key,
                    api_version=settings.azure_openai_api_version
                )
            except Exception as e:
                print(f"Warning: Could not initialize Azure OpenAI client: {e}")
                print("Falling back to mock mode")
                self.use_mock = True
    
    def generate_timeline_summary(
        self,
        transcript_segment: str,
        time_range: str,
        speakers: List[str]
    ) -> Dict[str, Any]:
        """
        Generate summary for a specific time segment
        
        Args:
            transcript_segment: Formatted transcript text for this segment
            time_range: Time range string (e.g., "0:00 - 5:00")
            speakers: List of speakers in this segment
        
        Returns:
            Dictionary with key_points, topics, and action_items
        """
        if self.use_mock:
            return self._mock_timeline_summary(transcript_segment, time_range, speakers)
        
        prompt = f"""Analyze the following meeting transcript segment and provide a structured summary.

Time Range: {time_range}
Speakers: {', '.join(speakers)}

Transcript:
{transcript_segment}

Please provide:
1. Key points discussed (as a list of 2-4 concise bullet points)
2. Main topics (as a list of 2-4 topics)
3. Action items if any (as a list, empty if none identified)

Format your response as JSON with keys: key_points, topics, action_items

Example format:
{{
    "key_points": ["Point 1", "Point 2"],
    "topics": ["Topic A", "Topic B"],
    "action_items": ["Action 1"]
}}"""
        
        try:
            response = self.client.chat.completions.create(
                model=settings.azure_openai_deployment_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert meeting summarizer. Provide concise, structured summaries in JSON format."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=500,
                response_format={"type": "json_object"}
            )
            
            # Parse response
            result = json.loads(response.choices[0].message.content)
            return result
        
        except Exception as e:
            print(f"Error calling Azure OpenAI API: {e}")
            # Fallback to mock
            return self._mock_timeline_summary(transcript_segment, time_range, speakers)
    
    def generate_overall_summary(self, all_summaries: List[TimelineSummary]) -> Dict[str, Any]:
        """
        Generate overall meeting summary from timeline summaries
        
        Args:
            all_summaries: List of TimelineSummary objects
        
        Returns:
            Dictionary with overall_summary, key_decisions, and follow_up_actions
        """
        if self.use_mock:
            return self._mock_overall_summary(all_summaries)
        
        # Combine all timeline summaries
        combined_text = "\n\n".join([
            f"Time {s.time_range}:\n"
            f"Topics: {', '.join(s.topics)}\n"
            f"Key Points:\n" + "\n".join(f"  - {point}" for point in s.key_points) +
            (f"\nAction Items:\n" + "\n".join(f"  - {item}" for item in s.action_items) if s.action_items else "")
            for s in all_summaries
        ])
        
        prompt = f"""Based on these timeline summaries from a meeting, provide an overall meeting summary:

{combined_text}

Provide:
1. A brief overall summary (2-3 sentences capturing the main purpose and outcomes)
2. Key decisions made during the meeting (as a list, empty if none)
3. Follow-up actions required (as a list, aggregated from all action items)

Format as JSON with keys: overall_summary, key_decisions, follow_up_actions

Example format:
{{
    "overall_summary": "Brief 2-3 sentence summary here",
    "key_decisions": ["Decision 1", "Decision 2"],
    "follow_up_actions": ["Action 1", "Action 2"]
}}"""
        
        try:
            response = self.client.chat.completions.create(
                model=settings.azure_openai_deployment_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at synthesizing meeting information into executive summaries."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=800,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
        
        except Exception as e:
            print(f"Error calling Azure OpenAI API: {e}")
            # Fallback to mock
            return self._mock_overall_summary(all_summaries)
    
    def _mock_timeline_summary(
        self,
        transcript: str,
        time_range: str,
        speakers: List[str]
    ) -> Dict[str, Any]:
        """
        Mock response for testing without Azure OpenAI API calls
        """
        # Extract some content from transcript for more realistic mock
        lines = transcript.split('\n')
        topics = []
        
        # Simple keyword extraction for mock topics
        keywords = ['Azure', 'Speech', 'OpenAI', 'iOS', 'backend', 'test', 'integration', 'implementation']
        for keyword in keywords:
            if any(keyword.lower() in line.lower() for line in lines):
                topics.append(keyword)
        
        if not topics:
            topics = ["General Discussion", "Planning"]
        
        return {
            "key_points": [
                "Discussed Azure Speech-to-Text integration with speaker diarization",
                "Reviewed timeline-based summarization approach using OpenAI",
                "Planned testing strategy with mock data before production"
            ][:len(lines)],  # Adjust based on content
            "topics": topics[:4],
            "action_items": [
                "Prepare mock data for testing",
                "Review progress in next meeting"
            ] if "test" in transcript.lower() or "action" in transcript.lower() else []
        }
    
    def _mock_overall_summary(self, summaries: List[TimelineSummary]) -> Dict[str, Any]:
        """
        Mock overall summary for testing
        """
        # Aggregate topics and action items
        all_topics = set()
        all_actions = []
        
        for summary in summaries:
            all_topics.update(summary.topics)
            all_actions.extend(summary.action_items)
        
        return {
            "overall_summary": (
                f"Team meeting covering {len(summaries)} discussion segments. "
                f"Main topics included {', '.join(list(all_topics)[:3])}. "
                "Agreed on implementation approach and testing strategy."
            ),
            "key_decisions": [
                "Use Python for backend prototype testing",
                "Implement timeline-based summarization with 5-minute intervals",
                "Test with mock data before Azure API integration"
            ],
            "follow_up_actions": list(set(all_actions)) if all_actions else [
                "Complete backend prototype",
                "Schedule follow-up sync meeting",
                "Prepare test scenarios"
            ]
        }
