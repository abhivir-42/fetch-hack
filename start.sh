#!/bin/bash

# Start the Flask API server in the background
echo "Starting Flask API server on port 8000..."
python cryptoreason/api_wrapper.py &
API_PID=$!

# Wait for API server to start
echo "Waiting for API server to start..."
sleep 5

# Start the Next.js development server
echo "Starting Next.js development server..."
npm run dev

# Function to handle termination
cleanup() {
  echo "Shutting down servers..."
  kill $API_PID
  exit 0
}

# Set up trap to handle termination
trap cleanup SIGINT SIGTERM

# Wait for interruption
wait 