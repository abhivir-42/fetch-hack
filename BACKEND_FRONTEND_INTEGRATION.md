# Backend-Frontend Integration

This document explains how we resolved the backend-frontend integration issues in the CryptoFund project.

## Issue Summary

The frontend was initially developed using mock data instead of connecting to a real API server. The backend Python code for agents was working correctly, but we needed to build a proper API server to connect the agents to the frontend.

## Solution

### 1. Fixed Python Package Structure

- Created proper `__init__.py` files in the `cryptoreason` package and its subpackages
- This allowed proper Python module imports across the codebase

### 2. Created a Dedicated API Server

Created a new file `cryptoreason/working_api_server.py` that:

- Sets up a Flask server with CORS support on port 8000
- Exposes RESTful API endpoints that match what the frontend expects
- Correctly imports from the `cryptoreason` package
- Provides both mock data and attempts to use real agent data when available
- Implements proper error handling and state management

### 3. Updated Frontend API Clients

Modified the frontend API client files to use the real API endpoints:

- Updated `apiClient.ts` to point to `http://localhost:8000/api`
- Replaced mock implementations in:
  - `market.ts`
  - `agents.ts`
  - `wallet.ts`
  - `auth.ts`
- Kept fallback behavior for endpoints not yet implemented in the API server

### 4. Created Helper Scripts

- `install_api_dependencies.sh`: Installs required Python packages for the API server
- `run_api_server.sh`: Sets up the Python path and runs the API server

## How to Run

1. First, start the API server:
   ```
   ./run_api_server.sh
   ```

2. Then, start the frontend development server:
   ```
   cd migrate/06_frontend
   npm run dev
   ```

3. Access the application at http://localhost:5173

## API Endpoints

The API server exposes the following endpoints:

- `/api/health`: Health check endpoint
- `/api/agents`: List all registered agents
- `/api/market-data`: Get latest market data
- `/api/transactions`: Get transaction history
- `/api/heartbeat`: Get heartbeat data
- `/api/market/data`: Get market data for coins
- `/api/market/prices`: Get price history for a specific coin
- `/api/wallet/connect`: Connect wallet endpoint
- `/api/wallet/balance`: Get wallet balance
- `/api/wallet/topup`: Topup wallet
- `/api/wallet/disconnect`: Disconnect wallet
- `/api/auth/login`: Login endpoint
- `/api/trigger-analysis`: Trigger market analysis
- `/api/update-heartbeat`: Update heartbeat data

## Future Improvements

1. Add proper authentication and authorization
2. Implement real endpoints for all mock data
3. Add proper error handling and logging
4. Add full integration tests
5. Add persistent storage
6. Add WebSocket support for real-time updates 