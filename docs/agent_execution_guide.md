# CryptoReason Agent Execution Guide

## System Overview

CryptoReason is a multi-agent system designed for crypto market analysis and automated trading. The system uses Fetch.ai's uAgents framework to create a network of specialized agents that work together to analyze market conditions and execute trades.

## Prerequisites

Before running the agents, ensure you have:

1. Python 3.12+ installed
2. All required Python packages installed:
   ```
   pip install -r requirements.txt
   ```
3. Environment variables properly configured in `.env` file:
   - `ASI1_API_KEY` - API key for ASI-1 AI model
   - `NEWS_API_KEY` - API key for news service
   - `AGENTVERSE_API_KEY` - API key for Fetch.ai's Agentverse
   - `CMC_API_KEY` - API key for CoinMarketCap (optional)
   - `METAMASK_PRIVATE_KEY` - Private key for executing trades (if needed)

## Running the Agents

### Option 1: Automatic Startup (Recommended)

We've provided a utility script that starts all agents in the correct order with proper delays:

```bash
cd /path/to/fetch-hack/cryptoreason
python start_all_agents.py
```

This script:
- Creates a `logs` directory to store agent output
- Starts agents in the correct dependency order
- Waits between each agent launch to ensure proper initialization
- Handles graceful shutdown of all agents on Ctrl+C
- Monitors for agent crashes

### Option 2: API Wrapper + Manual Control

For more granular control, you can use the API wrapper:

1. Start the API wrapper:
   ```bash
   cd /path/to/fetch-hack/cryptoreason
   python api_wrapper.py
   ```

2. Use the API to start agents:
   - Start all agents: `curl -X POST http://localhost:5000/api/start-all`
   - Start specific agent: `curl -X POST http://localhost:5000/api/start-agent -d '{"agent":"main"}' -H "Content-Type: application/json"`
   - Check agent status: `curl http://localhost:5000/api/status`

### Option 3: Manual Startup

If you need to start agents individually, follow this order:

1. **Dependency Agents**:
   ```bash
   # Start these first (in any order)
   python reward_agent.py &
   python topup_agent.py &
   python swapland/swapfinder_agent.py &
   python swapland/base_ethTOusdc.py &
   python swapland/base_usdcTOeth.py &
   ```

2. **Service Agents**:
   ```bash
   # Start these next (in any order)
   python heartbeat_agent.py &
   python coininfo_agent.py &
   python fgi_agent.py &
   python cryptonews_agent.py &
   python asi/llm_agent.py &
   ```

3. **Main Agent** (start last):
   ```bash
   python main.py
   ```

## Expected Output

When running properly, the main agent will:

1. Log its startup info and wallet balance:
   ```
   INFO: Agent started: agent1qfrhxy23v262v5tr20qnmnjuq8k5t0mxgwdxfap945922t9v4ugqtkakea
   INFO: Hello! I'm SentimentBasedCryptoSellAlerts and my address is agent1qfrhxy23v262v5tr20qnmnjuq8k5t0mxgwdxfap945922t9v4ugqtkakea, my wallet address fetch1p78q2zeeycnwcksc4s7ap7232uautlwq2pf
   INFO: My balance is 1374.445090455 TESTFET
   ```

2. Provide an agent inspector URL:
   ```
   INFO: Agent inspector available at https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A8017&address=agent1qfrhxy23v262v5tr20qnmnjuq8k5t0mxgwdxfap945922t9v4ugqtkakea
   ```

3. Collect data from supporting agents:
   ```
   INFO: Received CoinResponse: name='Ethereum' symbol='ETH' current_price=1510.25 market_cap=18264819537.0 total_volume=21218775926.0 price_change_24h=-2.2367
   INFO: Received CryptoNewsResponse!
   INFO: Sending request to FGI sent!
   INFO: Received FGI response: data=[FearGreedData(value=17.0, value_classification='Extreme Fear', timestamp='1743984000')] status='success' timestamp='2025-04-08T16:39:53.288995+00:00'
   ```

4. Analyze data with LLM agent:
   ```
   INFO: ASI1 Agent 4 finished reasoning
   INFO: ASI1 Agent 3 finished reasoning
   INFO: ASI1 Agent 2 finished reasoning
   ```

5. If a sell signal is detected:
   ```
   CRITICAL: SELL SIGNAL DETECTED!
   INFO: Successfully executed Swapland Agent to convert ETH to USDC!
   ```

## Common Issues and Troubleshooting

1. **Agent Connection Failures**:
   - Error: `Failed to deliver message to agent1q0...`
   - Solution: Ensure the target agent is running and listening on the expected port

2. **Wallet Balance Issues**:
   - Error: `Insufficient funds to execute transaction`
   - Solution: Use topup_agent to add funds to your wallet

3. **API Key Errors**:
   - Error: `Invalid API key` or `API rate limit exceeded`
   - Solution: Check your `.env` file and ensure valid API keys

4. **Port Conflicts**:
   - Error: `Address already in use`
   - Solution: Stop any existing agent processes and restart

## Monitoring Tools

1. **Agent Inspector**:
   Use the Agentverse inspector URL provided at startup to monitor agent activity in real-time.

2. **API Status Endpoint**:
   When using the API wrapper, monitor `/api/status` for agent health.

3. **Log Files**:
   When using `start_all_agents.py`, check the logs directory for detailed output.

## Additional Resources

- [Fetch.ai Documentation](https://docs.fetch.ai/)
- [uAgents Documentation](https://docs.fetch.ai/uAgents/)
- [Agentverse Platform](https://agentverse.ai/)

## Next Steps

After confirming the agent system is running correctly, you can:

1. Launch the frontend application
2. Customize trading parameters
3. Monitor system performance
4. Scale with additional agents as needed 