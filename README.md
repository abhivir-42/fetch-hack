# CryptoFund

A decentralized autonomous crypto trading assistant built using FetchAI's agent framework and uAgents. The system leverages multiple specialized AI agents that collaborate to analyze market data, sentiment indicators, and financial data to make informed cryptocurrency trading decisions.

## Features

- Multi-agent architecture for specialized tasks
- Real-time market data analysis from CoinGecko
- Crypto news sentiment analysis
- Fear & Greed Index monitoring
- Heart rate-based emotional trading safeguards
- Automated swap execution on Base network
- Dynamic agent discovery and coordination
- REST API for external integrations

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
6. **API Server**:
   - REST API for external system integration

## Setup

### Prerequisites

- Python 3.10+
- API keys for ASI1, CoinMarketCap, and other services
- MetaMask wallet with private key for transactions

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/cryptofund.git
   cd cryptofund
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root with your API keys:
   ```
   ASI1_API_KEY=your_asi1_api_key
   CMC_API_KEY=your_coinmarketcap_api_key
   NEWS_API_KEY=your_news_api_key
   METAMASK_PRIVATE_KEY=your_metamask_private_key
   AGENTVERSE_API_KEY=your_agentverse_api_key
   ```

## Usage

### Starting the System

1. Start the API server:
   ```
   python cryptoreason/api_server.py
   ```

2. Start the main agent:
   ```
   python cryptoreason/main_agent.py
   ```

3. Start the required agents:
   ```
   python cryptoreason/asi/llm_agent.py
   python cryptoreason/swapland/swapfinder.py
   ```

### API Endpoints

The system exposes several REST API endpoints:

- `GET /api/health`: System health check
- `GET /api/agents`: List all registered agents
- `GET /api/market-data`: Get latest market data
- `GET /api/transactions`: Get transaction history
- `GET /api/heartbeat`: Get heartbeat data
- `POST /api/trigger-analysis`: Trigger market analysis
- `POST /api/update-heartbeat`: Update heartbeat data

### Configuration

The system can be configured by modifying the following files:

- `cryptoreason/common/config.py`: Global configuration settings
- `cryptoreason/data/agent_registry.json`: Agent registry configuration

## Architecture Improvements

The codebase has been refactored with the following improvements:

1. **Error Handling and Resilience**:
   - Implemented centralized error handling
   - Added retry mechanisms for API calls and agent communications
   - Added timeouts for all external API calls

2. **Asynchronous Processing**:
   - Implemented event-based synchronization
   - Added back-pressure handling
   - Created state machine for complex workflows

3. **Code Organization**:
   - Moved message models to shared modules
   - Created centralized configuration system
   - Standardized logging formats

4. **Agent Registration and Discovery**:
   - Implemented dynamic agent discovery
   - Created service registry

5. **Security Enhancements**:
   - Removed hardcoded secrets
   - Implemented proper credential management
   - Added input validation

6. **Modularity Improvements**:
   - Refactored large files into smaller, focused modules
   - Created common base agent class
   - Implemented dependency injection

7. **Redundancy Elimination**:
   - Consolidated similar swap execution agents using factory pattern
   - Removed duplicated code

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- FetchAI for the agent framework
- ASI1 for the decision-making engine
- CoinGecko and CoinMarketCap for market data