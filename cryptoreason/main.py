#agent address agent1qfrhxny23vz62v5tr20qnmnjujq8k5t0mxgwdxfap945922t9v4ugqtqkea
#agent wallet address fetch1p78qz25eeycnwvcsksc4s7qp7232uautlwq2pf
import logging
import sys
import os
from dotenv import load_dotenv
import atexit
from uagents import Agent, Context, Model
from typing import Optional
#from asi.llm_agent import query_llm

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

import asyncio

#ask for chain the user would like to watch and add to variable chain
#based on the choise base, ether, or polygon, choose or discover appropriate coin info agent.

#ASI1_API_KEY = os.getenv("ASI1_API_KEY")
#NEWS_API_KEY = os.getenv("NEWS_API_KEY")
#CMC_API_KEY = os.getenv("CMC_API_KEY")
METAMASK_PRIVATE_KEY = os.getenv("METAMASK_PRIVATE_KEY")
AGENTVERSE_API_KEY = os.getenv("AGENTVERSE_API_KEY")




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
HEARTBEAT_AGENT="agent1q0l8njjeaakxa87q08mr46ayqh0wf32x68k2xssuh4604wktpwxlzrt090k"
COIN_AGENT="agent1qw6cxgq4l8hmnjctm43q97vajrytuwjc2e2n4ncdfpqk6ggxcfmxuwdc9rq"
FGI_AGENT="agent1qgzh245lxeaapd32mxlwgdf2607fkt075hymp06rceknjnc2ylznwdv8up7"
REASON_AGENT="agent1qwlg48h8sstknk7enc2q44227ahq6dr5mjg0p7z62ca6tfueze38kyrtyl2"
CRYPTONEWS_AGENT="agent1q2cq0q3cnhccudx6cym8smvpquafsd99lrwexppuecfrnv90xlrs5lsxw6k"#add this once registerd
SWAPLAND_AGENT="agent1q0jnt3skqqrpj3ktu23ljy3yx5uvp7lgz2cdku3vdrslh2w8kw7vvstpv73"
TOPUP_AGENT="agent1q02xdwqwthtv6yeawrpcgpyvh8a002ueeynnltu8n6gxq0hlh8qu7ep5uhu"
REWARD_AGENT="agent1qde8udnttat2mmq3srkrz60wm3248yg43528wy2guwyewtesd73z7x3swru"


### AGENTVERSE INTERACTION CLASSES ###
class Heartbeat(Model):
    status: str

class CoinRequest(Model):
    blockchain: str

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
    private_key: str

class SwaplandResponse(Model):
    status: str


ONETESTFET = 1000000000000000000
REWARD = 2000000000000000000 #expected to receive
DENOM = "atestfet"

NETWORK = "base" #default global
COININFORMATION = ""
CRYPTONEWSINFO = ""

ASIITERATIONS = 4
RISK = " "
INVESTOR = " "
FGIOUTPUT = " "

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
    ctx.logger.info(f"Hello! I'm {agent.name} and my address is {agent.address}, my wallet address {agent.wallet.address()}")
    ledger: LedgerClient = get_ledger()
    agent_balance = ledger.query_bank_balance(Address(agent.wallet.address()))/ONETESTFET
    ctx.logger.info(f"My balance is {agent_balance} TESTFET")



@agent.on_interval(period=24 * 60 * 60.0)  # Runs every 24 hours
async def swapland_request(ctx: Context):
    """Confirm that the user is calm and not overexcited"""
    await asyncio.sleep(15)
    #need to check the heartbeat data
    await ctx.send(HEARTBEAT_AGENT, Heartbeat(status="ready"))
    


