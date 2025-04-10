# API Wrapper Testing Guide

This guide explains how to test the API wrapper that interfaces with the CryptoReason agent system.

## Prerequisites

1. Make sure all agents are running (ideally using the `start_all_agents.py` script)
2. The API wrapper is running on port 5000 (`python3 api_wrapper.py`)

## Testing API Endpoints

You can test the API endpoints using `curl` commands or any API testing tool like Postman. Here are examples using `curl`:

### 1. Check Agent Status

```bash
curl http://localhost:5000/api/status
```

Expected response (example):
```json
{
  "main_agent": true,
  "heartbeat_agent": true,
  "coin_info_agent": true,
  "fgi_agent": true,
  "crypto_news_agent": true,
  "llm_agent": true,
  "reward_agent": true,
  "topup_agent": true,
  "swapfinder_agent": true,
  "swap_eth_to_usdc": true
}
```

### 2. Get Market Data

```bash
curl http://localhost:5000/api/market-data
```

Expected response:
```json
{
  "name": "Ethereum",
  "symbol": "ETH",
  "current_price": 1510.25,
  "market_cap": 182648195370.0,
  "total_volume": 21218775926.0,
  "price_change_24h": -2.2367
}
```

### 3. Get Sentiment Analysis

```bash
curl http://localhost:5000/api/sentiment-analysis
```

Expected response:
```json
{
  "data": [
    {
      "value": 17.0,
      "value_classification": "Extreme Fear",
      "timestamp": "1743984000"
    }
  ],
  "status": "success",
  "timestamp": "2025-04-08T16:39:53.288995+00:00"
}
```

### 4. Get Crypto News

```bash
curl http://localhost:5000/api/news
```

Expected response (shortened):
```json
{
  "articles": [
    {
      "source": {"id": null, "name": "Forbes"},
      "author": "Ty Roush, Forbes Staff",
      "title": "Bitcoin Falls Below $77,000 As Trump's Tariffs Erase Election Boost",
      "description": "Several cryptocurrencies have lost nearly all their gains since Trump's election win in November.",
      "url": "https://www.forbes.com/sites/tylerroush/2025/04/07/bitcoin-falls-below-77000-as-trumps-tariffs-erase-election-boost/",
      "urlToImage": "https://imageio.forbes.com/specials-images/imageserve/67d3822876162cb2c2d8/0x0.jpg?format=jpg&crop=3393,1908,x0,y318,safe&height=900&width=1600&fit=bounds",
      "publishedAt": "2025-04-07T13:05:32Z",
      "content": "President Donald Trump's far-reaching reciprocal tariffs appear to be impacting cryptocurrency prices..."
    }
  ]
}
```

### 5. Get Transaction History

```bash
curl http://localhost:5000/api/transactions
```

Expected response (when no transactions are available):
```json
[]
```

### 6. Execute a Trade

```bash
curl -X POST http://localhost:5000/api/execute-trade \
  -H "Content-Type: application/json" \
  -d '{"action":"SELL", "amount":0.1}'
```

Expected response:
```json
{
  "status": "pending",
  "message": "Trade SELL for 0.1 submitted",
  "timestamp": 1712748123.456789
}
```

### 7. Start a Specific Agent

If an agent has stopped or wasn't started:

```bash
curl -X POST http://localhost:5000/api/start-agent \
  -H "Content-Type: application/json" \
  -d '{"agent":"fgi"}'
```

Expected response:
```json
{
  "status": "success",
  "message": "Agent fgi started"
}
```

### 8. Start All Agents

To start all agents in the correct order:

```bash
curl -X POST http://localhost:5000/api/start-all
```

Expected response:
```json
{
  "status": "success",
  "message": "All agents started"
}
```

## Integration in Frontend

When integrating with a frontend application, you would typically:

1. Make AJAX or fetch calls to these endpoints
2. Poll the `/api/status` endpoint periodically to monitor agent health
3. Use WebSockets for real-time updates if needed
4. Implement a caching layer on the frontend to minimize API calls

Example fetch request in JavaScript:

```javascript
// Get market data
fetch('http://localhost:5000/api/market-data')
  .then(response => response.json())
  .then(data => {
    console.log(data);
    // Update UI with market data
  })
  .catch(error => console.error('Error fetching market data:', error));

// Execute a trade
fetch('http://localhost:5000/api/execute-trade', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    action: 'SELL',
    amount: 0.1
  })
})
.then(response => response.json())
.then(data => {
  console.log(data);
  // Update UI with trade status
})
.catch(error => console.error('Error executing trade:', error));
```

## Troubleshooting

If you encounter issues:

1. **Endpoint returns an error**: Check the terminal where the API wrapper is running for error logs
2. **Data looks incorrect**: Verify the corresponding agent is running using the `/api/status` endpoint
3. **Connection refused**: Ensure the API wrapper is running and listening on port 5000
4. **CORS issues**: If testing from a web application, ensure CORS is properly configured in the API wrapper 