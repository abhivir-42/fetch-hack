# How to Run Layer 1: Foundation & Core Data Agents

This guide explains how to set up your environment and run the initial layer of the AI Crypto Hedge Fund Simulator.

## Prerequisites

*   **Python:** Ensure you have Python 3.9 or later installed.
*   **Git:** Ensure you have Git installed for cloning the repository (if you haven't already).
*   **CoinMarketCap API Key:** You need an API key from CoinMarketCap to fetch the Fear & Greed Index. You can get one from [https://coinmarketcap.com/api/](https://coinmarketcap.com/api/). The free plan should be sufficient for this project.

## Setup Steps

1.  **Clone the Repository (if needed):**
    If you haven't cloned the project repository yet, do so now:
    ```bash
    git clone <repository-url> # Replace with the actual URL
    cd fetch-hack # Or your project directory name
    ```

2.  **Create and Activate a Virtual Environment:**
    It's highly recommended to use a virtual environment to manage dependencies.
    ```bash
    # Navigate to the project root directory if you aren't already there
    cd /path/to/fetch-hack

    # Create the virtual environment (named 'venv')
    python3 -m venv venv

    # Activate the virtual environment
    # On macOS/Linux:
    source venv/bin/activate
    # On Windows (Command Prompt/PowerShell):
    # venv\Scripts\activate
    ```
    You should see `(venv)` at the beginning of your terminal prompt.

3.  **Install Dependencies:**
    Install all the required Python packages listed in `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables:**
    *   Locate the `.env.example` file in the project root.
    *   **Rename or copy** this file to `.env`.
    *   **Edit the `.env` file** and replace `"YOUR_API_KEY_HERE"` with your actual CoinMarketCap API key:
        ```dotenv
        # .env
        COINMARKETCAP_API_KEY="paste_your_real_api_key_here"

        # Agent addresses will be added automatically by run_layer1.py
        # MARKET_DATA_AGENT_ADDRESS="..."
        # SENTIMENT_AGENT_ADDRESS="..."
        ```
    *   Save the `.env` file. **Do not commit this file to Git** (it's included in `.gitignore`).

## Running the Agents (Layer 1)

Execute the `run_layer1.py` script from the project root directory:

```bash
python src/run_layer1.py
```

## Expected Output and Behavior

When you run the script, you should see log messages in your terminal indicating:

1.  **Script Start:** `--- Starting Layer 1 ---`
2.  **Agent Initialization:** Messages indicating `MarketDataAgent`, `SentimentAgent`, and `SimulationManagerAgent` are being added to the Bureau, along with their seeds.
3.  **.env Update:** Messages showing that `MARKET_DATA_AGENT_ADDRESS` and `SENTIMENT_AGENT_ADDRESS` are being set in your `.env` file.
4.  **Bureau Start:** `Starting bureau...`
5.  **Agent Startups:** Messages from each agent confirming it has started and listing its address and endpoint (e.g., `📈 SentimentAgent started: agent1...`, `💹 MarketDataAgent started: agent1...`, `🚀 SimulationManagerAgent started: agent1...`).
6.  **Periodic Fetch (Simulation Manager):** Every 60 seconds (as configured in `simulation_manager_agent.py`), you will see logs like:
    *   `Initiating periodic data fetch...`
    *   `Sending MarketDataRequest for ['bitcoin', 'ethereum'] to agent1...`
    *   `Sending FGIRequest to agent1...`
7.  **Data Agent Requests (Market/Sentiment Agents):** Corresponding logs from the data agents showing they received requests:
    *   `Received MarketDataRequest from agent1...`
    *   `Received FGI request from agent1...`
8.  **Data Agent Responses (Market/Sentiment Agents):** Logs showing they are sending data back:
    *   `Sending market data for 2 coin(s)`
    *   `Sending FGI data: Value=..., Class='...'`
9.  **Data Received (Simulation Manager):** Logs confirming the Simulation Manager received the data:
    *   `Received MarketDataResponse from agent1...` followed by formatted coin data.
    *   `Received FGIResponse from agent1...` followed by formatted FGI data.

**Example Log Snippet:**

```
INFO:__main__:--- Starting Layer 1 --- 
INFO:__main__:Adding agents to bureau...
INFO:__main__:- Adding SimulationManagerAgent (Seed: sim_manager_agent_default_seed)
INFO:__main__:- Adding MarketDataAgent (Seed: market_data_agent_default_seed)
INFO:__main__:- Adding SentimentAgent (Seed: sentiment_agent_default_seed)
INFO:__main__:Updating agent addresses in: /Users/abhivir42/projects/fetch-hack/.env
INFO:__main__:MARKET_DATA_AGENT_ADDRESS set to agent1q...
INFO:__main__:SENTIMENT_AGENT_ADDRESS set to agent1q...
INFO:__main__:Starting bureau...
INFO:src.market_data_agent:💹 MarketDataAgent started: agent1q...
INFO:src.market_data_agent:Endpoint: http://127.0.0.1:8002/submit
INFO:src.sentiment_agent:📈 SentimentAgent started: agent1q...
INFO:src.sentiment_agent:Endpoint: http://127.0.0.1:8001/submit
INFO:src.simulation_manager_agent:🚀 SimulationManagerAgent started: agent1q...
INFO:src.simulation_manager_agent:Endpoint: http://127.0.0.1:8000/submit
INFO:src.simulation_manager_agent:Market Data Agent Address: agent1q...
INFO:src.simulation_manager_agent:Sentiment Agent Address: agent1q...
# ... after 60 seconds ...
INFO:src.simulation_manager_agent:--------------------------------------------------
INFO:src.simulation_manager_agent:Initiating periodic data fetch (Interval: 60.0s)
INFO:src.simulation_manager_agent:Sending MarketDataRequest for ['bitcoin', 'ethereum'] to agent1q...
INFO:src.simulation_manager_agent:Sending FGIRequest to agent1q...
INFO:src.market_data_agent:Received MarketDataRequest from agent1q... for coins: ['bitcoin', 'ethereum']
INFO:src.sentiment_agent:Received FGI request from agent1q...
INFO:src.market_data_agent:Sending market data for 2 coin(s)
INFO:src.sentiment_agent:Sending FGI data: Value=..., Class='...'
INFO:src.simulation_manager_agent:Received MarketDataResponse from agent1q...:
INFO:src.simulation_manager_agent:  - Bitcoin (BTC): Price=..., MCap=..., Vol=..., 24h%=...%
INFO:src.simulation_manager_agent:  - Ethereum (ETH): Price=..., MCap=..., Vol=..., 24h%=...%
INFO:src.simulation_manager_agent:Received FGIResponse from agent1q...:
INFO:src.simulation_manager_agent:  - FGI Value: ..., Classification: '...', Timestamp: ...
# ... continues every 60 seconds ...
```

## Stopping the Agents

Press `Ctrl+C` in the terminal where the script is running. This will initiate a graceful shutdown of the agents and the Bureau.
You should see log messages indicating the Bureau is stopping.

## Troubleshooting

*   **`ModuleNotFoundError`:** Ensure your virtual environment is active and you ran `pip install -r requirements.txt`.
*   **API Key Error:** Double-check that your `COINMARKETCAP_API_KEY` in the `.env` file is correct and doesn't have extra quotes or spaces. Ensure the `.env` file is in the project root directory.
*   **Address Errors:** If the Simulation Manager logs warnings about agent addresses not being configured, ensure the `run_layer1.py` script ran correctly and updated the `.env` file. Check the `.env` file for `MARKET_DATA_AGENT_ADDRESS` and `SENTIMENT_AGENT_ADDRESS`.
*   **Connection Errors:** Ensure no other application is using ports 8000, 8001, or 8002 on your machine. If necessary, you can change the default ports by setting environment variables (`SIM_AGENT_PORT`, `MARKET_AGENT_PORT`, `SENTIMENT_AGENT_PORT`) in your `.env` file *before* running `run_layer1.py` for the first time.
*   **API Request Failed:** Check your internet connection. Verify the CoinMarketCap or CoinGecko APIs are operational. Check for specific error messages logged by the agents (e.g., rate limits, invalid key). 