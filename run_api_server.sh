#!/bin/bash

# Ensure we're in the right directory
cd "$(dirname "$0")"

# Set up the Python path to include the project root
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Run the API server
echo "Starting CryptoFund API Server..."
python cryptoreason/working_api_server.py 