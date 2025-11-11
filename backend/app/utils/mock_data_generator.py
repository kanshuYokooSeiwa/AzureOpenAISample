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
            ("Speaker 1", 0, 15, "皆さん、おはようございます。会議を始めましょう。"),
            ("Speaker 2", 15, 30, "会議の準備ありがとうございます。Azureの統合について話し合いたいと思います。"),
            ("Speaker 1", 30, 50, "はい、話者分離機能を使ったAzure Speech to Textの実装に取り組んでいます。"),
            ("Speaker 3", 50, 70, "それは素晴らしいですね。要約機能についてはどうですか？"),
            ("Speaker 1", 70, 95, "タイムラインベースの要約にAzure OpenAIを使用する予定です。"),
            ("Speaker 2", 95, 120, "本番環境にする前に、まずモックデータでテストすべきだと思います。"),
            ("Speaker 1", 120, 145, "もちろんです。プロンプトとレスポンス形式を検証する必要があります。"),
            ("Speaker 3", 145, 165, "最初のプロトタイプはいつ頃できそうですか？"),
            ("Speaker 1", 165, 185, "バックエンドのPythonバージョンは2週間で完成する見込みです。"),
            ("Speaker 2", 185, 210, "完璧ですね。来週また進捗を確認するために集まりましょう。"),
        ],
        [
            ("Speaker 1", 0, 20, "iOSの実装の詳細について話し合いましょう。"),
            ("Speaker 2", 20, 45, "Microsoft Cognitive Services Speech SDKを追加するためにCocoaPodsを使う必要があります。"),
            ("Speaker 1", 45, 70, "そうですね。それと、Azureの認証情報を安全に設定する必要があります。"),
            ("Speaker 3", 70, 95, "キーチェーンに保存すべきでしょうか？"),
            ("Speaker 2", 95, 115, "はい、それがiOSアプリのベストプラクティスです。"),
            ("Speaker 1", 115, 140, "会話文字起こしモードで継続的な認識も実装する必要があります。"),
            ("Speaker 3", 140, 165, "話者分離を有効にすることを忘れないでください。"),
            ("Speaker 2", 165, 190, "タイムライン機能のために単語レベルのタイムスタンプも取得する必要があります。"),
            ("Speaker 1", 190, 215, "AudioRecordingManagerとAzureSpeechServiceクラスを作成します。"),
            ("Speaker 3", 215, 240, "いいですね。明日、初期実装をレビューするために会いましょう。"),
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
