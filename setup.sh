#!/bin/bash

# Install backend dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Install frontend dependencies
echo "Installing Node.js dependencies..."
npm install

# Copy logo to public directory
echo "Setting up assets..."
mkdir -p app/public
cp fetch_fund_logo.png app/public/

echo "Setup complete!" 