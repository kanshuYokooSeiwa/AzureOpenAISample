# Meeting Summarization Backend

Python backend prototype for Azure Speech-to-Text meeting summarization with timeline-based analysis using Azure OpenAI.

## Overview

This backend application receives meeting transcripts from an iOS app (using Azure Speech-to-Text with speaker diarization) and generates timeline-based summaries using Azure OpenAI.

### Features

- ✅ **Timeline-based Summarization**: Breaks meetings into 5-minute segments
- ✅ **Speaker Diarization Support**: Handles multi-speaker conversations
- ✅ **Mock Mode**: Test without Azure OpenAI API calls
- ✅ **REST API**: FastAPI endpoints for iOS integration
- ✅ **Mock Data Generator**: Built-in test data for development
- ✅ **Jupyter Notebook**: Interactive testing environment

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                          # FastAPI application
│   ├── models/
│   │   ├── __init__.py
│   │   ├── transcript.py                # Data models for transcripts
│   │   └── summary.py                   # Data models for summaries
│   ├── services/
│   │   ├── __init__.py
│   │   ├── azure_openai_service.py      # Azure OpenAI wrapper
│   │   └── summarization_service.py     # Business logic
│   ├── utils/
│   │   ├── __init__.py
│   │   └── mock_data_generator.py       # Mock data for testing
│   └── config/
│       ├── __init__.py
│       └── settings.py                  # Configuration
├── tests/
│   ├── __init__.py
│   └── mock_data/
│       └── sample_transcript.json
├── notebooks/
│   └── azure_openai_wrapper_test.ipynb  # Testing notebook
├── requirements.txt
├── .env.example
├── .env
└── README.md
```

## Setup

### 1. Create Virtual Environment

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Edit `.env`:

```env
# For Testing (Mock Mode - No API required)
USE_MOCK_OPENAI=true

# For Production (Real Azure OpenAI)
USE_MOCK_OPENAI=false
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
```

## Running the Application

### Start API Server

```bash
# Make sure you're in the backend directory with venv activated
cd backend
source venv/bin/activate

# Run the server
python -m uvicorn app.main:app --reload --port 8000
```

Server will start at: `http://localhost:8000`

### API Endpoints

#### Health Check
```bash
curl http://localhost:8000/health
```

#### Get Mock Meeting Data
```bash
curl http://localhost:8000/api/meetings/mock-data
```

#### Generate Summary from Mock Data
```bash
curl http://localhost:8000/api/meetings/mock-summary
```

#### Summarize Custom Meeting (POST)
```bash
curl -X POST http://localhost:8000/api/meetings/summarize \
  -H "Content-Type: application/json" \
  -d @tests/mock_data/sample_transcript.json
```

#### Get Long Meeting Summary (30 minutes, multiple timeline segments)
```bash
curl "http://localhost:8000/api/meetings/long-mock-summary?duration_minutes=30"
```

## Testing with Jupyter Notebook

### Start Jupyter

```bash
cd backend
source venv/bin/activate
jupyter notebook notebooks/azure_openai_wrapper_test.ipynb
```

The notebook includes:
- Mock data generation
- Timeline-based summarization testing
- Azure OpenAI wrapper testing
- Full end-to-end flow examples

## Data Models

### TranscriptSegment (Input from iOS)

```json
{
  "id": "uuid",
  "speaker_id": "Speaker 1",
  "text": "Meeting transcript text",
  "start_time": 0.0,
  "end_time": 15.0,
  "confidence": 0.95,
  "timestamp": "2025-10-30T10:00:00Z"
}
```

### MeetingSession (Input from iOS)

```json
{
  "id": "uuid",
  "start_time": "2025-10-30T10:00:00Z",
  "end_time": "2025-10-30T10:10:00Z",
  "duration": 600.0,
  "participants": ["Speaker 1", "Speaker 2"],
  "transcript": [...]
}
```

### MeetingSummaryResponse (Output to iOS)

```json
{
  "meeting_id": "uuid",
  "generated_at": "2025-10-30T10:15:00Z",
  "total_duration": 600.0,
  "timeline_summaries": [
    {
      "time_range": "0:00 - 5:00",
      "start_time": 0.0,
      "end_time": 300.0,
      "speakers": ["Speaker 1", "Speaker 2"],
      "key_points": ["Point 1", "Point 2"],
      "topics": ["Topic A", "Topic B"],
      "action_items": ["Action 1"]
    }
  ],
  "overall_summary": "Meeting summary text",
  "key_decisions": ["Decision 1"],
  "follow_up_actions": ["Action 1"]
}
```

