import os
import logging
import requests
from typing import Dict, List
from dotenv import load_dotenv
from uagents import Agent, Context
from src.models import MarketDataRequest, MarketDataResponse, CoinData, ErrorResponse

# Load environment variables
load_dotenv()

# Configure Logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Define agent constants
MARKET_AGENT_SEED = os.getenv("MARKET_AGENT_SEED", "market_data_agent_default_seed")
MARKET_AGENT_PORT = int(os.getenv("MARKET_AGENT_PORT", 8002))
MARKET_AGENT_ENDPOINT = os.getenv("MARKET_AGENT_ENDPOINT", f"http://127.0.0.1:{MARKET_AGENT_PORT}/submit")

# Initialize Agent
market_data_agent = Agent(
    name="MarketDataAgent",
    port=MARKET_AGENT_PORT,
    seed=MARKET_AGENT_SEED,
    endpoint=[MARKET_AGENT_ENDPOINT],
)

def get_market_data(coin_ids: List[str], vs_currency: str = 'usd') -> MarketDataResponse:
    """Fetch market data for specified cryptocurrencies from CoinGecko API."""
    if not coin_ids:
        return MarketDataResponse(success=False, error="No coin IDs provided.")

    # API Endpoint: https://www.coingecko.com/en/api/documentation
    # Using /coins/markets endpoint
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': vs_currency,
        'ids': ",".join(coin_ids), # Comma-separated list of coin IDs
        'order': 'market_cap_desc',
        'per_page': len(coin_ids), # Limit results to requested coins
        'page': 1,
        'sparkline': 'false' # We don't need sparkline data
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status() # Raises error for non-200 status codes

        raw_data = response.json()
        #logger.debug(f"CoinGecko Raw Response: {raw_data}")

        if not isinstance(raw_data, list):
            logger.error(f"Unexpected API response format: {raw_data}")
            return MarketDataResponse(success=False, error="Unexpected API response format")

        processed_data: Dict[str, CoinData] = {}
        for coin_raw in raw_data:
            if coin_raw and isinstance(coin_raw, dict) and 'id' in coin_raw:
                coin_id = coin_raw['id']
                processed_data[coin_id] = CoinData(
                    id=coin_id,
                    symbol=coin_raw.get('symbol', 'n/a').upper(),
                    name=coin_raw.get('name', 'Unknown'),
                    current_price=coin_raw.get('current_price'),
                    market_cap=coin_raw.get('market_cap'),
                    total_volume=coin_raw.get('total_volume'),
                    price_change_percentage_24h=coin_raw.get('price_change_percentage_24h')
                )
            else:
                logger.warning(f"Skipping invalid entry in API response: {coin_raw}")

        # Check if all requested coins were found
        if len(processed_data) != len(coin_ids):
            logger.warning(f"Could not find data for all requested coin IDs. Found: {list(processed_data.keys())}")
            # Decide if this should be an error or partial success
            # For now, return what was found

        if not processed_data:
             return MarketDataResponse(success=False, error="No data found for requested coin IDs")

        return MarketDataResponse(success=True, data=processed_data)

    except requests.exceptions.RequestException as e:
        logger.error(f"⚠️ CoinGecko API Request Failed: {e}")
        return MarketDataResponse(success=False, error=str(e))
    except Exception as e:
        logger.error(f"🔥 Unexpected error processing market data: {e}")
        return MarketDataResponse(success=False, error=f"Unexpected processing error: {str(e)}")

@market_data_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"💹 MarketDataAgent started: {ctx.address}")
    ctx.logger.info(f"Endpoint: {MARKET_AGENT_ENDPOINT}")

@market_data_agent.on_message(model=MarketDataRequest)
async def handle_market_data_request(ctx: Context, sender: str, msg: MarketDataRequest):
    ctx.logger.info(f"Received MarketDataRequest from {sender} for coins: {msg.coin_ids}")
    response = get_market_data(msg.coin_ids)

    if response.success:
        num_coins = len(response.data) if response.data else 0
        ctx.logger.info(f"Sending market data for {num_coins} coin(s)")
        await ctx.send(sender, response)
    else:
        ctx.logger.error(f"Failed to fetch market data: {response.error}")
        # Send an error response back
        await ctx.send(sender, ErrorResponse(error=f"Failed to fetch market data: {response.error}"))

# Note: No __main__ block here, will be run from run_layer1.py 