from uagents import Agent, Context
from pydantic import BaseModel
from typing import Optional
from asi.llm import query_llm

# Initialize the agent with a name and mailbox enabled for communication
agent = Agent(name="Sentiment-Based Crypto Sell Alerts Agent", mailbox=True)

# Coin to monitor
COIN_ID = "bitcoin"

### AGENTVERSE AGENTS ###
# These are the addresses of the deployed agents on Agentverse
COIN_AGENT = "agent1qw6cxgq4l8hmnjctm43q97vajrytuwjc2e2n4ncdfpqk6ggxcfmxuwdc9rq"
FGI_AGENT = "agent1qgzh245lxeaapd32mxlwgdf2607fkt075hymp06rceknjnc2ylznwdv8up7"

### AGENTVERSE INTERACTION CLASSES ###
# Request model for retrieving coin data
class CoinRequest(BaseModel):
    coin_id: str

# Response model for coin data
class CoinResponse(BaseModel):
    name: str
    symbol: str
    current_price: float
    market_cap: float
    total_volume: float
    price_change_24h: float

# Request model for Fear Greed Index (FGI) data
class FGIRequest(BaseModel):
    limit: Optional[int] = 1

# Model for individual FGI data points
class FearGreedData(BaseModel):
    value: float
    value_classification: str
    timestamp: str

# Response model for FGI data
class FGIResponse(BaseModel):
    data: list[FearGreedData]
    status: str
    timestamp: str

# Global variables to store agent responses
market_data = None  # Stores the latest market data of the coin
fgi_analysis = None  # Stores the latest Fear Greed Index analysis

# Seed phrase for deploying the local agent as a mailbox
# This enables the agent to receive messages from Agentverse agents
# Learn more: https://fetch.ai/docs/guides/agentverse/agentverse-mailbox/utilising-the-mailbox
SEED_PHRASE = "fefefeajhsdyta87sdbajuhsdb78gb78B8BubUH99Bhj"

@agent.on_event("startup")
async def introduce_agent(ctx: Context):
    """Introduces the agent when it starts running."""
    print(f"Hello! I'm {agent.name} and my address is {agent.address}.")

@agent.on_interval(period=24 * 60 * 60.0)  # Runs every 24 hours
async def check_coin(ctx: Context):
    """Requests market data for the monitored coin once a day."""
    await ctx.send(COIN_AGENT, CoinRequest(coin_id=COIN_ID))

@agent.on_message(model=CoinResponse)
async def handle_coin_response(ctx: Context, sender: str, msg: CoinResponse):
    """Handles incoming coin market data and requests FGI data if the price drop exceeds 10%."""
    global market_data
    market_data = msg
    
    # Check if price has dropped by 10% or more before requesting FGI analysis
    if msg.price_change_24h <= -10.0:
        await ctx.send(FGI_AGENT, FGIRequest())

@agent.on_message(model=FGIResponse)
async def handle_fgi_response(ctx: Context, sender: str, msg: FGIResponse):
    """Analyzes Fear Greed Index data and determines whether to issue a SELL alert."""
    global fgi_analysis
    fgi_analysis = msg
    
    # Construct the AI prompt based on current market and sentiment analysis
    prompt = f'''
    Given the following information, respond with either SELL or HOLD for the coin {COIN_ID}.
    
    Below is analysis on the Fear Greed Index:
    {fgi_analysis}
    
    Below is analysis on the coin:
    {market_data}
    '''
    
    print(prompt)  # Debugging log
    
    response = query_llm(prompt)  # Query the AI for a decision
    
    print(response)  # Output AI response
    print()
    
    # Interpret the AI response and print SELL or HOLD decision
    if "SELL" in response:
        print("SELL")
    else:
        print("HOLD")

if __name__ == "__main__":
    agent.run()
