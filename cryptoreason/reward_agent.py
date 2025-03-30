#this agent receives request to get the reward. upon request it checks storage fet, and send the , confirms with given agent address and sends the reward. test tokens for now

import logging
from uagents import Agent, Context, Model
from uagents.network import wait_for_tx_to_complete
from uagents.setup import fund_agent_if_low

from cosmpy.aerial.client import LedgerClient
from cosmpy.aerial.faucet import FaucetApi
from cosmpy.crypto.address import Address
 
from uagents.network import get_faucet, get_ledger
from uagents.agent import AgentRepresentation #to use txn wallet

from logging import Logger
import sys
from uagents.config import TESTNET_REGISTRATION_FEE
from uagents.utils import get_logger
import argparse
import time
from cosmpy.aerial.config import NetworkConfig
from cosmpy.aerial.wallet import LocalWallet

 
class PaymentRequest(Model):
    wallet_address: str
    amount: int
    denom: str
 
class TransactionInfo(Model):
    tx_hash: str

class PaymentInquiry(Model):
    ready: str
 #ctx.agent.wallet.address()
 
class RewardRequest(Model):
    ready: str

class PaymentReceived(Model):
    status: str


AMOUNT = 1000000000000000000
DENOM = "atestfet"

REWARD = 1000000000000000000
#DENOM = "afet"

reward = Agent(name="reward", seed="reward secret phrase agent oekwpfokw", port=8003, endpoint=["http://127.0.0.1:8003/submit"])
 
fund_agent_if_low(reward.wallet.address(), min_balance=AMOUNT)
 
 
@reward.on_event("startup")
async def introduce_agent(ctx: Context):
    """Logs agent startup details."""
    logging.info(f"✅ Agent started: {ctx.agent.address}")
    ctx.logger.info(f"MHello! I'm {reward.name} and my address is {reward.address}, my wallet address {reward.wallet.address()} ")

    logging.info("🚀 Agent startup complete.")
    ledger: LedgerClient = get_ledger()
    agent_balance = ledger.query_bank_balance(Address(reward.wallet.address()))/1000000000000000000
    ctx.logger.info(f"My balance is {agent_balance} TESTFET")
    
    
    
    
    #local_ledger = {"agent_address":"this is my address", "tx":"transaction0409283"}
    #ctx.storage.set("1331331", local_ledger)
    #check = ctx.storage.get("1331331")
    #ctx.logger.info(f"My check is {check['agent_address']}")
    #ctx.storage.remove("1331331")
    #check = ctx.storage.get("1331331")
    #ctx.logger.info(f"My check is {check} after removal")

    
@reward.on_message(model=PaymentInquiry)
async def send_payment(ctx: Context, sender: str, msg: PaymentInquiry):
    ctx.logger.info(f"Received payment request from {sender}: {msg}")
    if(msg.ready == "ready"):
        await ctx.send(sender,PaymentRequest(wallet_address=str(reward.wallet.address()), amount=AMOUNT, denom=DENOM))#str(ctx.agent.address)


@reward.on_message(model=TransactionInfo)
async def confirm_transaction(ctx: Context, sender: str, msg: TransactionInfo):
    ctx.logger.info(f"Received transaction info from {sender}: {msg}")
    tx_resp = await wait_for_tx_to_complete(msg.tx_hash, ctx.ledger)
 
    coin_received = tx_resp.events["coin_received"]
    if (
            coin_received["receiver"] == str(reward.wallet.address())
            and coin_received["amount"] == f"{AMOUNT}{DENOM}"
    ):
        ctx.logger.info(f"Transaction was successful: {coin_received}")
    else:
        ctx.logger.info(f"Transaction was unsuccessful: {coin_received}")

    ledger: LedgerClient = get_ledger()
    agent_balance = ledger.query_bank_balance(Address(reward.wallet.address()))/1000000000000000000
    ctx.logger.info(f"Balance after fees: {agent_balance} TESTFET")

    #storage to verify for reward
    local_ledger = {"agent_address":sender, "tx":msg.tx_hash}
    ctx.storage.set("{ctx.agent.address}", local_ledger)#{ctx.agent.wallet.address()}
    
    await ctx.send(sender,PaymentReceived(status="success"))#str(ctx.agent.address)
    #ctx.logger.info(ctx.storage.get("Passkey"))
    stakystake() #stake received amount of funds


@reward.on_message(model=RewardRequest)
async def request_reward(ctx: Context, sender: str, msg: RewardRequest):
    fund_agent_if_low(reward.wallet.address(), min_balance=AMOUNT)
    check = ctx.storage.get("{ctx.agent.address}")
    if (check['agent_address'] == sender):
        await ctx.send(sender,PaymentRequest(wallet_address=str(reward.wallet.address()), amount=REWARD, denom=DENOM))#send the reward
        ctx.logger.info(f"Reward has been issued!")
        ctx.storage.remove("ctx.agent.address")#{ctx.agent.wallet.address()}
        ctx.logger.info(f"Reward storage cleared")
    else:
        ctx.logger.info(f"Transaction not found!")
    

def stakystake():
    ledger: LedgerClient = get_ledger()
    faucet: FaucetApi = get_faucet()
    #faucet.get_wealth(farmer.wallet.address())

    agent_balance = ledger.query_bank_balance(Address(reward.wallet.address()))
    converted_balance = agent_balance/1000000000000000000
    ctx.logger.info(f"Received: {converted_balance} TESTFET")
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
    agent_balance = agent_balance - 1000000000000000
    tx = ledger_client.delegate_tokens(validator.address, agent_balance, reward.wallet)
    tx.wait_to_complete()
    ctx.logger.info("Delegation completed.")
    summary = ledger_client.query_staking_summary(reward.wallet.address())
    totalstaked = summary.total_staked/1000000000000000000
    ctx.logger.info(f"Staked: {totalstaked} TESTFET")

 
if __name__ == "__main__":
    reward.run()
 
