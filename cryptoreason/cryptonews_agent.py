#pip install newsapi-python
import os
import logging
import sys
import json
import requests
from typing import Optional
from uagents import Agent, Context, Model
import atexit
from newsapi import NewsApiClient

from datetime import datetime, timedelta



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
    port=8005,
    seed="newsnewshehhee_agent1_secret_phrase",
    endpoint=["http://127.0.0.1:8005/submit"],
    )


@agent.on_event("startup")
async def startup(ctx: Context):
    """Initialize agent with a test request"""
    ctx.logger.info(f"✅ Agent started: {ctx.agent.address}")
    
    #test it
    #response = get_recent_crypto_news()
    #ctx.logger.info(f"{response}")


def get_recent_crypto_news(limit: int = 1) -> CryptonewsResponse:
    """Fetch crypto news data from NewsAPI"""
    
    today = datetime.today().strftime('%Y-%m-%d')# Get today's date
    yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')# Get yesterday's date by subtracting 1 day
   
    crypto_news=""
    news_output=""
    
    try:
        newsapi = NewsApiClient(api_key="94b2d38f6b104eafa2f041bc323ed03c")#"NEWS_API_KEY"
        #94b2d38f6b104eafa2f041bc323ed03c 1b523a692b7640858f842cd09acc67df
        crypto_news = newsapi.get_everything(q="crypto OR cryptocurrency OR bitcoin OR ethereum OR recession OR FOMC OR crypto exchange OR bearish OR bullish",from_param=str(yesterday),to=str(today), sort_by = "relevancy", page=20, language="en")#recession, FOMC, crypto exchange, bearish, bullish, financial market
        #we need to optimise the size, otherwise it may exceed ASI1 28000 tokens limit
        # Parse the JSON string into a Python dictionary
        #news are delayed by 1 day with free version
        data = json.loads(crypto_news)

        # Create NEWOUTPUT with only title, description, and content
        news_output = {
            "title": data["title"],
            "description": data["description"],
            "content": data["content"]
        }
        
        
        
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
        
    return json.dumps(crypto_news) #news_output
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
        logging.info("🚀 Starting the CryptoNews agent...")
        agent.run()
    except Exception as e:
        logging.error(f"❌ Fatal Error: {e}")