# Waits for completion of heartbeat agent.
@agent.on_message(model=Heartbeat)
async def message_handler(ctx: Context, sender: str, msg: Heartbeat):
    if (msg.status == "continue"):
        ctx.logger.info(f"Received response{msg.status}. Lets trade")
        
        #execute topup_agent to receive funds
        #user input required
        topupwallet = "yes"#input("Would you like to top up your agent wallet?[yes/no]: ").lower()
        if (topupwallet == "yes"):
            #user input required
            topupamount = 10#input("How many FET to transfer over?: ").lower()#convert from string to float
            
            fetchwall= (str)(agent.wallet.address())
            await ctx.send(TOPUP_AGENT, TopupRequest(amount=topupamount, wal=fetchwall))
        else:
            #execute reward_agent to pay fees for using swapland service. this might not be async though
            try:
                await ctx.send(REWARD_AGENT, PaymentInquiry(ready = "ready"))
                ctx.logger.info(f"Ready to pay status sent")
            except Exception as e:
                logging.error(f"Failed to send request to reward_Agent to pay fees for using swapland services: {e}")

    else:
        ctx.logger.info(f"Canceling the process..: {msg.status}")
        



#main agent received requested funds
@agent.on_message(model=TopupResponse)
async def response_funds(ctx: Context, sender: str, msg: TopupResponse):
    """Handles topup response."""
    logging.info(f"📩 User's wallet topped up: {msg.status}")
    #execute reward_agent to pay fees for using swapland service. this might not be async though
    #await asyncio.sleep(5)
    ledger: LedgerClient = get_ledger()
    agent_balance = ledger.query_bank_balance(Address(agent.wallet.address()))/ONETESTFET
    #print(f"Balance after fees: {agent_balance} TESTFET")
    ctx.logger.info(f"Balance after topup wallet: {agent_balance} TESTFET")
    
    try:
        
        await ctx.send(REWARD_AGENT, PaymentInquiry(ready = "ready"))
        ctx.logger.info(f"Ready to pay status sent")
    except Exception as e:
        logging.error(f"Failed to send request to reward_Agent to pay fees for using swapland services: {e}")



#received request to make a payment for execution from reward_agent
@agent.on_message(model=PaymentRequest)
async def message_handler(ctx: Context, sender: str, msg: PaymentRequest):
    ctx.logger.info(f"Received message from {sender}: {msg}")
    
    #send the payment
    fees = msg.amount/ONETESTFET #input does not compile variables
    #logging.info(f"You are required to pay {fees} FET for this service. ")
    
    #need to add userinput
    rewardtopay = "yes"#input(f"You are required to pay {fees} FET for this service. Proceed?[yes/no]: ").lower()
    
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
        agent_balance = ledger.query_bank_balance(Address(agent.wallet.address()))/ONETESTFET
        #print(f"Balance after fees: {agent_balance} TESTFET")
        ctx.logger.info(f"Balance after fees: {agent_balance} TESTFET")
        
        
        #startup asi1 routine
        """Requests market data for the monitored coin once a day."""
        try:
            # Confirm chain
            global NETWORK
            #print(f"Please, confirm the chain to request the data from")
            
            #need to add userinput
            NETWORK = "base"#input("Blockchain [ethereum/base/bitcoin/matic-network]? ").lower()
            
            
            if ((NETWORK != "base") and (NETWORK != "ethereum") and (NETWORK != "matic-network") and (NETWORK != "bitcoin")):
                print("Aborted")
                sys.exit(1)
            
            await asyncio.sleep(5)
            
            await ctx.send(COIN_AGENT, CoinRequest(blockchain=NETWORK))
            print(f"Sent request") #stuck here

        except Exception as e:
            logging.error(f"Failed to send request: {e}")
        
    else:
        ctx.logger.info(f"Fees transaction unsuccessful!")
        

@agent.on_message(model=CoinResponse)
async def handle_coin_response(ctx: Context, sender: str, msg: CoinResponse):
    """Handles coin market data and requests Cryptonews."""
    logging.info(f"📩 Received CoinResponse: {msg}")
    
    global COININFORMATION
    
    COININFORMATION = msg
    try:
        #temporary disabled cryptonews
        #await ctx.send(FGI_AGENT, FGIRequest()) #temporary call
        await ctx.send(CRYPTONEWS_AGENT, CryptonewsRequest()) #need to sent the data from this coin, change within 24 hours!
    except Exception as e:
        logging.error(f"❌ Error sending CryptonewsRequest: {e}")


