from uagents import Agent, Bureau, Context, Model
from uagents.network import wait_for_tx_to_complete
from uagents.setup import fund_agent_if_low
 
class PaymentRequest(Model):
    wallet_address: str
    amount: int
    denom: str
 
class TransactionInfo(Model):
    tx_hash: str
 
AMOUNT = 100
DENOM = "atestfet"
 
alice = Agent(name="alice", seed="numberonelkjfwepofkwpoekpoew", port=8001, endpoint=["http://127.0.0.1:8001/submit"])
bob = Agent(name="bob", seed="bob secret phrase", port=8002, endpoint=["http://127.0.0.1:8002/submit"])
 
fund_agent_if_low(bob.wallet.address(), min_balance=AMOUNT)
 
@alice.on_interval(period=100000.0)
async def request_funds(ctx: Context):
    await ctx.send(bob.address,PaymentRequest(
            wallet_address=str(alice.wallet.address()), amount=AMOUNT, denom=DENOM),
    )
 
 
@alice.on_message(model=TransactionInfo)
async def confirm_transaction(ctx: Context, sender: str, msg: TransactionInfo):
    ctx.logger.info(f"Received transaction info from {sender}: {msg}")
    ctx.logger.info(f"Received transaction info from {ctx.address}: {msg}")
    tx_resp = await wait_for_tx_to_complete(msg.tx_hash, ctx.ledger)
 
    coin_received = tx_resp.events["coin_received"]
    if (
            coin_received["receiver"] == str(alice.wallet.address())
            and coin_received["amount"] == f"{AMOUNT}{DENOM}"
    ):
        ctx.logger.info(f"Transaction was successful: {coin_received}")
 
 
@bob.on_message(model=PaymentRequest, replies=TransactionInfo)
async def send_payment(ctx: Context, sender: str, msg: PaymentRequest):
    ctx.logger.info(f"Received payment request from {sender}: {msg}")

    # send the payment
    transaction = ctx.ledger.send_tokens(
        msg.wallet_address, msg.amount, msg.denom, bob.wallet
    )
 
    # send the tx hash so alice can confirm
    await ctx.send(alice.address, TransactionInfo(tx_hash=transaction.tx_hash))
 
bureau = Bureau()
bureau.add(alice)
bureau.add(bob)
 
if __name__ == "__main__":
    bureau.run()
 
