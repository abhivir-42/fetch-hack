import logging
import sys
import atexit
from uagents import Agent, Context, Model
from typing import Optional
from asi.llm import query_llm

#ask for chain the user would like to watch and add to variable chain
#based on the choise base, ether, or polygon, choose or discover appropriate coin info agent.

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

# Initialize the agent
#logging.info("🚀 Initializing the Sentiment-Based Crypto Sell Alerts Agent...")
agent = Agent(
    name="SentimentBased CryptoSellAlerts",
    port=8017,
    seed="this_is_main_agent_to_run",
    mailbox = True,
    endpoint=["http://127.0.0.1:8017/submit"],
    )


# Agentverse agent addresses
COIN_AGENT="agent1qw6cxgq4l8hmnjctm43q97vajrytuwjc2e2n4ncdfpqk6ggxcfmxuwdc9rq"
FGI_AGENT="agent1qgzh245lxeaapd32mxlwgdf2607fkt075hymp06rceknjnc2ylznwdv8up7"

NETWORK = "bitcoin"

### AGENTVERSE INTERACTION CLASSES ###
class CoinRequest(Model):
    blockchain: str

#define models for other agents to be discovered locally
#class CoinRequest(Model):
 #   blockchain: str

class CoinResponse(Model):
    name: str
    symbol: str
    current_price: float
    market_cap: float
    total_volume: float
    price_change_24h: float

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

@agent.on_event("startup")
async def introduce_agent(ctx: Context):
    """Logs agent startup details."""
    logging.info(f"✅ Agent started: {ctx.agent.address}")
    print(f"Hello! I'm {agent.name} and my address is {agent.address}.")
    logging.info("🚀 Agent startup complete.")


@agent.on_interval(period=24 * 60 * 60.0)  # Runs every 24 hours
async def check_coin(ctx: Context):
    """Requests market data for the monitored coin once a day."""
    try:
        # Confirm chain
        print(f"Please, confirm the chain to request the data from")
        chain = input("Blockchain [ethereum/base/bitcoin/matic-network]? ").lower()
        
        if ((chain != "base") and (chain != "ethereum") and (chain != "matic-network") and (chain != "bitcoin")):
            print("Aborted")
            sys.exit(1)
        
        NETWORK = chain
        
        await ctx.send(COIN_AGENT, CoinRequest(blockchain=chain))
        print(f"Sent request") #stuck here

    except Exception as e:
        logging.error(f"Failed to send request: {e}")


@agent.on_message(model=CoinResponse)
async def handle_coin_response(ctx: Context, sender: str, msg: CoinResponse):
    """Handles coin market data and requests FGI if price drop exceeds 10%."""
    logging.info(f"📩 Received CoinResponse: {msg}")
    
    # Check if price has dropped by 10% or more before requesting FGI analysis
    if msg.price_change_24h < -3.0:
        logging.warning(f"⚠️ {msg.symbol} price dropped by {msg.price_change_24h}%. Requesting FGI data.")
        try:
            await ctx.send(FGI_AGENT, FGIRequest())
        except Exception as e:
            logging.error(f"❌ Error sending FGIRequest: {e}")
    elif msg.price_change_24h > +3.0:
        logging.warning(f"🚀 {msg.symbol} price raised by {msg.price_change_24h}%. Requesting FGI data.")
        try:
            await ctx.send(FGI_AGENT, FGIRequest())
        except Exception as e:
            logging.error(f"❌ Error sending FGIRequest: {e}")
    else:
        logging.warning(f"No majour fluctuations in the market!")
        try:
            await ctx.send(FGI_AGENT, FGIRequest())
        except Exception as e:
            logging.error(f"❌ Error sending FGIRequest: {e}")


@agent.on_message(model=FGIResponse)
async def handle_fgi_response(ctx: Context, sender: str, msg: FGIResponse):
    """Analyzes FGI data and determines whether to issue a SELL alert."""
    logging.info(f"📊 Received FGIResponse: {msg}")

    # Construct the AI prompt
    prompt = f'''
    Given the following information, respond with either SELL, BUY or HOLD native token from {NETWORK} network.
    
    
    Fear Greed Index Analysis:
    {msg}
    
    Coin Market Data:
    {msg}
    '''
    #add recent news description within this agent

    try:
        response = query_llm(prompt)  # Query ASI1 Mini for a decision
        
        if "SELL" in response:
            logging.critical("🚨 SELL SIGNAL DETECTED!")
            print("SELL")
            #start search an run of ETH to USDC swap agent
        elif "BUY" in response:
            logging.critical("✅ BUY SIGNAL DETECTED!")
            print("BUY")
            #start search an run of ETH to USDC swap agent
        else:
            logging.info("⏳ HOLD decision received.")
            print("HOLD")
    
    except Exception as e:
        logging.error(f"❌ Error querying ASI1 model: {e}")

# Ensure the agent starts running
if __name__ == "__main__":
    try:
        logging.info("🔥 Starting the agent...")
        agent.run()
    except Exception as e:
        logging.error(f"❌ Error starting the agent: {e}")
