# CryptoFund Codebase Architecture

## Overview

CryptoFund is a decentralized autonomous crypto trading assistant built using FetchAI's agent framework and uAgents. The system leverages multiple specialized AI agents that collaborate to analyze market data, sentiment indicators, and financial data to make informed cryptocurrency trading decisions.

The architecture follows a multi-agent paradigm where specialized agents communicate via standardized messages to collect data, analyze market conditions, and execute trades on various blockchain networks.

## System Architecture

The system consists of the following main components:

1. **Main Agent**: Central coordinator that manages communication between all agents
2. **Data Collection Agents**: Retrieve market data, news, and sentiment indicators
   - CoinInfo Agent
   - CryptoNews Agent
   - FGI (Fear & Greed Index) Agent
3. **Decision Making Layer**:
   - Reason Agent (ASI1): AI-based decision engine
4. **Transaction Layer**:
   - SwapFinder Agent: Discovers and coordinates with swap execution agents
   - Swap Execution Agents: Execute trades on specific networks and token pairs
   - Topup Agent: Manages wallet funding
   - Reward Agent: Handles payment processing and rewards distribution
5. **User Interaction**:
   - Heartbeat Agent: Monitors user's emotional state via heart rate data

## Directory Structure

```
/
├── cryptoreason/           # Main codebase directory
│   ├── main.py             # Main orchestration agent
│   ├── coininfo_agent.py   # Market data retrieval agent
│   ├── cryptonews_agent.py # Crypto news retrieval agent
│   ├── fgi_agent.py        # Fear & Greed Index agent
│   ├── heartbeat_agent.py  # User heart rate monitoring agent
│   ├── topup_agent.py      # Wallet funding agent
│   ├── reward_agent.py     # Payment processing agent
│   ├── swapland/           # Swap execution components
│   │   ├── swapfinder_agent.py  # Agent discovery and coordination
│   │   ├── base_ethTOusdc.py    # ETH to USDC swap on Base network
│   │   ├── base_usdcTOeth.py    # USDC to ETH swap on Base network
│   │   └── llm_swapfinder.py    # LLM helper for agent discovery
│   └── asi/               # AI reasoning components
│       └── llm_agent.py   # ASI1 integration for decision making
├── migrate/               # Migration utilities
├── data/                  # Data storage
├── docs/                  # Documentation
└── requirements.txt       # Project dependencies
```

## Key Components

### Main Agent (`main.py`)

The main agent serves as the central orchestrator for the entire system. It:

- Initializes and coordinates all other agents
- Manages the data collection process from various sources
- Forwards collected data to the reasoning layer
- Interprets trading decisions and initiates swap executions
- Handles transaction verification and reward distribution

This agent maintains the overall state of the system and orchestrates the workflow between data collection, analysis, and execution.

### Data Collection Agents

#### CoinInfo Agent (`coininfo_agent.py`)

- Retrieves cryptocurrency market data from CoinGecko API
- Provides current prices, market cap, volume, and 24h price changes
- Supports multiple blockchains (Ethereum, Base, Polygon, Bitcoin)
- Communicates data back to the main agent via standardized message models

#### CryptoNews Agent (`cryptonews_agent.py`)

- Fetches latest news related to cryptocurrencies
- Provides market context and sentiment indicators
- Returns news summaries to the main agent

#### FGI Agent (`fgi_agent.py`)

- Connects to CoinMarketCap API to fetch Fear & Greed Index data
- Provides market sentiment classification
- Returns sentiment data with timestamp and classification (e.g., "Extreme Fear", "Neutral", "Greed")

### Decision Making Layer

#### Reason Agent (`asi/llm_agent.py`)

- Integrates with ASI1-Mini LLM for decision making
- Analyzes collected market data, news, and sentiment indicators
- Generates trading recommendations (buy/sell signals)
- Considers user's investment style and risk tolerance
- Communicates decisions back to the main agent

### Transaction Layer

#### SwapFinder Agent (`swapland/swapfinder_agent.py`)

- Searches for appropriate swap agents in the Agentverse ecosystem
- Uses LLM to determine the most suitable agent for specific token swaps
- Coordinates with swap execution agents to perform trades
- Communicates transaction status back to the main agent

