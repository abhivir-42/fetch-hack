 
from uagents.setup import fund_agent_if_low
from uagents import Agent, Context, Protocol, Model
import random
import logging
from uagents import Field
#from ai_engine import UAgentResponse, UAgentResponseType
import sys


from logging import Logger

from cosmpy.aerial.client import LedgerClient
from cosmpy.aerial.faucet import FaucetApi
from cosmpy.crypto.address import Address

from uagents.config import TESTNET_REGISTRATION_FEE
from uagents.network import get_faucet, get_ledger
from uagents.utils import get_logger


class TopupRequest(Model):
    amount: float
    wal: str

class TopupResponse(Model):
    status: str
 
 
farmer = Agent(
    name="Farmer agent faucet collector",
    port=8001,
    seed="kjpopoFJpwjofemwffreSTRgkgjkkjkjINGS",
    endpoint=["http://localhost:8001/submit"],#remove this to hide
)


fund_agent_if_low(farmer.wallet.address())
 
@farmer.on_event("startup")
async def introduce_agent(ctx: Context):
    ctx.logger.info(farmer.address)

 
 #need to add some pause before starting
@farmer.on_interval(5)
async def get_faucet_farmer(ctx: Context):
    ledger: LedgerClient = get_ledger()
    faucet: FaucetApi = get_faucet()
    agent_balance = ledger.query_bank_balance(Address(farmer.wallet.address()))
    faucet.get_wealth(farmer.wallet.address())
    ctx.logger.info({agent_balance})
 
 
 #idealy should be sending funds from the FET wallet, on mainnet. but lets farm for now
@farmer.on_message(model=TopupRequest)
async def request_funds(ctx: Context, sender: str, msg: TopupRequest):
    """Handles topup requests Topup."""
    
    ledger: LedgerClient = get_ledger()
    faucet: FaucetApi = get_faucet()
    logging.info(f"📩 Sender wallet address received: {msg.wal}")

    sender_balance = ledger.query_bank_balance(Address(msg.wal))
    ctx.logger.info({sender_balance})
    faucet.get_wealth(msg.wal)
    sender_balance = ledger.query_bank_balance(Address(msg.wal))
    logging.info(f"📩 After funds received: {sender_balance}")
    #ctx.logger.info({sender_balance})
    
    try:
        await ctx.send(sender, TopupResponse(status="Success!"))
    except Exception as e:
        logging.error(f"❌ Error sending TopupResponse: {e}")


if __name__ == "__main__":
    farmer.run()

#money making farm :D just enter your agents and start printing money!


