import logging
import sys
import atexit
from uagents import Agent, Context, Model
from typing import Optional

from uagents.network import wait_for_tx_to_complete
from uagents.setup import fund_agent_if_low

from cosmpy.aerial.client import LedgerClient
from cosmpy.aerial.faucet import FaucetApi
from cosmpy.crypto.address import Address

from uagents.network import get_faucet, get_ledger
from uagents.agent import AgentRepresentation #to use txn wallet
from uagents.config import TESTNET_REGISTRATION_FEE

from cosmpy.aerial.config import NetworkConfig
from cosmpy.aerial.wallet import LocalWallet



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
TOPUP_AGENT="agent1q02xdwqwthtv6yeawrpcgpyvh8a002ueeynnltu8n6gxq0hlh8qu7ep5uhu"
REWARD_AGENT="agent1qde8udnttat2mmq3srkrz60wm3248yg43528wy2guwyewtesd73z7x3swru"

REWARD = 2000000000000000000 #expected to receive
DENOM = "atestfet"

NETWORK = "base" #default global
COININFORMATION = ""
CRYPTONEWSINFO = ""
### AGENTVERSE INTERACTION CLASSES ###

### REWARD AGENT ###
class PaymentRequest(Model):
    wallet_address: str
    amount: int
    denom: str
 
class TransactionInfo(Model):
    tx_hash: str

class PaymentInquiry(Model):
    ready: str
    
class PaymentReceived(Model):
    status: str
    
class RewardRequest(Model):
    status: str
    
class SwapCompleted(Model):
    status: str
    message: str
###--------------###

class TopupRequest(Model):
    amount: float
    #wal: str

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
    port=8001,
    seed="this_is_main_agent_to_run",
    endpoint=["http://127.0.0.1:8001/submit"],
    )


@agent.on_event("startup")
async def introduce_agent(ctx: Context):
    """Logs agent startup details."""
    #logging.info(f"✅ Agent started: {ctx.agent.address}")
    ctx.logger.info(f"Hello! I'm {agent.name} and my address is {agent.address}, my wallet address {agent.wallet.address()}")
    logging.info("Agent startup complete.")
    ledger: LedgerClient = get_ledger()
    agent_balance = ledger.query_bank_balance(Address(agent.wallet.address()))/1000000000000000000
    ctx.logger.info(f"My balance is {agent_balance} TESTFET")


@agent.on_interval(period=24 * 60 * 60.0)  # Runs every 24 hours
async def swapland_request(ctx: Context):
    """Requests market data for the monitored coin once a day."""
    
    
    #execute topup_agent to receive funds
    topupwallet = input("Would you like to top up your agent wallet?[yes/no]: ").lower()
    if (topupwallet == "yes"):
        topupamount = input("How many FET to transfer over?: ").lower()#convert from string to float
        fetchwall= (str)(agent.wallet.address())
        await ctx.send(TOPUP_AGENT, TopupRequest(amount=topupamount, wal=fetchwall))
    
    #check balance here
    #debugflag = input("wait fro the next step!..").lower()


    #execute reward_agent to pay fees for using swapland service. this might not be async though
    try:
        await ctx.send(REWARD_AGENT, PaymentInquiry(ready = "ready"))
        ctx.logger.info(f"Ready to pay status sent")
    except Exception as e:
        logging.error(f"Failed to send request to reward_Agent to pay fees for using swapland services: {e}")
    
    
    
    # i need to insert this after reason_agent(ASI1 llm) is done.
    try:
        chain = NETWORK
        #money = input("How much would you like to swap?: ").lower()
        #amountt = 0.1 #usdc to eth
        #signall = "Buy" #usdc to eth
        
        amountt = 0.0002 #SELL signal, ETH to USDC
        signall = "Sell" #eth to usdc
        #all works, temporary disabled to test further
        await ctx.send(SWAPLAND_AGENT, SwaplandRequest(blockchain=chain,signal=signall, amount = amountt))
        #print(f"Sent request") #stuck here

    except Exception as e:
        logging.error(f"Failed to send request: {e}")
    
    #debugflag = input("wait fro the next step!..").lower()

    #ctx.logger.info(f"Reward request sent..")

    





