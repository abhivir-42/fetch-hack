# Fetch Fund - AI-Powered Crypto Trading Platform

A web application that leverages Fetch.ai agents to analyze cryptocurrency market conditions and provide trading recommendations.

## Features

- User input form to customize trading parameters
- Real-time market data and sentiment analysis
- AI-powered trading recommendations (BUY/SELL/HOLD)
- Transaction history tracking
- Multi-agent architecture for comprehensive analysis

## Project Structure

- `app/` - Next.js frontend application
- `cryptoreason/` - Python backend with Fetch.ai agents
- `docs/` - Documentation files

## Requirements

- Node.js 14+ and npm
- Python 3.12
- Fetch.ai uAgents package and other Python dependencies
- API keys (stored in .env)

## Quick Start

We have prepared convenience scripts to make setup and running easier:

```bash
# Make scripts executable (if not already)
chmod +x setup.sh start.sh run_api.sh

# Setup the project (installs dependencies)
./setup.sh

# Start both backend and frontend
./start.sh
```

After running these commands, you can access:
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

## Manual Setup Instructions

### Backend Setup

1. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Configure environment variables in `.env`:
   ```
   ASI1_API_KEY=your_api_key
   NEWS_API_KEY=your_api_key
   AGENTVERSE_API_KEY=your_api_key
   CMC_API_KEY=your_api_key
   METAMASK_PRIVATE_KEY=your_private_key
   ```

3. Start the Flask API wrapper:
   ```
   python cryptoreason/api_wrapper.py
   ```

### Frontend Setup

1. Install Node.js dependencies:
   ```
   npm install
   ```

2. Run the development server:
   ```
   npm run dev
   ```

3. Build for production:
   ```
   npm run build
   npm start
   ```

## Usage Guide

1. Access the web application at `http://localhost:3000`
2. Navigate to the Trade page
3. Fill in your trading parameters:
   - Choose whether to top up your wallet
   - Enter your EVM private key (used for executing trades)
   - Select a network (Ethereum, Base, Polygon, Bitcoin)
   - Choose your investor type and risk strategy
   - Provide a reason for your trade
4. Submit the form to receive AI-powered recommendations
5. View the recommendation (BUY/SELL/HOLD)
6. Check the Dashboard to monitor market data and transaction history

## Troubleshooting

### Backend Issues

- **Agents not starting**: Check that ports are available (5000, 8000-8017)
- **API key errors**: Verify all API keys in the .env file are correct
- **Database errors**: Check that required data files exist in the data/ directory
- **Environment issues**: Ensure Python 3.12 is being used

### Frontend Issues

- **Build errors**: Make sure all dependencies are installed with `npm install`
- **Connection errors**: Verify the Flask API is running on port 5000
- **Type errors**: Check that TypeScript types are correctly generated

### Common Solutions

- Restart both servers
- Clear browser cache
- Check network connectivity
- Verify that required ports are not in use by other applications

## API Endpoints

The Flask API wrapper provides these endpoints:

- `GET /api/status` - Get status of all agents
- `GET /api/market-data` - Get current market data
- `GET /api/sentiment-analysis` - Get Fear & Greed Index
- `GET /api/news` - Get latest crypto news
- `GET /api/transactions` - Get transaction history
- `POST /api/execute-trade` - Manually trigger a trade
- `POST /api/submit-inputs` - Submit user inputs for analysis
- `POST /api/start-agent` - Start a specific agent
- `POST /api/start-all` - Start all agents in the correct order

## Notes for Production

- Replace placeholder private keys with real ones
- Configure proper security measures for API keys
- Set up proper logging and monitoring
- Consider using environment-specific configurations

## Agent Architecture

The system uses multiple agents for analysis:

- Main Agent: Coordinates all other agents
- Heartbeat Agent: Monitors user sentiment
- Coin Information Agent: Provides market data
- Fear & Greed Index Agent: Market sentiment analysis
- Crypto News Agent: Aggregates news articles
- LLM Agent: Uses AI to analyze data
- Reward Agent: Handles transactions
- Topup Agent: Manages wallet balances
- Swap Agents: Execute cryptocurrency trades

## Troubleshooting

- If agents fail to start, check port availability
- Ensure all required API keys are set in the .env file
- For frontend issues, check browser console for errors
- API issues can be debugged at http://localhost:5000/api/status
