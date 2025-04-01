import os
import logging
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv
from uagents import Agent, Context
from src.models import FGIRequest, FGIResponse, FearGreedData, ErrorResponse

# Load environment variables
load_dotenv()

# Configure Logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Ensure API key is loaded
CMC_API_KEY = os.getenv("COINMARKETCAP_API_KEY")
if not CMC_API_KEY:
    logger.error("❌ COINMARKETCAP_API_KEY is not set in the .env file.")
    # Depending on the desired behavior, you might exit or let the agent fail on request
    # sys.exit(1)

# Define agent constants
SENTIMENT_AGENT_SEED = os.getenv("SENTIMENT_AGENT_SEED", "sentiment_agent_default_seed")
SENTIMENT_AGENT_PORT = int(os.getenv("SENTIMENT_AGENT_PORT", 8001))
SENTIMENT_AGENT_ENDPOINT = os.getenv("SENTIMENT_AGENT_ENDPOINT", f"http://127.0.0.1:{SENTIMENT_AGENT_PORT}/submit")

# Initialize Agent
sentiment_agent = Agent(
    name="SentimentAgent",
    port=SENTIMENT_AGENT_PORT,
    seed=SENTIMENT_AGENT_SEED,
    endpoint=[SENTIMENT_AGENT_ENDPOINT],
)

def get_fear_and_greed_index() -> FGIResponse:
    """Fetch the latest Fear and Greed index data from CoinMarketCap API."""
    if not CMC_API_KEY:
        return FGIResponse(success=False, error="API key not configured.")

    # Note: CMC API for FGI might return historical data by default.
    # We request limit=1 to get the most recent entry.
    url = "https://pro-api.coinmarketcap.com/v3/fear-and-greed/historical"
    headers = {"X-CMC_PRO_API_KEY": CMC_API_KEY}
    params = {"limit": 1} # Get the latest entry

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status() # Raises error for non-200 status codes

        raw_data = response.json()
        #logger.debug(f"CMC Raw Response: {raw_data}")

        if raw_data.get("status", {}).get("error_code", 0) != 0:
            error_message = raw_data.get("status", {}).get("error_message", "Unknown API error")
            logger.error(f"API Error: {error_message}")
            return FGIResponse(success=False, error=error_message)

        if not raw_data.get("data"):
            logger.warning("No data found in FGI API response.")
            return FGIResponse(success=False, error="No data returned from API")

        # Assuming the first entry in the data list is the latest
        latest_entry = raw_data["data"][0]
        fgi_data = FearGreedData(
            value=latest_entry["value"],
            value_classification=latest_entry["value_classification"],
            timestamp=latest_entry["timestamp"]
        )

        return FGIResponse(success=True, data=fgi_data)

    except requests.exceptions.RequestException as e:
        logger.error(f"⚠️ API Request Failed: {e}")
        return FGIResponse(success=False, error=str(e))
    except Exception as e:
        logger.error(f"🔥 Unexpected error processing FGI data: {e}")
        return FGIResponse(success=False, error=f"Unexpected processing error: {str(e)}")

@sentiment_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"📈 SentimentAgent started: {ctx.address}")
    ctx.logger.info(f"Endpoint: {SENTIMENT_AGENT_ENDPOINT}")

@sentiment_agent.on_message(model=FGIRequest)
async def handle_fgi_request(ctx: Context, sender: str, _msg: FGIRequest):
    ctx.logger.info(f"Received FGI request from {sender}")
    response = get_fear_and_greed_index()

    if response.success:
        ctx.logger.info(f"Sending FGI data: Value={response.data.value}, Class='{response.data.value_classification}'")
        await ctx.send(sender, response)
    else:
        ctx.logger.error(f"Failed to fetch FGI data: {response.error}")
        # Send an error response back to the requester
        await ctx.send(sender, ErrorResponse(error=f"Failed to fetch FGI data: {response.error}"))

# Note: No __main__ block here, will be run from run_layer1.py 