# Handle incoming messages with the SwaplandResponse model from ai agent swapfinder_agent
@agent.on_message(model=SwaplandResponse)
async def message_handler(ctx: Context, sender: str, msg: SwaplandResponse):
    ctx.logger.info(f"Received message from {sender}: {msg.status}")




#main agent received requested funds
@agent.on_message(model=TopupResponse)
async def response_funds(ctx: Context, sender: str, msg: TopupResponse):
    """Handles topup response."""
    logging.info(f"📩 User's wallet topped up: {msg.status}")




#received request to make a payment for execution from reward_agent
@agent.on_message(model=PaymentRequest)
async def message_handler(ctx: Context, sender: str, msg: PaymentRequest):
    ctx.logger.info(f"Received message from {sender}: {msg}")
    
    #send the payment
    fees = msg.amount /1000000000000000000 #input does not compile variables
    #logging.info(f"You are required to pay {fees} FET for this service. ")
    rewardtopay = input(f"You are required to pay {fees} FET for this service. Proceed?[yes/no]: ").lower()
    if (rewardtopay == "yes"):
        transaction = ctx.ledger.send_tokens(msg.wallet_address, msg.amount, msg.denom,agent.wallet)
    else:
        exit(1)
    # send the tx hash so reward agent can confirm with fees payment
    await ctx.send(sender, TransactionInfo(tx_hash=transaction.tx_hash))#str(ctx.agent.address)
    

#confirmation from reward_agent after main agent paid fees for exection.
@agent.on_message(model=PaymentReceived)
async def message_handler(ctx: Context, sender: str, msg: PaymentReceived):
    if (msg.status == "success"):
        ctx.logger.info(f"Fees transaction successful!")
        ledger: LedgerClient = get_ledger()
        agent_balance = ledger.query_bank_balance(Address(agent.wallet.address()))/1000000000000000000
        #print(f"Balance after fees: {agent_balance} TESTFET")
        ctx.logger.info(f"Balance after fees: {agent_balance} TESTFET")
        
    else:
        ctx.logger.info(f"Fees transaction unsuccessful!")
        exit(1)

#confirmation that reward has been received from reward_agent
@agent.on_message(model=TransactionInfo)
async def confirm_transaction(ctx: Context, sender: str, msg: TransactionInfo):
    ctx.logger.info(f"Received transaction info from {sender}: {msg}")
    tx_resp = await wait_for_tx_to_complete(msg.tx_hash, ctx.ledger)
 
    coin_received = tx_resp.events["coin_received"]
    if (
            coin_received["receiver"] == str(agent.wallet.address())
            and coin_received["amount"] == f"{REWARD}{DENOM}"
    ):
        ctx.logger.info(f"Reward transaction was successful: {coin_received}")
    else:
        ctx.logger.info(f"Transaction was unsuccessful: {coin_received}")

    ledger: LedgerClient = get_ledger()
    agent_balance = (ledger.query_bank_balance(Address(agent.wallet.address())))/1000000000000000000
    ctx.logger.info(f"Balance after receiving reward: {agent_balance} TESTFET")
    
    await ctx.send(sender,PaymentReceived(status="reward"))#str(ctx.agent.address)



# Waits for completion of swapland agents. then executes request for reward from reward_agent
@agent.on_message(model=SwapCompleted)
async def message_handler(ctx: Context, sender: str, msg: SwapCompleted):
    if (msg.status == "swapcompleted"):
        ctx.logger.info(f"{msg.message}")
        
        try:
            await ctx.send(REWARD_AGENT, RewardRequest(status="reward"))
        except Exception as e:
            logging.error(f"Failed to send request for reward: {e}")
    
    else:
        ctx.logger.info(f"Fail to execute swap via swapland: {msg.status}")



# Ensure the agent starts running
if __name__ == "__main__":
    try:
        logging.info("Starting the agent...")
        agent.run()
    except Exception as e:
        logging.error(f"Error starting the agent: {e}")
