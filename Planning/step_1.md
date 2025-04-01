# Step 1 Plan: Foundation & Core Data Agents

## Objective

Establish the foundational project structure, review and potentially adapt existing code from V1 for a simulation context, implement the core data-gathering agents (`MarketDataAgent`, `SentimentAgent`), and a basic `SimulationManagerAgent` to coordinate them. Ensure these agents can start, communicate minimally, fetch data from external APIs, and log this data. The system should be runnable and testable at the end of this step.

## Tasks

1.  **Project Structure Setup:**
    *   Ensure a logical directory structure exists (e.g., `src/` for agent code, `docs/`, `Planning/`, `tests/`, potentially `data/` for logs/configs).
    *   Create/update `requirements.txt` with necessary initial dependencies (e.g., `fetch-ai-uagents`, `requests`, potentially `python-dotenv`).
    *   Create a basic `.gitignore` file.
    *   Create a simple `README.md` explaining the project setup and how to run the Layer 1 implementation.

2.  **Review & Adapt V1 Code:**
    *   **`main.py`:** Analyze its role as the central coordinator. Adapt it to become the basis for `SimulationManagerAgent`. Remove direct user input prompts for runtime configuration (this will move to config files or dashboard later). Focus on agent startup and basic interval-based triggering.
    *   **`coininfo_agent.py`:** This aligns well with the `MarketDataAgent` role. Review its API integration (CoinMarketCap). Ensure it can fetch price, volume, etc., for specified coins (initially ETH, BTC) and respond to requests. Adapt message models if necessary (`CoinRequest`, `CoinResponse`).
    *   **`fgi_agent.py`:** This maps directly to the `SentimentAgent`. Review its API integration (CoinMarketCap FGI). Ensure it fetches the index and potentially its classification. Adapt message models if needed.
    *   **Other V1 Agents:** Note the functionality of `cryptonews_agent.py`, `asi1_test.py`, `swapfinder_agent.py`, `dashboard_agent.py`, etc., but *defer their implementation or adaptation* to later layers as specified in the PRD. The goal of Layer 1 is *only* the foundation and data agents.
    *   **Configuration:** Identify any hardcoded API keys or endpoints. Plan to move these to environment variables (`.env` file) or a configuration file.

3.  **Implement `SimulationManagerAgent` (`src/simulation_manager_agent.py`):**
    *   Create a new uAgent.
    *   Initialize instances of `MarketDataAgent` and `SentimentAgent` (or get their addresses if running separately).
    *   Implement a basic interval loop (e.g., every 60 seconds).
    *   On each interval:
        *   Send a request to `MarketDataAgent` for data (e.g., ETH, BTC prices).
        *   Send a request to `SentimentAgent` for the FGI.
    *   Implement handlers to receive responses from the data agents.
    *   Log the received data (using basic `print` or Python `logging` module) to demonstrate functionality.

4.  **Implement/Refine `MarketDataAgent` (`src/market_data_agent.py`):**
    *   Adapt `coininfo_agent.py`.
    *   Ensure it uses an API key from environment variables/config.
    *   Define clear message models for requests (specifying coins/blockchains) and responses (containing the data).
    *   Implement the handler for requests from `SimulationManagerAgent`.
    *   Fetch data for at least ETH and BTC.
    *   Handle potential API errors gracefully (e.g., log errors, return default/error state).

5.  **Implement/Refine `SentimentAgent` (`src/sentiment_agent.py`):**
    *   Adapt `fgi_agent.py`.
    *   Ensure it uses necessary API keys/endpoints from environment variables/config.
    *   Define message models for requests and responses.
    *   Implement the handler for requests from `SimulationManagerAgent`.
    *   Handle potential API errors gracefully.

6.  **Basic Agent Communication:**
    *   Utilize `uagent.send()` for requests and message handlers (`@agent.on_message`) for responses.
    *   Ensure agent addresses are correctly configured/retrieved for communication (initially, can run all in one script or use fixed addresses for simplicity).

7.  **Testing and Verification:**
    *   **Manual Run:** Create a simple run script (e.g., `run_layer1.py`) that initializes and runs the `SimulationManagerAgent` (which in turn might start or connect to the other agents).
    *   **Check Logs:** Verify that the `SimulationManagerAgent` successfully requests data and logs the responses from `MarketDataAgent` and `SentimentAgent` periodically.
    *   **API Calls:** Monitor (if possible) or infer that the data agents are making successful calls to external APIs.
    *   **Error Handling:** Test scenarios like invalid API keys or network issues (if feasible) to ensure agents log errors appropriately.

## Technologies

*   Python 3.x
*   `fetch-ai-uagents`
*   `requests` (for API calls)
*   `python-dotenv` (for environment variables)
*   CoinMarketCap API (or alternative like CoinGecko) - Requires API Key.

## Deliverables

*   Updated project structure.
*   `requirements.txt`, `.gitignore`, `README.md`.
*   `.env.example` file showing needed environment variables (API keys).
*   Implemented/adapted Python files for:
    *   `src/simulation_manager_agent.py`
    *   `src/market_data_agent.py`
    *   `src/sentiment_agent.py`
    *   `src/models.py` (if using shared Pydantic models for messages)
*   A script (`run_layer1.py`) to start the Layer 1 agents.
*   **Runnable State:** Agents start, communicate, fetch market/sentiment data periodically, and log the results. 