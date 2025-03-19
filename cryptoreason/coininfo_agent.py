import os
import logging
import sys
import requests
import atexit
from uagents import Agent, Context, Model

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

class CoinRequest(Model):
    blockchain: str

class CoinResponse(Model):
    name: str
    symbol: str
    current_price: float
    market_cap: float
    total_volume: float
    price_change_24h: float

# Initialize Agent
agent = Agent(
    name="CoinInfoAgent",
    port=8009,
    seed="coin_info_agent1_secret_phrase",
    endpoint=["http://127.0.0.1:8009/submit"],
    )

def get_crypto_info(blockchain: str) -> CoinResponse:
    match blockchain:
        case "ethereum" | "base":  # Both map to "ethereum"
            coin_id = "ethereum"
        case "bitcoin":
            coin_id = "bitcoin"
        case "matic-network":
            coin_id = "matic-network"
        case _:
            raise ValueError(f"Unsupported blockchain: {blockchain}")  # Handle unexpected inputs
            #what would happen to the execution in this case?
        
    """Fetch cryptocurrency information from CoinGecko API"""
    
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
    
    try:
        response = requests.get(url)
        logging.info("🚀 URL for {coint_id} received...")
        response.raise_for_status()  # Raises an error for non-200 responses

        data = response.json()
        
        return CoinResponse(
            name=data['name'],
            symbol=data['symbol'].upper(),
            current_price=data['market_data']['current_price']['usd'],
            market_cap=data['market_data']['market_cap']['usd'],
            total_volume=data['market_data']['total_volume']['usd'],
            price_change_24h=data['market_data']['price_change_percentage_24h']
        )
    
    except requests.exceptions.RequestException as e:
        logging.error(f"⚠️ API Request Failed: {e}")
        return CoinResponse(
            name="Unknown",
            symbol="N/A",
            current_price=0.0,
            market_cap=0.0,
            total_volume=0.0,
            price_change_24h=0.0
        )

async def process_response(ctx: Context, msg: CoinRequest) -> CoinResponse:
    """Process the crypto request and return formatted response"""
    logging.debug(f"🔄 Fetching crypto data for: {msg.blockchain}")

    crypto_data = get_crypto_info(msg.blockchain)
    
    ctx.logger.info(f"📊 Crypto Info: {crypto_data}")
    return crypto_data

@agent.on_event("startup")
async def startup(ctx: Context):
    """Initialize agent with a startup message"""
    ctx.logger.info(f"✅ Agent started: {ctx.agent.address}")

@agent.on_message(model=CoinRequest)
async def handle_message(ctx: Context, sender: str, msg: CoinRequest):
    """Handle incoming messages requesting crypto information"""
    ctx.logger.info(f"📩 Received message from {sender}: {msg.blockchain}")
    
    response = await process_response(ctx, msg)
    await ctx.send(sender, response)

    return response

if __name__ == "__main__":
    try:
        logging.info("🚀 Starting the CoinInfoAgent...")
        agent.run()
        
    except Exception as e:
        logging.error(f"❌ Fatal Error: {e}")
