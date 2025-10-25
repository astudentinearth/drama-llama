#!/bin/bash

# File Upload/Download Test Runner
# This script sets up the test environment and runs the tests

echo "🚀 Starting File Upload/Download Tests"
echo "======================================"

# Check if MinIO is running
echo "📋 Checking MinIO status..."
if ! docker-compose -f docker-compose.minio.yml ps | grep -q "minio.*Up"; then
    echo "⚠️  MinIO is not running. Starting MinIO..."
    docker-compose -f docker-compose.minio.yml up -d
    
    echo "⏳ Waiting for MinIO to be ready..."
    sleep 15
    
    # Check if MinIO is accessible
    if ! curl -s http://localhost:9000/minio/health/live > /dev/null; then
        echo "❌ MinIO failed to start or is not accessible"
        echo "Please check MinIO logs: docker-compose -f docker-compose.minio.yml logs minio"
        exit 1
    fi
    echo "✅ MinIO is ready"
else
    echo "✅ MinIO is already running"
fi

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Run tests
echo "🧪 Running tests..."
npm test

# Capture exit code
TEST_EXIT_CODE=$?

# Cleanup
echo "🧹 Cleaning up..."
docker-compose -f docker-compose.minio.yml down

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "✅ All tests passed!"
else
    echo "❌ Some tests failed"
fi

exit $TEST_EXIT_CODE