## Mock Mode vs Production Mode

### Mock Mode (Default)
- Set `USE_MOCK_OPENAI=true` in `.env`
- No Azure OpenAI API calls
- Returns predefined summaries
- Perfect for development and testing
- No costs incurred

### Production Mode
- Set `USE_MOCK_OPENAI=false` in `.env`
- Requires Azure OpenAI credentials
- Makes actual API calls to Azure
- Real AI-generated summaries
- API costs apply

## Configuration Options

Edit `backend/.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `USE_MOCK_OPENAI` | Use mock mode for testing | `true` |
| `TIMELINE_INTERVAL_SECONDS` | Timeline segment duration | `300` (5 min) |
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint | - |
| `AZURE_OPENAI_KEY` | Azure OpenAI API key | - |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | Model deployment name | `gpt-4` |
| `API_HOST` | API server host | `0.0.0.0` |
| `API_PORT` | API server port | `8000` |

## Testing

### Run Tests
```bash
# TODO: Add pytest tests
pytest tests/
```

### Manual Testing with curl

1. **Test health endpoint:**
```bash
curl http://localhost:8000/health
```

2. **Get mock data:**
```bash
curl http://localhost:8000/api/meetings/mock-data | jq .
```

3. **Get mock summary:**
```bash
curl http://localhost:8000/api/meetings/mock-summary | jq .
```

4. **Test with different durations:**
```bash
curl "http://localhost:8000/api/meetings/mock-summary?duration_minutes=15" | jq .
```

## iOS Integration

### iOS App Flow

1. **Record audio** using iOS device
2. **Transcribe with Azure Speech SDK** (conversation transcription mode)
   - Captures speaker diarization
   - Word-level timestamps
   - Real-time transcription
3. **Send transcript to backend** via POST request
4. **Receive timeline-based summary**
5. **Display in iOS app**

### Example iOS Request

```swift
let url = URL(string: "http://localhost:8000/api/meetings/summarize")!
var request = URLRequest(url: url)
request.httpMethod = "POST"
request.addValue("application/json", forHTTPHeaderField: "Content-Type")

let meeting = MeetingSession(/* ... */)
let encoder = JSONEncoder()
encoder.dateEncodingStrategy = .iso8601
request.httpBody = try encoder.encode(meeting)

let task = URLSession.shared.dataTask(with: request) { data, response, error in
    if let data = data {
        let summary = try JSONDecoder().decode(MeetingSummaryResponse.self, from: data)
        // Display summary in UI
    }
}
task.resume()
```

## Next Steps for Production

### 1. Switch to Real Azure OpenAI
- Create Azure OpenAI resource
- Update `.env` with credentials
- Set `USE_MOCK_OPENAI=false`
- Test with actual API

### 2. Add Authentication
- Implement API key authentication
- Add JWT tokens for iOS app
- Secure endpoints

### 3. Add Database
- Store meeting transcripts
- Cache summaries
- Track usage

### 4. Deploy Backend
- Containerize with Docker
- Deploy to Azure App Service
- Configure CORS for iOS app domain
- Set up monitoring

### 5. Java Implementation
- Port models to Java POJOs
- Implement with Spring Boot
- Use Azure OpenAI Java SDK
- Add JPA for persistence

## Development Notes

### Why Python First?
- Rapid prototyping
- Test Azure OpenAI integration
- Validate prompts and response formats
- Iterate on timeline segmentation logic
- Confirm iOS data model compatibility

### Migration to Java
Once validated, port to Java Spring Boot for production:
- Better integration with existing Java backend
- Type safety
- Enterprise features
- Team expertise

## Troubleshooting

### Import Errors
Make sure virtual environment is activated:
```bash
source venv/bin/activate
```

### Port Already in Use
Change port in `.env` or command line:
```bash
uvicorn app.main:app --port 8001
```

### Azure OpenAI Errors
Check credentials in `.env` or switch to mock mode:
```bash
USE_MOCK_OPENAI=true
```

## License

This is a sample project for testing Azure integration.

## Contact

For questions about the Java implementation or production deployment, contact the development team.
