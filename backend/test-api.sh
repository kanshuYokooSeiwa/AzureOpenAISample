#!/bin/bash

# Test script for Meeting Summarization API

BASE_URL="http://localhost:8000"

echo "🧪 Testing Meeting Summarization API"
echo "=================================="
echo ""

# Test 1: Health check
echo "1️⃣  Testing health endpoint..."
response=$(curl -s "${BASE_URL}/health")
if [ $? -eq 0 ]; then
    echo "✅ Health check passed"
    echo "   Response: $response"
else
    echo "❌ Health check failed"
    echo "   Is the server running? Run: ./start.sh"
    exit 1
fi
echo ""

# Test 2: Mock data
echo "2️⃣  Testing mock data generation..."
response=$(curl -s "${BASE_URL}/api/meetings/mock-data")
if [ $? -eq 0 ]; then
    echo "✅ Mock data generation passed"
    segments=$(echo "$response" | python3 -c "import sys, json; print(len(json.load(sys.stdin)['transcript']))" 2>/dev/null || echo "N/A")
    echo "   Generated meeting with $segments transcript segments"
else
    echo "❌ Mock data generation failed"
fi
echo ""

# Test 3: Mock summary
echo "3️⃣  Testing mock summary generation..."
response=$(curl -s "${BASE_URL}/api/meetings/mock-summary")
if [ $? -eq 0 ]; then
    echo "✅ Mock summary generation passed"
    timelines=$(echo "$response" | python3 -c "import sys, json; print(len(json.load(sys.stdin)['summary']['timeline_summaries']))" 2>/dev/null || echo "N/A")
    echo "   Generated $timelines timeline summaries"
else
    echo "❌ Mock summary generation failed"
fi
echo ""

# Test 4: Long meeting summary
echo "4️⃣  Testing long meeting summary (30 minutes)..."
response=$(curl -s "${BASE_URL}/api/meetings/long-mock-summary?duration_minutes=30")
if [ $? -eq 0 ]; then
    echo "✅ Long meeting summary passed"
    segments=$(echo "$response" | python3 -c "import sys, json; print(json.load(sys.stdin)['timeline_segments'])" 2>/dev/null || echo "N/A")
    echo "   Generated $segments timeline segments for 30-minute meeting"
else
    echo "❌ Long meeting summary failed"
fi
echo ""

echo "=================================="
echo "✅ All tests completed!"
echo ""
echo "📝 Available endpoints:"
echo "   • Health:       ${BASE_URL}/health"
echo "   • API Docs:     ${BASE_URL}/docs"
echo "   • Mock Data:    ${BASE_URL}/api/meetings/mock-data"
echo "   • Mock Summary: ${BASE_URL}/api/meetings/mock-summary"
echo ""
echo "🎯 Try in browser: ${BASE_URL}/docs"