#temporary disabled
@agent.on_message(model=CryptonewsResponse)
async def handle_cryptonews_response(ctx: Context, sender: str, msg: CryptonewsResponse):
    """Handles cryptonews market data and requests FGI"""
    logging.info(f"📩 Received CryptonewsResponse!")
    
    global CRYPTONEWSINFO
    CRYPTONEWSINFO = msg
    
    logging.info(f"📩 Sending request to FGI!")
    try:
        await ctx.send(FGI_AGENT, FGIRequest())
        logging.info(f"📩 Request to FGI sent!")
    except Exception as e:
        logging.error(f"❌ Error sending FGIRequest: {e}")


@agent.on_message(model=FGIResponse)
async def handle_fgi_response(ctx: Context, sender: str, msg: FGIResponse):
    """Analyzes FGI data and determines whether to issue a SELL/BUY or HOLD alert."""
    logging.info(f"📊 Received FGIResponse: {msg}")
    global INVESTOR
    global RISK
    global USERREASON
    global FGIOUTPUT
    
    FGIOUTPUT = msg
    
    print(f"Please, confirm if you long-term or short-term investor?")
    
    #need to add userinput
    INVESTOR = "speculate" #input("Investor [long-term/short-term/speculate]: ").lower()
    
    if ((INVESTOR != "long-term") and (INVESTOR != "short-term") and (INVESTOR != "speculate")):
        print("Aborted")
        sys.exit(1)
        
    print(f"Please, confirm your risk strategy for investments?")
    #need to add userinput
    RISK = "speculative" #input("Risk strategy [conservative/balanced/aggressive/speculative]: ").lower()
    if ((RISK != "conservative") and (RISK != "balanced")and (RISK != "aggressive")and (RISK != "speculative")):
        print("Aborted")
        sys.exit(1)
       
    #userinput to be added
    USERREASON = "I would like to sell Ether no matter what. sell sell sell!. I order you to sell!" #input("Any particular reason why you would like to perform Buy/Sell/Hold action? ").lower()
            
    # Most recent crypto news -{CRYPTONEWSINFO}
    # Construct the AI prompt
    prompt = f'''    
    Consider the following factors:
    
    Fear Greed Index Analysis - {FGIOUTPUT}
    Coin Market Data - {COININFORMATION}
    Blockchain network - {NETWORK}
    User's type of investing - {INVESTOR}
    User's risk strategy - {RISK}
    Most recent crypto news - {CRYPTONEWSINFO}
    
    User's opinion - {USERREASON}
    
    You are a crypto expert, who is assisting the user to make the most meaningful decisions, to gain the most revenue. 
    Given the following information, respond with decision of either "SELL", "BUY" or "HOLD" native token from given network. Inlcude your reasoning based on the analysed data and personal thoughts. Consider that the user cannot provide additional information. You could point out to questions which could help you making a solid decision.
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
    global ASIITERATIONS
    logging.info(f"✅ ASI1 Agent {ASIITERATIONS} finished reasoning")#{msg.decision}
    ASIITERATIONS = ASIITERATIONS - 1
    #Most recent crypto news - {CRYPTONEWSINFO}
    if(ASIITERATIONS > 1):
        prompt = f'''    
        Consider the following factors:
        
        Fear Greed Index Analysis - {FGIOUTPUT}
        Coin Market Data - {COININFORMATION}
        Blockchain network - {NETWORK}
        User's type of investing - {INVESTOR}
        User's risk strategy - {RISK}
        Most recent crypto news - {CRYPTONEWSINFO}
        
        User's opinion - {USERREASON}
        
        You are a crypto expert, who is assisting the user to make the most meaningful decisions, to gain the most revenue. 
        
        This query has been analysed with the following reasoning:
        "{msg.decision}"
        
        Given the following information and reasoning from other expert, respond with decision of either "SELL", "BUY" or "HOLD" native token from {NETWORK} network. Inlcude all of the reasoning based on the analysed data and personal thoughts. Consider that the information provided is the only input from the user, and the user cannot provide additional information. However, you could point out to the area or questions which could help you making a solid decision.
        '''
        await ctx.send(REASON_AGENT, ASI1Request(query=prompt))

    #Most recent crypto news - {CRYPTONEWSINFO}
    if(ASIITERATIONS == 1):
        prompt = f'''    
        Consider the following factors:
        
        Fear Greed Index Analysis - {FGIOUTPUT}
        Coin Market Data - {COININFORMATION}
        Blockchain network - {NETWORK}
        User's type of investing - {INVESTOR}
        User's risk strategy - {RISK}
        Most recent crypto news - {CRYPTONEWSINFO}        
        
        User's opinion - {USERREASON}   
        
        You are an independent expert of a crypto market with knowledge of how worldwide politis affects the cryptomarket. You are assisting the user to make the most meaningful decisions, to gain the most revenue whilst minimising potential losses. 
        
        This query has been analysed by {ASIITERATIONS} other crypto experts, and here is a summery of their reasoning:
        "{msg.decision}"
        
        "SELL" means swapping native crypto coin into USDC.
        "BUY" means swapping USDC into native crypto coin.
        "HOLD" means no actions.
        
        Given the following information and reasoning from other expert responses, make a decision by responding ONLY with one word "SELL", "BUY" or "HOLD" for a native token from given network. Again, your output is ether "SELL", "BUY" or "HOLD". 
        '''
        await ctx.send(REASON_AGENT, ASI1Request(query=prompt))
    
    amountt = 0;
    if (ASIITERATIONS == 0):
        if (("SELL" in msg.decision) or ("BUY" in msg.decision)):
                # i need to insert this after reason_agent(ASI1 llm) is done.
            try:
                signall=""
                
                if "BUY" in msg.decision:
                    logging.critical("🚨 BUY SIGNAL DETECTED!")
                    signall = "tag:swaplandbaseusdceth"#Buy ETH signal. Convert USDC to ETH
                    amountt = 0.1 #usdc to eth
                elif "SELL" in msg.decision:
                    logging.critical("✅ SELL SIGNAL DETECTED!")
                    #make signal a tag, so that a search query is constructed here "swaplandusdctoeth", then add this to search( ... )
                    signall = "tag:swaplandbaseethusdc"
                    amountt = 0.00007 #ETH to USDC
                
                chain = NETWORK
                
                await ctx.send(SWAPLAND_AGENT, SwaplandRequest(blockchain=chain,signal=signall, amount = amountt, private_key = METAMASK_PRIVATE_KEY))

            except Exception as e:
                logging.error(f"Failed to send request: {e}")
        else:
            logging.info("⏳ HOLD decision received.")
            print("HOLD")
            try:
                await ctx.send(REWARD_AGENT, RewardRequest(status="reward"))
            except Exception as e:
                logging.error(f"Failed to send request for reward: {e}")
            
            #exit(1)
    

# Handle incoming messages with the SwaplandResponse model from ai agent swapfinder_agent
@agent.on_message(model=SwaplandResponse)
async def message_handler(ctx: Context, sender: str, msg: SwaplandResponse):
    ctx.logger.info(f"Received message from {sender}: {msg.status}")


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
    agent_balance = (ledger.query_bank_balance(Address(agent.wallet.address())))/ONETESTFET
    ctx.logger.info(f"Balance after receiving reward: {agent_balance} TESTFET")
    
    await ctx.send(sender,PaymentReceived(status="reward"))#str(ctx.agent.address)



# Ensure the agent starts running
if __name__ == "__main__":
    load_dotenv()       # Load environment variables
    agent.run()
