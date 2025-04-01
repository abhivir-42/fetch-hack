# AI Crypto Hedge Fund - Project Requirements Document (PRD)

## 1. Introduction

This document outlines the requirements for the **AI Crypto Hedge Fund**, an educational platform designed to have cryptocurrency trading strategies using a multi-agent system (MAS) built with Fetch.ai's uAgents framework.  The project builds upon the initial concepts of "CryptoFund" (detailed in `V1.md`).

## 2. Goals

*   **Crypto Trading:** Do cryptocurrency trading, including market data, sentiment analysis, and AI-driven decision-making.
*   **Educational Tool:** Serve as a learning platform for understanding AI agents, Fetch.ai technology, crypto market dynamics, and trading strategies.
*   **Showcase Fetch.ai:** Demonstrate the capabilities of Fetch.ai's uAgents and potentially Agentverse for building complex, decentralized applications.
*   **Realistic Environment:** Model key real-world trading factors like transaction fees, exchange slippage, and varying market conditions across different blockchains.
*   **Modularity and Extensibility:** Design the system with a layered, modular architecture to allow for easy extension with new agents, strategies, data sources, or features.
*   **User Interaction:** Provide an interactive web dashboard for monitoring the exchange, viewing results, and configuring parameters.

## 3. Target Audience

*   Developers interested in Fetch.ai, agent-based systems, and DeFi.
*   AI and cryptocurrency enthusiasts looking to experiment with trading strategies.

## 4. High-Level Architecture

The simulator will employ a multi-agent system architecture using Fetch.ai uAgents. Key agent roles (adapted and refined from `V1.md`) include:

*   **`SimulationManagerAgent`:** The central coordinator. Manages the simulation loop (time progression), overall state, configuration (user inputs like starting capital, risk profile), agent lifecycle, and coordination between other agents.
*   **`MarketDataAgent`:** Responsible for fetching and providing real-time and potentially historical market data (price, volume, etc.) for various cryptocurrencies and blockchains (initially ETH, BASE, POLY, BTC) from external APIs (e.g., CoinMarketCap, CoinGecko).
*   **`SentimentAgent`:** Fetches and interprets market sentiment indicators (e.g., Fear & Greed Index) from relevant sources.
*   **`NewsAgent`:** (Optional Layer) Fetches relevant cryptocurrency news headlines or summaries to provide context.
*   **`StrategyAgent(s)`:** Implements the core trading logic. Multiple instances with different strategies (rule-based, AI/LLM-based) can run concurrently. These agents receive data from MarketData, Sentiment, and potentially News agents to generate trading signals (Buy/Sell/Hold).
*   **`ExecutionSimulatorAgent`:** Receives trading signals from Strategy Agents and simulates their execution on target blockchains/DEXes. It calculates the outcome based on current market price, simulated slippage, and transaction fees, updating the portfolio state. 
*   **`PortfolioManagerAgent`:** Maintains the state of the simulated investment portfolio (asset balances, overall value, profit/loss). Updates based on simulated trades from the `ExecutionSimulatorAgent`.
*   **`DashboardAgent`:** Acts as a backend service (e.g., using Flask or FastAPI) to provide data from the simulation (portfolio status, market data, trade history, agent logs) to the web frontend.
*   **`BacktestingAgent`:** (Optional Layer) Manages the process of running simulations using historical market data to evaluate strategy performance over past periods.

## 5. Core Features

