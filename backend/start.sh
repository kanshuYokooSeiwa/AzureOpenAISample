#!/bin/bash

# Quick Start Script for Meeting Summarization Backend

echo "🚀 Starting Meeting Summarization Backend Setup..."
echo ""

# Check if we're in the backend directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: Please run this script from the backend directory"
    echo "   cd backend && ./start.sh"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo "✅ Dependencies installed"
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found, copying from .env.example"
    cp .env.example .env
fi

echo "🎯 Configuration:"
echo "   - Mock mode: ENABLED (no Azure credentials needed)"
echo "   - Port: 8000"
echo "   - Timeline interval: 5 minutes"
echo ""

# Start the server
echo "🚀 Starting FastAPI server..."
echo "   Server will be available at: http://localhost:8000"
echo "   API docs at: http://localhost:8000/docs"
echo ""
echo "   Press Ctrl+C to stop the server"
echo ""

python -m uvicorn app.main:app --reload --port 8000
