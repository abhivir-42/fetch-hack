 
from uagents.setup import fund_agent_if_low
from uagents import Agent, Context, Protocol, Model
import random
import logging
from uagents import Field
from uagents.agent import AgentRepresentation #to use txn wallet

#from ai_engine import UAgentResponse, UAgentResponseType
import sys


from logging import Logger

from cosmpy.aerial.client import LedgerClient
from cosmpy.aerial.faucet import FaucetApi
from cosmpy.crypto.address import Address

from uagents.config import TESTNET_REGISTRATION_FEE
from uagents.network import get_faucet, get_ledger
from uagents.utils import get_logger


import argparse
import time

from cosmpy.aerial.config import NetworkConfig
from cosmpy.aerial.wallet import LocalWallet




class TopupRequest(Model):
    amount: float
    #wal: str

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
    ctx.logger.info(farmer.wallet.address())

 
 #need to add some pause before starting
@farmer.on_interval(0.1)
async def get_faucet_farmer(ctx: Context):
    ledger: LedgerClient = get_ledger()
    faucet: FaucetApi = get_faucet()
    agent_balance = ledger.query_bank_balance(Address(farmer.wallet.address()))
    converted_balance = agent_balance/1000000000000000000
    faucet.get_wealth(farmer.wallet.address())
    print(f"Received: {converted_balance} TESTFET")
    #ctx.logger.info({agent_balance})
    
    #staking letsgooo
    ledger_client = LedgerClient(NetworkConfig.fetchai_stable_testnet())
    faucet_api = FaucetApi(NetworkConfig.fetchai_stable_testnet())
    validators = ledger_client.query_validators()
    # choose any validator
    validator = validators[2]
    #ctx.logger.info({validator.address})
    
    #key = PrivateKey("FX5BZQcr+FNl2usnSIQYpXsGWvBxKLRDkieUNIvMOV7=")
    #wallet = LocalWallet(key)
    #farmer_wallet = LocalWallet.from_unsafe_seed("kjpopoFJpwjofemwffreSTRgkgjkkjkjINGS")
    #ctx.logger.info({farmer_wallet})
    
    # delegate some tokens to this validator
    tx = ledger_client.delegate_tokens(validator.address, agent_balance, farmer.wallet)
    tx.wait_to_complete()
    #then call function to stake
    #my_wallet = LocalWallet.from_unsafe_seed("registration test wallet")
    ctx.logger.info("Delegation completed.")
    summary = ledger_client.query_staking_summary(farmer.wallet.address())
    totalstaked = summary.total_staked/1000000000000000000
    print(f"Staked: {totalstaked} TESTFET")
 
 
    """
    if true_reward > 0:
        print(f"Staking {true_reward} (reward after fees)")
        tx = ledger_client.delegate_tokens(validator.address, true_reward, wallet)
        tx.wait_to_complete()
    else:
        print("Fees from claim rewards transaction exceeded reward")

    end = time.monotonic()

    time.sleep(period-(end-begin))
    time_check = time.monotonic() - start_time

    """
 
 #idealy should be sending funds from the FET wallet, on mainnet. but lets farm for now
@farmer.on_message(model=TopupRequest)
async def request_funds(ctx: Context, sender: str, msg: TopupRequest):
    """Handles topup requests Topup."""
    
    ledger: LedgerClient = get_ledger()
    faucet: FaucetApi = get_faucet()
    logging.info(f"📩 Sender wallet address received: {msg.wal}")

    sender_balance = ledger.query_bank_balance(Address(ctx.agent.wallet.address()))/1000000000000000000#ctx.agent.wallet.address()
    ctx.logger.info({sender_balance})
    faucet.get_wealth(ctx.agent.wallet.address())#ctx.agent.wallet.address() msg.wal can be removed from the class
    sender_balance = ledger.query_bank_balance(Address(ctx.agent.wallet.address()))/1000000000000000000
    logging.info(f"📩 After funds received: {sender_balance}")
    #ctx.logger.info({sender_balance})
    
    try:
        await ctx.send(sender, TopupResponse(status="Success!"))
    except Exception as e:
        logging.error(f"❌ Error sending TopupResponse: {e}")


if __name__ == "__main__":
    farmer.run()

#money making farm :D just enter your agents and start printing money!


