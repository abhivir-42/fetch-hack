#pip install newsapi-python
import os
from dotenv import load_dotenv
import logging
import sys
import json
import requests
from typing import Optional
from uagents import Agent, Context, Model
import atexit
from newsapi import NewsApiClient

from datetime import datetime, timedelta


# Ensure API key is loaded
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

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
    ctx.logger.info(f"Agent started: {ctx.agent.address}")
    
    #test it
    #response = get_recent_crypto_news()
    #ctx.logger.info(f"{response}")


def get_recent_crypto_news(limit: int = 1) -> CryptonewsResponse:
    """Fetch crypto news data from NewsAPI"""
    
    today = datetime.today().strftime('%Y-%m-%d')# Get today's date
    yesterday = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')# Get yesterday's date by subtracting 1 day
   
    crypto_news=""
    news_output=""
    extracted_data = []
    try:
        newsapi = NewsApiClient(api_key=NEWS_API_KEY)#"NEWS_API_KEY"
        
        #already a dictionary
        crypto_news = newsapi.get_everything(q="crypto OR cryptocurrency OR bitcoin OR ethereum OR recession OR FOMC OR crypto exchange OR bearish OR bullish",from_param=str(yesterday),to=str(today), sort_by = "relevancy", page_size=10, page=1, language="en")#recession, FOMC, crypto exchange, bearish, bullish, financial market
        
        logging.info(f"Found info: {crypto_news}")
        #we need to optimise the size, otherwise it may exceed ASI1 28000 tokens limit
        #news are delayed by 1 day with free version

        articles = crypto_news['articles']
        
        for article in articles:
            title = article.get('title')
            description = article.get('description')
            content = article.get('content')
            extracted_data.append({'title': title, 'description': description})#'content':content
        
        
    except Exception as e:
        logging.error(f"❌ Couldnt connect to NEWS_API: {e}")

        
    return json.dumps(extracted_data) #news_output
            #status="success",
            #timestamp=datetime.now(timezone.utc).isoformat()
        
    

@agent.on_message(model=CryptonewsRequest)
async def handle_message(ctx: Context, sender: str, msg: CryptonewsRequest):
    """Handle incoming messages requesting crypto news data"""
    logging.info(f"📩 Received message from {sender}: CryptonewsRequest for {msg.limit} entries")
    
    response = get_recent_crypto_news(msg.limit)
    await ctx.send(sender, CryptonewsResponse(cryptoupdates=response))


if __name__ == "__main__":
    load_dotenv()       # Load environment variables
    agent.run()

