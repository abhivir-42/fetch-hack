from uagents import Agent, Context, Protocol, Model, Field
import random
import logging
from uagents.agent import AgentRepresentation #to use txn wallet
from uagents.setup import fund_agent_if_low

import sys
import os
from dotenv import load_dotenv

from logging import Logger

from cosmpy.aerial.client import LedgerClient
from cosmpy.aerial.faucet import FaucetApi
from cosmpy.crypto.address import Address
from cosmpy.aerial.config import NetworkConfig
from cosmpy.aerial.wallet import LocalWallet

from uagents.config import TESTNET_REGISTRATION_FEE
from uagents.network import get_faucet, get_ledger
from uagents.utils import get_logger

import argparse
import time

import asyncio


class TopupRequest(Model):
    amount: float
    #wal: str

class TopupResponse(Model):
    status: str
 
 
farmer = Agent(
    name="Farmer agent faucet collector",
    port=8002,
    seed="kjpopoFJpwjofemwffrekfkkssfbrSTRgkfobgnh98hjio38j398902098f89ehf978jijoevm90werw8u0gjkkjkjINGS",
    endpoint=["http://localhost:8002/submit"],
)

ONETESTFET=1000000000000000000
UNCERTAINTYFET=1000000000000000

fund_agent_if_low(farmer.wallet.address())
 
@farmer.on_event("startup")
async def introduce_agent(ctx: Context):
    ctx.logger.info(farmer.address)
    ctx.logger.info(farmer.wallet.address())
    

"""
 #need to add some pause before starting
@farmer.on_interval(50)
async def get_faucet_farmer(ctx: Context):
    ledger: LedgerClient = get_ledger()
    faucet: FaucetApi = get_faucet()
    #fund_agent_if_low(farmer.wallet.address())
    faucet.get_wealth(farmer.wallet.address())
    agent_balance = ledger.query_bank_balance(Address(farmer.wallet.address()))
    converted_balance = agent_balance/ONETESTFET
    
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
    
    if (converted_balance >1):
        # delegate some tokens to this validator
        agent_balance = agent_balance - UNCERTAINTYFET
        #tx = ledger_client.delegate_tokens(validator.address, agent_balance, farmer.wallet)
        #tx.wait_to_complete()
        
        #then call function to stake
        ctx.logger.info("Delegation completed.")
        summary = ledger_client.query_staking_summary(farmer.wallet.address())
        totalstaked = summary.total_staked/ONETESTFET
        print(f"Staked: {totalstaked} TESTFET")
 """
 
 #idealy should be sending funds from the FET wallet, on mainnet. but lets farm for now
@farmer.on_message(model=TopupRequest)
async def request_funds(ctx: Context, sender: str, msg: TopupRequest):
    """Handles topup requests Topup."""
    
    #fund_agent_if_low(farmer.wallet.address())
    
    ledger: LedgerClient = get_ledger()
    faucet: FaucetApi = get_faucet()
    #print(f"📩 Sender wallet address received: {ctx.agent.wallet.address() }")
    #logging.info(f"📩 Sender wallet address received: {ctx.agent.wallet.address()}")

    sender_balance = ledger.query_bank_balance(Address("fetch1p78qz25eeycnwvcsksc4s7qp7232uautlwq2pf"))/ONETESTFET#ctx.agent.wallet.address()
    ctx.logger.info({sender_balance})
    ##faucet.get_wealth(ctx.agent.wallet.address())#ctx.agent.wallet.address() msg.wal can be removed from the class
    amo = int(msg.amount * ONETESTFET) #5 TESTFET
    deno = 'atestfet'
    
    transaction = ctx.ledger.send_tokens("fetch1p78qz25eeycnwvcsksc4s7qp7232uautlwq2pf", amo, deno,farmer.wallet)
    
    sender_balance = ledger.query_bank_balance(Address("fetch1p78qz25eeycnwvcsksc4s7qp7232uautlwq2pf"))/ONETESTFET
    sender_balance = sender_balance + amo/ONETESTFET
    logging.info(f"📩 After funds received: {sender_balance}")
    #ctx.logger.info({sender_balance})
    await asyncio.sleep(5)
    #try:
    await ctx.send(sender, TopupResponse(status="Success!"))
  #  except Exception as e:
  #      logging.error(f"❌ Error sending TopupResponse: {e}")


if __name__ == "__main__":
    load_dotenv()       # Load environment variables
    farmer.run()

