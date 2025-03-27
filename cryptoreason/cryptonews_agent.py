import os
import logging
import sys
import json
import requests
from datetime import datetime, timezone
from typing import Optional
from uagents import Agent, Context, Model
import atexit
#pip install newsapi-python
from newsapi import NewsApiClient

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
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

class FearGreedData(Model):
    value: float
    value_classification: str
    timestamp: str

class CryptonewsRequest(Model):
    limit: Optional[int] = 1

class CryptonewsResponse(Model):
    cryptoupdates: str


# Initialize Agent
agent = Agent(
    name="Newsagent",
    port=8016,
    seed="newsnewshehhee_agent1_secret_phrase",
    mailbox = True,
    endpoint=["http://127.0.0.1:8016/submit"],
    )


@agent.on_event("startup")
async def startup(ctx: Context):
    """Initialize agent with a test request"""
    ctx.logger.info(f"✅ Agent started: {ctx.agent.address}")
    #dummy_request = FGIRequest(limit=1)
    #await process_response(ctx, dummy_request)


def get_recent_crypto_news(limit: int = 1) -> CryptonewsResponse:
    """Fetch crypto news data from NewsAPI"""
    crypto_news=""
    try:
        newsapi = NewsApiClient(api_key="94b2d38f6b104eafa2f041bc323ed03c")
        crypto_news = newsapi.get_everything(q="crypto OR cryptocurrency OR bitcoin OR ethereum OR financial market OR crypto exchange OR bullish OR bearish OR recession OR FOMC", language="en")
    except Exception as e:
        logging.error(f"❌ Couldnt connect to NEWS_API: {e}")
        #response = requests.get(url, headers=headers, params=params)
        #response.raise_for_status()  # Raises error for non-200 status codes
        logging.info(f"Found info: {crypto_news}")
        #raw_data = response.json()
        #fear_greed_data = []

        #for entry in raw_data.get("data", []):
        #    data = FearGreedData(
        #        value=entry["value"],
        #        value_classification=entry["value_classification"],
         #       timestamp=entry["timestamp"]
         #   )
        #    fear_greed_data.append(data)

        #return FGIResponse(
        #    data=fear_greed_data,
        #    status="success",
        #    timestamp=datetime.utcnow(timezone.utc).isoformat()
        #)
        
    return json.dumps(crypto_news)
            #status="success",
            #timestamp=datetime.now(timezone.utc).isoformat()
        
    

@agent.on_message(model=CryptonewsRequest)
async def handle_message(ctx: Context, sender: str, msg: CryptonewsRequest):
    """Handle incoming messages requesting crypto news data"""
    logging.info(f"📩 Received message from {sender}: CryptonewsRequest for {msg.limit} entries")
    
    response = get_recent_crypto_news(msg.limit)
    await ctx.send(sender, CryptonewsResponse(cryptoupdates=response))


if __name__ == "__main__":
    try:
        logging.info("🚀 Starting the FGI agent...")
        agent.run()
    except Exception as e:
        logging.error(f"❌ Fatal Error: {e}")

