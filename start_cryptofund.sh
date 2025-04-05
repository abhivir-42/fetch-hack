#!/bin/bash

# Script to start the CryptoFund application
# This starts both the backend API server and the frontend

# Ensure we're in the right directory
cd "$(dirname "$0")"

# Print banner
echo "======================================="
echo "  Starting CryptoFund Application"
echo "======================================="

# Start the API server in the background
echo "Starting API Server..."
./run_api_server.sh &
API_PID=$!

# Wait for API server to start
echo "Waiting for API server to start..."
sleep 3

# Check if the API server is running
if ! ps -p $API_PID > /dev/null; then
    echo "API server failed to start. Check logs for details."
    exit 1
fi

# Start the frontend
echo "Starting Frontend..."
cd migrate/06_frontend
npm run dev &
FRONTEND_PID=$!

# Wait for frontend to start
echo "Waiting for frontend to start..."
sleep 5

# Print success message
echo ""
echo "======================================="
echo "CryptoFund application is now running!"
echo "API Server: http://localhost:8000/api"
echo "Frontend:   http://localhost:5173"
echo "======================================="
echo ""
echo "Press Ctrl+C to stop both servers"

# Function to clean up on exit
cleanup() {
    echo "Stopping servers..."
    kill $API_PID $FRONTEND_PID 2>/dev/null
    wait $API_PID $FRONTEND_PID 2>/dev/null
    echo "Servers stopped."
    exit 0
}

# Set up cleanup on script exit
trap cleanup INT TERM

# Wait for both processes
wait