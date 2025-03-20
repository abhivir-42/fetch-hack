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




class SwaplandRequest(Model):
    blockchain: str
    signal: str
    amount: float

class SwaplandResponse(Model):
    status: str








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
    readme=
    """![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag:domain/tag-of-your-agent](https://img.shields.io/badge/domain-colorcode)

**Description**:  This AI Agent retrieves real-time stock prices for any publicly traded company based on its ticker symbol. It provides  share prices, stock quotes, and stock prices to users. Simply input a stock ticker (e.g., AAPL, TSLA)  to get the latest stock price.

**Input Data Model**
class StockPriceRequest(Model):
    ticker: str

**Output Data Model**
class StockPriceResponse(Model):
    price: float""",
    endpoint=["http://127.0.0.1:8017/submit"],
    )


@agent.on_event("startup")
async def introduce_agent(ctx: Context):
    """Logs agent startup details."""
    logging.info(f"✅ Agent started: {ctx.agent.address}")
    print(f"Hello! I'm {agent.name} and my address is {agent.address}.")
    logging.info("🚀 Agent startup complete.")


@agent.on_interval(period=24 * 60 * 60.0)  # Runs every 24 hours
async def swapland_request(ctx: Context):
    """Requests market data for the monitored coin once a day."""
    try:
        chain = "base"
        amountt = 1.0
        signall = "Buy"
        await ctx.send(SWAPLAND_AGENT, SwaplandRequest(blockchain=chain,signal=signall, amount = amountt))
        print(f"Sent request") #stuck here

    except Exception as e:
        logging.error(f"Failed to send request: {e}")

# Handle incoming messages with the SwaplandResponse model from ai agent
@uagent.on_message(model=SwaplandResponse)
async def message_handler(ctx: Context, sender: str, msg: SwaplandResponse):
    ctx.logger.info(f"Received message from {sender}: {msg.status}")


# Ensure the agent starts running
if __name__ == "__main__":
    try:
        logging.info("🔥 Starting the agent...")
        agent.run()
    except Exception as e:
        logging.error(f"❌ Error starting the agent: {e}")
