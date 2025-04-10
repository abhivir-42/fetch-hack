# Frontend Integration Guide for CryptoReason Agent System

## System Overview

CryptoReason is a multi-agent system that provides cryptocurrency market analysis and automated trading signals. The system leverages Fetch.ai's uAgents framework to create a network of specialized agents that collectively analyze market conditions and execute trades.

## Agent Architecture

### Main Agent (`main.py`)
- **Address**: agent1qfrhxny23vz62v5tr20qnmnjujq8k5t0mxgwdxfap945922t9v4ugqtqkea
- **Port**: 8017
- **Functionality**: Coordinates all other agents, processes signals, and executes trades
- **Endpoint**: http://127.0.0.1:8017/submit

### Supporting Agents
1. **Heartbeat Agent**
   - **Port**: 5011/5911
   - **Functionality**: Monitors user sentiment and market conditions periodically

2. **Coin Information Agent**
   - **Port**: 8004
   - **Functionality**: Provides real-time cryptocurrency price and market data

3. **Fear & Greed Index (FGI) Agent**
   - **Functionality**: Provides market sentiment analysis using the Fear & Greed Index

4. **Crypto News Agent**
   - **Functionality**: Aggregates and analyzes crypto news articles

5. **LLM Agent**
   - **Functionality**: Uses AI models to analyze market data and make trading decisions

6. **Reward Agent**
   - **Functionality**: Handles token rewards and transactions

7. **Topup Agent**
   - **Functionality**: Manages wallet balances and token distribution

8. **Swap Agents**
   - **Functionality**: Execute cryptocurrency swaps via DEX integrations

## Frontend Integration Points

### 1. Agent Communication

#### HTTP Endpoints
All agents expose HTTP endpoints that can be queried to retrieve information or submit requests:

```
Main Agent: http://127.0.0.1:8017/submit
Heartbeat Agent: http://127.0.0.1:5911 (or 5011)
```

#### WebSocket Integration
For real-time updates, consider implementing a WebSocket client that subscribes to agent events.

### 2. Agent Inspector URL

The Agentverse platform provides a web-based inspector for monitoring agent activity:

```
https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A8017&address=agent1qfrhxny23vz62v5tr20qnmnjujq8k5t0mxgwdxfap945922t9v4ugqtqkea
```

This can be embedded in an iframe within your frontend or used for debugging.

### 3. Data Models for Frontend

#### Market Data Model
```typescript
interface CoinData {
  name: string;
  symbol: string;
  current_price: number;
  market_cap: number;
  total_volume: number;
  price_change_24h: number;
}
```

#### Fear & Greed Data Model
```typescript
interface FearGreedData {
  value: number;
  value_classification: string;
  timestamp: string;
}
```

#### Crypto News Model
```typescript
interface CryptoNews {
  articles: Array<{
    source: { id: string; name: string };
    author: string;
    title: string;
    description: string;
    url: string;
    urlToImage: string;
    publishedAt: string;
    content: string;
  }>;
}
```

#### Transaction Model
```typescript
interface Transaction {
  tx_hash: string;
  status: string;
  amount: string;
  timestamp: string;
}
```

### 4. System State Flow

The CryptoReason system follows this typical flow:

1. **Initialization**: Main agent starts up and connects to supporting agents
2. **Data Collection**: 
   - Retrieves coin information
   - Fetches crypto news
   - Gets Fear & Greed Index
3. **Analysis**:
   - LLM agent analyzes collected data
   - Makes trading decision (BUY/SELL/HOLD)
4. **Execution**:
   - If a trade signal is generated, swap agents execute the trade
   - Transaction is recorded and rewards distributed

Your frontend should follow this flow for proper integration.

### 5. REST API Endpoints (proposed)

For frontend integration, consider implementing these REST API wrappers:

#### GET /api/market-data
Returns current market data for selected cryptocurrency

#### GET /api/sentiment-analysis
Returns the current Fear & Greed Index and sentiment analysis

#### GET /api/news
Returns latest crypto news

#### GET /api/transactions
Returns list of recent transactions

#### POST /api/execute-trade
Manually triggers a trade

## Sample Integration Code

### React Hook Example
```javascript
import { useState, useEffect } from 'react';

function useCryptoData() {
  const [marketData, setMarketData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchData() {
      try {
        const response = await fetch('http://localhost:8017/market-data');
        const data = await response.json();
        setMarketData(data);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    }

    fetchData();
    const interval = setInterval(fetchData, 60000); // Update every minute
    
    return () => clearInterval(interval);
  }, []);

  return { marketData, loading, error };
}
```

## Common Issues and Troubleshooting

### Agent Connection Issues
- Ensure all agents are running on their respective ports
- Check for port conflicts or firewall restrictions
- Verify that environment variables are properly set

### Transaction Failures
- Check agent balance on Fetch.ai testnet
- Verify that transaction parameters are correctly formatted
- Ensure network connectivity to blockchain nodes

### Slow Response Times
- Consider implementing caching for certain data types
- Use WebSockets for real-time updates instead of polling

## Development Roadmap

1. **Phase 1**: Basic dashboard showing agent status and market data
2. **Phase 2**: Real-time updates via WebSocket integration
3. **Phase 3**: User configuration panel for risk preferences and trading strategies
4. **Phase 4**: Transaction history and portfolio performance tracking

## Monitoring

Consider implementing a monitoring dashboard that tracks:
- Agent uptime and health
- Transaction success/failure rates
- API request volume and latency
- Trading strategy performance 