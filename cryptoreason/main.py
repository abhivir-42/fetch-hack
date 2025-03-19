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

# Agentverse agent addresses
COIN_AGENT="agent1qw6cxgq4l8hmnjctm43q97vajrytuwjc2e2n4ncdfpqk6ggxcfmxuwdc9rq"
FGI_AGENT="agent1qgzh245lxeaapd32mxlwgdf2607fkt075hymp06rceknjnc2ylznwdv8up7"
REASON_AGENT="agent1qwlg48h8sstknk7enc2q44227ahq6dr5mjg0p7z62ca6tfueze38kyrtyl2"
CRYPTONEWS_AGENT="agent1q2cq0q3cnhccudx6cym8smvpquafsd99lrwexppuecfrnv90xlrs5lsxw6k"#add this once registerd

NETWORK = "bitcoin" #default global
COININFORMATION = ""
CRYPTONEWSINFO = ""
### AGENTVERSE INTERACTION CLASSES ###
class CoinRequest(Model):
    blockchain: str

#define models for other agents to be discovered locally
#class CoinRequest(Model):
 #   blockchain: str

class CryptonewsRequest(Model):
    limit: Optional[int] = 1

class CryptonewsResponse(Model):
    cryptoupdates: str
    
class ASI1Request(Model):
    query: str
    
class ASI1Response(Model):
    decision: str

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

# Initialize the agent
#logging.info("🚀 Initializing the Sentiment-Based Crypto Sell Alerts Agent...")
agent = Agent(
    name="SentimentBased CryptoSellAlerts",
    port=8017,
    seed="this_is_main_agent_to_run",
    endpoint=["http://127.0.0.1:8017/submit"],
    )


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
    """Handles coin market data and requests Cryptonews."""
    logging.info(f"📩 Received CoinResponse: {msg}")
    COININFORMATION = msg
    try:
        await ctx.send(CRYPTONEWS_AGENT, CryptonewsRequest()) #need to sent the data from this coin, change within 24 hours!
    except Exception as e:
        logging.error(f"❌ Error sending CryptonewsRequest: {e}")


@agent.on_message(model=CryptonewsResponse)
async def handle_cryptonews_response(ctx: Context, sender: str, msg: CryptonewsResponse):
    """Handles cryptonews market data and requests FGI"""
    logging.info(f"📩 Received CryptonewsResponse!")
    CRYPTONEWSINFO = msg
    logging.info(f"📩 Sending request to FGI!")
    try:
        await ctx.send(FGI_AGENT, FGIRequest())
        logging.info(f"📩 Request to FGI sent!")
    except Exception as e:
        logging.error(f"❌ Error sending FGIRequest: {e}")


@agent.on_message(model=FGIResponse)
async def handle_fgi_response(ctx: Context, sender: str, msg: FGIResponse):
    """Analyzes FGI data and determines whether to issue a SELL alert."""
    logging.info(f"📊 Received FGIResponse: {msg}")

    print(f"Please, confirm if you long-term or short-term investor?")
    investor = input("Investor [long-term/short-term/speculate]: ").lower()
    if ((investor != "long-term") and (investor != "short-term") and (investor != "speculate")):
        print("Aborted")
        sys.exit(1)
        
    print(f"Please, confirm your risk strategy for investments?")
    risk = input("Risk strategy [conservative/balanced/aggressive/speculative]: ").lower()
    if ((risk != "conservative") and (risk != "balanced")and (risk != "aggressive")and (risk != "speculative")):
        print("Aborted")
        sys.exit(1)
            
    # Construct the AI prompt
    prompt = f'''    
    Consider the following factors:
    
    Fear Greed Index Analysis - {msg}
    Coin Market Data - {COININFORMATION}
    User's type of investing - {investor}
    User's risk strategy - {risk}
    
    Most recent crypto news - {CRYPTONEWSINFO}
    
    You are a crypto expert, who is assisting the user to make the most meaningful decisions, to gain the most revenue. 
    Given the following information, respond with one word, either "SELL", "BUY" or "HOLD" native token from {NETWORK} network.
    '''
    
    try:
        #response = query_llm(prompt)  # Query ASI1 Mini for a decision
        #compined prompt sent to ASI1 agent
        await ctx.send(REASON_AGENT, ASI1Request(query=prompt))
        #moved to Asi1Response
    except Exception as e:
        logging.error(f"❌ Error querying ASI1 model: {e}")


@agent.on_message(model=ASI1Response)
async def handle_asi1_query(ctx: Context, sender: str, msg: ASI1Response):
    if "SELL" in msg.decision:
        logging.critical("🚨 SELL SIGNAL DETECTED!")
        print("SELL")
        #start search an run of ETH to USDC swap agent
    elif "BUY" in msg.decision:
        logging.critical("✅ BUY SIGNAL DETECTED!")
        print("BUY")
        #start search an run of ETH to USDC swap agent
    else:
        logging.info("⏳ HOLD decision received.")
        print("HOLD")





# Ensure the agent starts running
if __name__ == "__main__":
    try:
        logging.info("🔥 Starting the agent...")
        agent.run()
    except Exception as e:
        logging.error(f"❌ Error starting the agent: {e}")
