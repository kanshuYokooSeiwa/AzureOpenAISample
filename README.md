# AzureOpenAI Meeting Summarization Sample

This is a sample project for meeting transcript summarization using Azure Speech-to-Text and Azure OpenAI.

## Architecture

- **Frontend**: iOS (iPhone/iPad) with Azure Speech SDK
  - Records audio in meetings
  - Uses Azure Speech-to-Text with conversation transcription mode
  - Provides speaker diarization and word-level timestamps
  
- **Backend**: Python FastAPI (this prototype) → Java Spring (production)
  - Receives transcripts from iOS
  - Generates timeline-based summaries using Azure OpenAI
  - Returns structured summaries to iOS app

## Quick Start

### 1. Setup Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### 2. Configure Environment

The `.env` file is already created with mock mode enabled (no Azure credentials needed for testing):

```bash
# .env is pre-configured with:
USE_MOCK_OPENAI=true
TIMELINE_INTERVAL_SECONDS=300
```

### 3. Run the Server

```bash
# From backend directory with venv activated
python -m uvicorn app.main:app --reload --port 8000
```

### 4. Test the API

Open another terminal and try:

```bash
# Health check
curl http://localhost:8000/health

# Get mock meeting summary
curl http://localhost:8000/api/meetings/mock-summary | python -m json.tool
```

### 5. Test with Jupyter Notebook

```bash
cd backend
jupyter notebook notebooks/azure_openai_wrapper_test.ipynb
```

## Features

✅ **Timeline-based Summarization** - Breaks meetings into 5-minute segments  
✅ **Speaker Diarization Support** - Handles multi-speaker conversations  
✅ **Mock Mode** - Test without Azure OpenAI API (enabled by default)  
✅ **REST API** - FastAPI endpoints ready for iOS integration  
✅ **Mock Data Generator** - Built-in test data  
✅ **Jupyter Notebook** - Interactive testing environment  

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/api/meetings/mock-data` | GET | Generate mock meeting data |
| `/api/meetings/mock-summary` | GET | Generate mock meeting with summary |
| `/api/meetings/summarize` | POST | Summarize a meeting transcript |
| `/api/meetings/long-mock-summary` | GET | Test with 30-minute meeting |

## Documentation

See [`backend/README.md`](backend/README.md) for detailed documentation including:
- Full API documentation
- Data models
- Azure OpenAI configuration
- iOS integration guide
- Deployment instructions

## Next Steps

### For Testing (Current State - No Azure Required)
1. ✅ Backend is ready to run in mock mode
2. ✅ Test API endpoints with curl or Postman
3. ✅ Explore Jupyter notebook for interactive testing
4. Test iOS integration with mock backend

### For Production (Real Azure OpenAI)
1. Create Azure OpenAI resource
2. Update `backend/.env` with credentials
3. Set `USE_MOCK_OPENAI=false`
4. Test with real API

### For Java Migration
1. Validate Python prototype
2. Port models to Java POJOs
3. Implement with Spring Boot
4. Use Azure OpenAI Java SDK

## License

Sample project for Azure integration testing.
