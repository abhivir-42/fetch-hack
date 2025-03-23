from uagents import Agent, Context
import cosmpy
 
from cosmpy.aerial.client import LedgerClient, NetworkConfig
 
agent = Agent(name="alice", seed="ifwoijeiofjeowijfoiewjoifjweoifjoiefjoiewojoi", port=8001,  endpoint=["http://localhost:8001/submit"])
 
@agent.on_event("startup")
async def introduce_agent(ctx: Context):
    ctx.logger.info(f"ASI wallet address:{agent.wallet.address()}")
    ctx.logger.info(f"ASI network address:{agent.address}")
    ledger_client = LedgerClient(NetworkConfig.fetch_mainnet())
    address: str = agent.wallet.address()
    balances = ledger_client.query_bank_all_balances(address)
    ctx.logger.info(f"Balance of addr: {balances}")
    
 
if __name__ == "__main__":
    agent.run()
 