#### Swap Execution Agents

Specialized agents for specific blockchain networks and token pairs:

- **Base ETH to USDC** (`base_ethTOusdc.py`): Executes ETH to USDC swaps on the Base network
- **Base USDC to ETH** (`base_usdcTOeth.py`): Executes USDC to ETH swaps on the Base network

These agents utilize Uniswap V3 smart contracts to execute trades and report back transaction status.

#### Topup Agent (`topup_agent.py`)

- Manages wallet funding for transaction execution
- Handles FET token transfers for agent operations
- Provides balance management functions

#### Reward Agent (`reward_agent.py`)

- Processes payments for services rendered
- Manages reward distribution
- Verifies transaction completion

### User Interaction

#### Heartbeat Agent (`heartbeat_agent.py`)

- Monitors user's emotional state via heart rate data
- Analyzes heart rate patterns to detect potential emotional trading decisions
- Can pause trading activity if user's heart rate exceeds thresholds
- Acts as a safeguard against impulsive trading during high-stress periods

## Communication Flow

The system uses a standardized message-based communication protocol powered by FetchAI's uAgents framework:

1. The main agent initializes and registers all component agents
2. At regular intervals or user request, the main agent initiates data collection
3. Data collection agents retrieve and return their specialized data
4. The main agent aggregates data and forwards it to the reasoning layer
5. The reasoning agent analyzes the data and returns a decision
6. If a trade is recommended, the main agent initiates the transaction process
7. The SwapFinder agent discovers appropriate swap execution agents
8. Swap execution agents perform the actual blockchain transactions
9. Transaction status is reported back to the main agent
10. The reward agent processes payments for completed transactions

## Agent Communication Models

Agents communicate using standardized data models:

```python
# Example message models
class CoinRequest(Model):
    blockchain: str

class CoinResponse(Model):
    name: str
    symbol: str
    current_price: float
    market_cap: float
    total_volume: float
    price_change_24h: float

class ASI1Request(Model):
    query: str
    
class ASI1Response(Model):
    decision: str

class SwaplandRequest(Model):
    blockchain: str
    signal: str
    amount: float
    private_key: str
```

## Asynchronous Processing

The system heavily leverages asynchronous processing throughout:

- All agent event handlers use Python's `async/await` pattern
- Message handling is non-blocking and event-driven
- Flask web servers handle webhook-based communication for Agentverse-based agents
- Long-running operations are managed via thread-based execution

## User Input Handling

User inputs are primarily processed through:

1. **Direct console interaction**: Some components accept direct user input during initialization
2. **Heartbeat monitoring**: User's emotional state is continuously monitored
3. **Initial configuration**: User sets preferences like blockchain network and risk tolerance

## Security Considerations

The system implements several security measures:

- Private keys for blockchain transactions are stored in environment variables
- The heartbeat agent provides a safety mechanism to prevent emotional trading
- Reward distribution is verified through transaction confirmation
- API keys for external services are secured via environment variables

## Agent Registration and Discovery

Agents register with the Agentverse platform, which provides:

- Agent discovery via search functionality
- Standardized communication channels
- Registration with unique agent identifiers
- Agent readme documentation with capabilities

## Technical Implementation

### Technologies Used

- **FetchAI's uAgents Framework**: For agent-based architecture and communication
- **ASI1 Mini LLM**: For decision-making and reasoning
- **Flask**: For web-based endpoints and communication
- **UniswapV3**: For performing token swaps on Ethereum and Base networks
- **CoinGecko/CoinMarketCap APIs**: For market data and sentiment metrics
- **Agentverse**: For agent discovery and registration
- **Web3.py**: For blockchain interaction

### Dependencies

Main Python dependencies include:
- uagents
- fetchai
- web3
- flask
- requests
- cosmpy
- dotenv

## Conclusion

The CryptoFund architecture demonstrates a sophisticated multi-agent system that leverages AI, blockchain, and agent-based communication to create an autonomous trading assistant. The system's modular design allows for easy extension with new capabilities, blockchain networks, and trading strategies while maintaining a clean separation of concerns between data collection, analysis, and execution components. 