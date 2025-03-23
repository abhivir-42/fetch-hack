import logging
import sys
import atexit
from uagents import Agent, Context, Model
from typing import Optional


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

SWAPLAND_AGENT="agent1qv9phv30v8gpm9r4cwk0djhuzdvsa7rdzm2k5tnefmdu76mp92l9zuqeexs"
TOPUP_AGENT="agent1qw0zrryt8fme4svuldt4vx5m929gwtx9vxxhustkxd4dh2gyp4fp2lw8cme"

NETWORK = "bitcoin" #default global
COININFORMATION = ""
CRYPTONEWSINFO = ""
### AGENTVERSE INTERACTION CLASSES ###


class TopupRequest(Model):
    amount: float
    wal: str

class TopupResponse(Model):
    status: str
    
class SwaplandRequest(Model):
    blockchain: str
    signal: str
    amount: float

class SwaplandResponse(Model):
    status: str

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
    print(f"Hello! I'm {agent.name} and my address is {agent.address}, my wallet address {agent.wallet.address()} ")
    logging.info("🚀 Agent startup complete.")


@agent.on_interval(period=24 * 60 * 60.0)  # Runs every 24 hours
async def swapland_request(ctx: Context):
    """Requests market data for the monitored coin once a day."""
    
    topupwallet = input("Would you like to top up your agent wallet?[yes/no]: ").lower()
    if (topupwallet == "yes"):
        topupamount = input("How many FET to transfer over?: ").lower()#convert from string to float
        fetchwall= (str)(agent.wallet.address())
        amoun = 23.0
        await ctx.send(TOPUP_AGENT, TopupRequest(amount=amoun, wal=fetchwall))
    
    try:
        chain = "base"
        amountt = 1.0
        signall = "Buy"
        await ctx.send(SWAPLAND_AGENT, SwaplandRequest(blockchain=chain,signal=signall, amount = amountt))
        print(f"Sent request") #stuck here

    except Exception as e:
        logging.error(f"Failed to send request: {e}")

# Handle incoming messages with the SwaplandResponse model from ai agent
@agent.on_message(model=SwaplandResponse)
async def message_handler(ctx: Context, sender: str, msg: SwaplandResponse):
    ctx.logger.info(f"Received message from {sender}: {msg.status}")


@agent.on_message(model=TopupResponse)
async def response_funds(ctx: Context, sender: str, msg: TopupResponse):
    """Handles topup response."""
    logging.info(f"📩 Received Topup request: {msg.status}")
    #COININFORMATION = msg
    try:
        await ctx.send(sender, TopupResponse()) #need to sent the data from this coin, change within 24 hours!
    except Exception as e:
        logging.error(f"❌ Error sending CryptonewsRequest: {e}")




# Ensure the agent starts running
if __name__ == "__main__":
    try:
        logging.info("🔥 Starting the agent...")
        agent.run()
    except Exception as e:
        logging.error(f"❌ Error starting the agent: {e}")
