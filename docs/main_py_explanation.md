# Main.py Script Explanation

## Overview
The `main.py` script is a sophisticated agent-based system designed for cryptocurrency sentiment analysis and trading alerts. It leverages the Fetch.ai uAgents framework to create an intelligent agent that monitors and analyzes cryptocurrency markets.

## Key Components

### Agent Initialization
- **Name**: SentimentBased CryptoSellAlerts
- **Port**: 8017
- **Wallet**: Automatically generated fetch wallet
- **Functionality**: Multi-agent communication system for crypto market analysis

### Main Agent Capabilities
1. **Startup Logging**
   - Logs agent address and initial wallet balance
   - Provides agent inspector URL for monitoring

2. **Periodic Checks**
   - Runs a 24-hour interval check via `swapland_request` method
   - Sends heartbeat to verify system readiness

3. **Wallet Management**
   - Supports wallet top-up functionality
   - Handles payment requests for services

### Communication Agents
The script defines interactions with several specialized agents:
- Heartbeat Agent
- Coin Information Agent
- Crypto News Agent
- Fear & Greed Index (FGI) Agent
- Swap Land Agent
- Reward Agent
- Topup Agent

## Interaction Flow
1. Agent starts up and logs initial information
2. Periodically checks market conditions
3. Can request wallet top-up
4. Communicates with various specialized agents to:
   - Fetch coin information
   - Get crypto news
   - Analyze market sentiment
   - Potentially execute trades

## Expected Output

When running properly, you should see the following stages of output:

### 1. Initialization
```
INFO: [SentimentBasedCryptoSellAlerts]: Starting agent with address: agent1qfrhxy23v262v5tr20qnmnjuq8k5t0mxgwdxfap945922t9v4ugqtkakea
INFO: root: ✅ Agent started: agent1qfrhxy23v262v5tr20qnmnjuq8k5t0mxgwdxfap945922t9v4ugqtkakea
INFO: [SentimentBasedCryptoSellAlerts]: Hello! I'm SentimentBasedCryptoSellAlerts and my address is agent1qfrhxy23v262v5tr20qnmnjuq8k5t0mxgwdxfap945922t9v4ugqtkakea, my wallet address fetch1p78q2zeeycnwcksc4s7ap7232uautlwq2pf
INFO: [SentimentBasedCryptoSellAlerts]: My balance is 1374.445090455 TESTFET
INFO: [SentimentBasedCryptoSellAlerts]: Agent inspector available at https://agentverse.ai/inspect/?uri=httpp3A//127.0.0.1:938A8017&address=agent1qfrhxy23v262v5tr20qnmnjuq8k5t0mxgwdxfap945922t9v4ugqtkakea
INFO: [SentimentBasedCryptoSellAlerts]: Starting server on http://0.0.0.0:8017 (Press CTRL+C to quit)
INFO: [uagents.registration]: Registration on Almanac API successful
INFO: [uagents.registration]: Almanac contract registration is up to date!
```

### 2. Wallet Top-up and Fee Payment
```
INFO: root: 📈 User's wallet topped up. Success! Received responsecontinue. LETS trade
INFO: [SentimentBasedCryptoSellAlerts]: Balance after topup wallet: 1384.445090455 TESTFET
INFO: [SentimentBasedCryptoSellAlerts]: Received top-up status sent
INFO: [SentimentBasedCryptoSellAlerts]: Received message from agent1qde8udnttat2mmq3srkrz60wn3r0qnmnjuq8k5t0mxgwdxfap9453228wy2guywewtesd737x3wsru: wallet: address=atestfet amount=6000000000000000000 denom='atestfet'
INFO: [SentimentBasedCryptoSellAlerts]: Fees transaction successful!
INFO: [SentimentBasedCryptoSellAlerts]: Balance after fees: 1378.445094885 TESTFET
```

### 3. Data Collection
```
INFO: root: 📈 Received CoinResponse: name='Ethereum' symbol='ETH' current_price=1510.25 market_cap=18264819537.0 total_volume=21218775926.0 price_change_24h=-2.2367
INFO: root: 📈 Received CryptoNewsResponse!
INFO: root: 📈 Sending request to FGI sent!
INFO: root: 📈 Received FGI response: data=[FearGreedData(value=17.0, value_classification='Extreme Fear', timestamp='1743984000')] status='success' timestamp='2025-04-08T16:39:53.288995+00:00'
```

### 4. AI Analysis
```
INFO: root: ✅ ASI1 Agent 4 finished reasoning
INFO: root: ✅ ASI1 Agent 3 finished reasoning
INFO: root: ✅ ASI1 Agent 2 finished reasoning
CRITICAL: root: ✅ SELL SIGNAL DETECTED!
```

### 5. Trade Execution
```
INFO: [SentimentBasedCryptoSellAlerts]: Received message from agent1q0jnt3skqarpj3ktu231j3yyx5uvp71g2zcdku3vds1n2u8kw7v5tpv73: Successfully sent request to Swapland Agent!
INFO: [SentimentBasedCryptoSellAlerts]: Successfully executed Swapland Agent to convert ETH to USDC!
INFO: [SentimentBasedCryptoSellAlerts]: Receive transaction info from agent1qde8udnttat2mmq3srkrz60wn3r0qnmnjuq8k5t0mxgwdxfap9453228wy2guywewtesd737x3wsru: tx_hash='FDE4A9C4D0312752235F2A85B80C738BF2245D184.3b2rkea3b294y943528wy2guywewtesd737x3wsru'
INFO: [SentimentBasedCryptoSellAlerts]: Reward transaction was successful: {'receiver': 'fetch1p78q2zeeycnwcksc4s7ap7232uautlwq2pf', 'amount': '2000000000000000000 atestfet'}
INFO: [SentimentBasedCryptoSellAlerts]: Balance after reward: 1380.445094885 TESTFET
```

## Troubleshooting Common Issues

### Connection Failures
If you see errors like this:
```
ERROR: Failed to deliver message to agent1q0l8njjeaakxa87q08mr46ayqh0wf32x68k2xssuh4604wktpwxlzrt090k @ ['http://localhost:5011/api/webhook']
```
This indicates that the target agent is not running or is not accessible at the expected endpoint. Ensure all dependent agents are running.

### Agent Communication Flow
For proper functioning, agents must be started in the correct order:
1. Start all dependency agents (reward, topup, swap)
2. Start all service agents (heartbeat, coin, news, FGI)
3. Start the main agent last

## Potential Limitations/Observations
- Requires multiple environment variables
- Some hardcoded values suggest work-in-progress
- Relies on external agent services
- Error handling for agent communication

## Environment Requirements
- Python 3.12
- uAgents framework
- Fetch.ai testnet access
- API keys for various services

## Recommended Next Steps
1. Complete agent registration process
2. Implement full agent communication logic
3. Add more robust error handling
4. Create frontend integration points

## Notes for Frontend Integration
- Use agent inspector URL for real-time monitoring
- Implement WebSocket or polling mechanism to fetch agent status
- Handle potential communication failures gracefully 