*   **Multi-Agent System (MAS):** Core architecture based on Fetch.ai uAgents communicating via messages.
*   **Market Data Integration:** Fetch data for major cryptocurrencies on Ethereum, Base, Polygon, and Bitcoin. Handle both real-time and historical data (for backtesting).
*   **Sentiment Analysis:** Integrate Fear & Greed Index or similar metrics.
*   **Configurable AI Trading Strategies:** Allow defining and running different trading strategies within `StrategyAgent` instances. Start with simple rule-based strategies and progress to LLM/AI-based ones.
<!-- *   **Simulated Trade Execution:** Model trade execution realistically, including:
    *   Configurable transaction fees (gas costs) based on target blockchain.
    *   Simulated slippage based on trade size and notional liquidity.
    *   Support for simulating trades on specific DEX protocols (e.g., Uniswap V3 logic) for relevant blockchains.
    *   Handling of Bitcoin simulation (e.g., simulating CEX trades as DEXes aren't typical). -->
*   **Blockchain Support:** Have activity across Ethereum, Base, Polygon, and Bitcoin.
*   **Interactive Web Dashboard:** A web UI (potentially using nextJS) to:
    *   Display current portfolio value and composition.
    *   Show real-time market data used by agents.
    *   List simulated trade history.
    *   Visualize performance metrics (e.g., P&L charts).
    *   Allow basic configuration (e.g., select strategies, set initial capital).
*   **Backtesting Framework:** Functionality to run simulations against historical data and evaluate strategy performance.
*   **User Configuration:** Allow users to set parameters like initial capital, risk tolerance (which strategies can use), and potentially select active strategies.

## 6. Non-Goals

*   **Full Decentralization:** While using decentralized agent tech, the initial focus is on a functional simulation, possibly running locally or on a single server. Agent discovery via Agentverse can be explored later.
*   **Becoming a Commercial Product:** This is primarily an educational and experimental project.

## 7. Technology Stack

*   **Backend & Agents:** Python, Fetch.ai uAgents
*   **AI/ML:** Potentially LLMs (like ASI), scikit-learn, TensorFlow/PyTorch (for more advanced strategies later).
*   **Web Framework (Dashboard Backend):** Flask or FastAPI
*   **Web Frontend:** A modern framework like Next or React
*   **Data Sources:** CoinMarketCap API, CoinGecko API, alternative free crypto data APIs, sentiment APIs.
*   **Database (Optional):** For storing historical data, backtesting results, simulation states (e.g., Supabase).
*   **Containerization (Optional):** Docker for easier deployment and dependency management.

## 8. Layered Implementation Plan

The project will be developed in incremental layers. Each layer results in a runnable, testable version of the simulator with added functionality.

*   **Layer 1: Foundation & Core Data Agents:**
    *   Set up project structure, dependencies (`requirements.txt`).
    *   Review V1 code (`docs/V1.md`) and adapt relevant parts.
    *   Implement basic `SimulationManagerAgent`, `MarketDataAgent`, `SentimentAgent`. Check their current implementation, most likely no change or minimal change would be needed. 
    *   Establish basic agent communication (uAgents protocol). I believe this should already have been happening with the agents that have been developed till now.
    *   Fetch and log real-time market and sentiment data.
    *   **Runnable State:** Agents start, fetch data periodically, and log it.
    *   Find a way to test the implementation as it goes ahead before even adding more agents. Maybe implementing something like a dashboard would be useful early on? 
*   **Layer 2: Basic Simulation Core & Portfolio:**
    *   Implement `PortfolioManagerAgent` to track simulated assets (e.g., starting with USD and ETH).
    *   Enhance `SimulationManagerAgent` to manage a simple simulation loop (discrete time steps).
    *   Establish data flow: Market data -> Simulation Manager -> (logged/stored).
    *   **Runnable State:** Simulation runs over time steps, portfolio state is maintained (though no trading happens yet).
*   **Layer 3: Simple Strategy & Simulated Execution:**
    *   Implement a basic `StrategyAgent` (e.g., rule-based like buy if FGI < 20, sell if FGI > 80).
    *   Implement `ExecutionSimulatorAgent` to handle buy/sell signals.
    *   Simulate trades: Update `PortfolioManagerAgent` based on signals, applying a *fixed* placeholder fee/slippage.
    *   Data flow: Data Agents -> Strategy Agent -> Execution Simulator -> Portfolio Manager.
    *   **Runnable State:** Simple strategy runs, generates signals, and simulated trades update the portfolio.
*   **Layer 4: Basic Web Dashboard:**
    *   Implement `DashboardAgent` (using Flask/FastAPI).
    *   Create a simple web UI (Next/React) to display:
        *   Current portfolio value and holdings (from `PortfolioManagerAgent`).
        *   Last fetched market/sentiment data.
        *   A list of simulated trades.
    *   **Runnable State:** Simulation runs, and its state can be viewed in a basic web interface.
*   **Layer 5: Realistic Simulation Parameters (Fees & Slippage):**
    *   Enhance `ExecutionSimulatorAgent` to model:
        *   Approximate gas fees based on blockchain (ETH, Base, Polygon).
        *   Simple slippage model (e.g., based on a percentage of trade size).
    *   Allow configuration of these parameters via `SimulationManagerAgent`.
    *   **Runnable State:** Simulation includes more realistic trading costs affecting portfolio performance.
*   **Layer 6: Multi-Asset & Multi-Blockchain:**
    *   Extend `MarketDataAgent` to fetch data for multiple assets (e.g., BTC, MATIC) on configured blockchains.
    *   Update `PortfolioManagerAgent` to handle multiple assets.
    *   Modify `ExecutionSimulatorAgent` to handle different fee structures/slippage assumptions per blockchain/asset pair.
    *   Adapt `StrategyAgent` to potentially handle multiple assets/pairs.
    *   Update Dashboard to display multi-asset portfolio.
    *   **Runnable State:** Simulation can trade multiple assets across supported blockchains.
*   **Layer 7: Basic Backtesting:**
    *   Modify `MarketDataAgent` to fetch or read historical data.
    *   Implement `BacktestingAgent` or add mode to `SimulationManagerAgent` to run simulation over a historical period.
    *   Store simulation results (portfolio value over time, trades).
    *   Update Dashboard to display backtesting results (e.g., final P&L, simple equity curve).
    *   **Runnable State:** Strategies can be tested on historical data.
*   **Layer 8: Enhanced Strategy & User Configuration:**
    *   Implement a more advanced `StrategyAgent` (e.g., using moving averages, RSI, or potentially the simple LLM from V1).
    *   Allow users to select which `StrategyAgent` to run via the `SimulationManagerAgent` (perhaps through a config file or simple dashboard input).
    *   Allow configuration of initial capital and basic risk parameters.
    *   **Runnable State:** Users can choose between different strategies and configure basic settings.
*   **Layer 9: Advanced Dashboard:**
    *   Improve the web UI (potentially migrate to React/Vue/Svelte).
    *   Add interactive charts (equity curve, price data).
    *   Display more detailed performance metrics (Sharpe ratio, max drawdown - calculated by `PortfolioManagerAgent` or `DashboardAgent`).
    *   Show agent logs/status.
    *   **Runnable State:** Simulation is monitored through a more professional and informative dashboard.
*   **Layer 10: Agent Collaboration & Refinement:**
    *   Explore more complex interactions, e.g., multiple `StrategyAgent` instances voting or specializing.
    *   Integrate `NewsAgent` data into strategies.
    *   Refine simulation models (fees, slippage).
    *   Explore Agentverse for dynamic agent discovery (e.g., finding specialized data providers or strategy agents if deployed).
    *   **Runnable State:** More sophisticated simulation with enhanced agent interactions and realism.

*(Future layers could include ML-based strategies, more DEX models, cross-chain simulation, enhanced backtesting options, etc.)*

## 9. Verification and Testing

*   **Unit Tests:** For individual agent logic, data processing functions, simulation calculations.
*   **Integration Tests:** Verify communication and data flow between agents.
*   **End-to-End Tests:** Simulate a full run and verify portfolio changes, dashboard output.
*   **Manual Testing:** Use the dashboard to monitor behavior and verify results match expectations.
*   **Code Reviews:** Ensure code quality, adherence to design principles.
*   **Layer Checkpoints:** After each layer, confirm the system is runnable and meets the layer's objectives before proceeding.

## 10. Open Questions / Future Considerations

*   Specific choices for external data APIs (considering free tiers, reliability).
*   Complexity of the slippage and fee models.
*   Scalability if running many agents or complex strategies.
*   Choice of frontend framework for the advanced dashboard.
*   Specific LLM/AI model integration details for Strategy Agents.
*   Deployment strategy (local, server, cloud). 