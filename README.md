# AI Crypto Hedge Fund Simulator

This project is an educational simulator for cryptocurrency trading using AI agents built with the Fetch.ai uAgents framework.

See `docs/prd.md` for the full project requirements and plan.

## Current Status

Layer 1: Foundation & Core Data Agents (In Progress)

## Setup (Layer 1)

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd fetch-hack
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    *   Rename `.env.example` to `.env`.
    *   Add your CoinMarketCap API key to the `.env` file.
    ```
    COINMARKETCAP_API_KEY="YOUR_API_KEY_HERE"
    ```

## Running Layer 1

```bash
python src/run_layer1.py
```

This will start the `SimulationManagerAgent`, `MarketDataAgent`, and `SentimentAgent`. The `SimulationManagerAgent` will periodically request data from the other two agents and log the results to the console.