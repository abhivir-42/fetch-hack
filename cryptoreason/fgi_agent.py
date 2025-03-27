import os
import logging
import sys
import requests
from datetime import datetime, timezone
from typing import Optional
from uagents import Agent, Context, Model
import atexit

# Configure Logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Log on exit
def log_and_exit():
    logging.debug("🚨 Script terminated unexpectedly")
atexit.register(log_and_exit)

# Catch unexpected errors
def handle_unexpected_exception(exc_type, exc_value, exc_traceback):
    logging.error("🔥 Uncaught Exception:", exc_info=(exc_type, exc_value, exc_traceback))
sys.excepthook = handle_unexpected_exception

# Ensure API key is loaded
CMC_API_KEY = os.getenv("CMC_API_KEY")
if not CMC_API_KEY:
    logging.error("❌ CMC_API_KEY is not set. Please set it in environment variables.")
    sys.exit(1)

class FGIRequest(Model):
    limit: Optional[int] = 1

class FearGreedData(Model):
    value: float
    value_classification: str
    timestamp: str

class FGIResponse(Model):
    data: list[FearGreedData]
    status: str
    timestamp: str

# Initialize Agent
agent = Agent(
    name="FGIagent",
    port=8010,
    seed="fgi_agent1_secret_phrase",
    endpoint=["http://127.0.0.1:8010/submit"],
    )

@agent.on_event("startup")
async def startup(ctx: Context):
    """Initialize agent with a test request"""
    ctx.logger.info(f"✅ Agent started: {ctx.agent.address}")
    #dummy_request = FGIRequest(limit=1)
    #await process_response(ctx, dummy_request)
    
    
def get_fear_and_greed_index(limit: int = 1) -> FGIResponse:
    """Fetch Fear and Greed index data from CoinMarketCap API"""
    url = "https://pro-api.coinmarketcap.com/v3/fear-and-greed/historical"

    headers = {
        "X-CMC_PRO_API_KEY": CMC_API_KEY
    }
    
    params = {
        "limit": limit
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raises error for non-200 status codes
        
        raw_data = response.json()
        fear_greed_data = []

        for entry in raw_data.get("data", []):
            data = FearGreedData(
                value=entry["value"],
                value_classification=entry["value_classification"],
                timestamp=entry["timestamp"]
            )
            fear_greed_data.append(data)

        #return FGIResponse(
        #    data=fear_greed_data,
        #    status="success",
        #    timestamp=datetime.utcnow(timezone.utc).isoformat()
        #)
        
        return FGIResponse(
            data=fear_greed_data,
            status="success",
            timestamp=datetime.now(timezone.utc).isoformat()
        )
    
    except requests.exceptions.RequestException as e:
        logging.error(f"⚠️ API Request Failed: {e}")
        return FGIResponse(data=[], status="error", timestamp=datetime.utcnow().isoformat())


async def process_response(ctx: Context, msg: FGIRequest) -> FGIResponse:
    """Process the request and return formatted response"""
    logging.debug("🔄 Processing request...")

    fear_greed_data = get_fear_and_greed_index(msg.limit)
    
    for entry in fear_greed_data.data:
        ctx.logger.info(f"📊 Fear and Greed Index: {entry.value}")
        ctx.logger.info(f"🔍 Classification: {entry.value_classification}")
        ctx.logger.info(f"⏳ Timestamp: {entry.timestamp}")
    
    return fear_greed_data


@agent.on_message(model=FGIRequest)
async def handle_message(ctx: Context, sender: str, msg: FGIRequest):
    """Handle incoming messages requesting Fear and Greed index data"""
    ctx.logger.info(f"📩 Received message from {sender}: FGIRequest for {msg.limit} entries")
    logging.info(f"📩 Received message from {sender}: FGIRequest for {msg.limit} entries")
    
    response = await process_response(ctx, msg)
    
    await ctx.send(sender, response)

    return response


if __name__ == "__main__":
    try:
        logging.info("🚀 Starting the FGI agent...")
        agent.run()
    except Exception as e:
        logging.error(f"❌ Fatal Error: {e}")
