#this agent receives funds from main, together with FET wallet, and stores it using storage. this would prove that transaction was made. i think.
#this agent receives request to get the reward. upon request it checks storage fet, and send the , confirms with given agent address and sends the reward. test tokens for now


from uagents import Agent, Bureau, Context, Model
from uagents.network import wait_for_tx_to_complete
from uagents.setup import fund_agent_if_low
 
class PaymentRequest(Model):
    wallet_address: str
    amount: int
    denom: str
 
class TransactionInfo(Model):
    tx_hash: str

class PaymentInquiry(Model):
    ready: str
    wallet: str #ctx.agent.wallet.address()


AMOUNT = 100
DENOM = "atestfet"
 
alice = Agent(name="alice", seed="numberonelkjfwepofkwpoekpoew", port=8001, endpoint=["http://127.0.0.1:8001/submit"])
reward = Agent(name="reward", seed="reward secret phrase agent oekwpfokw", port=8002, endpoint=["http://127.0.0.1:8002/submit"])
 
fund_agent_if_low(reward.wallet.address(), min_balance=AMOUNT)
 
@alice.on_interval(period=100000.0)
async def request_funds(ctx: Context):
    await ctx.send(bob.address,PaymentRequest(
            wallet_address=str(alice.wallet.address()), amount=AMOUNT, denom=DENOM),
    )
 
 
@alice.on_message(model=TransactionInfo)
async def confirm_transaction(ctx: Context, sender: str, msg: TransactionInfo):
    ctx.logger.info(f"Received transaction info from {sender}: {msg}")
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
    transaction = ctx.ledger.send_tokens(ctx.agent.wallet.address(), msg.amount, msg.denom,bob.wallet)
 
    # send the tx hash so alice can confirm
    await ctx.send(alice.address, TransactionInfo(tx_hash=transaction.tx_hash))
    
    
    
    
    
    
    
    
@reward.on_message(model=PaymentInquiry, replies=TransactionInfo)
async def send_payment(ctx: Context, sender: str, msg: PaymentRequest):
    ctx.logger.info(f"Received payment request from {sender}: {msg}")
 
    await ctx.send(sender,PaymentRequest(wallet_address=ctx.agent.wallet.address(), amount=AMOUNT, denom=DENOM))


@reward.on_message(model=TransactionInfo)
async def confirm_transaction(ctx: Context, sender: str, msg: TransactionInfo):
    ctx.logger.info(f"Received transaction info from {sender}: {msg}")
    tx_resp = await wait_for_tx_to_complete(msg.tx_hash, ctx.ledger)
 
    coin_received = tx_resp.events["coin_received"]
    if (
            coin_received["receiver"] == str(ctx.agent.wallet.address())
            and coin_received["amount"] == f"{AMOUNT}{DENOM}"
    ):
    ctx.logger.info(f"Transaction was successful: {coin_received}")
    
    local_ledger = {"agent_address":ctx.address, "tx":msg.tx_hash}
    ctx.storage.set("{ctx.agent.wallet.address()}", local_ledger)

    #ctx.logger.info(ctx.storage.get("Passkey"))


@reward.on_message(model=RewardRequest)
async def request_reward(ctx: Context, sender: str, msg: RewardRequest):
    ctx.logger.info(ctx.storage.get("{ctx.address}"))
    #now i need jsonify it?
    #what is the difference between ctx: Context and sender:str ; ctx.address?


 
bureau = Bureau()
bureau.add(reward)
bureau.add(bob)
 
if __name__ == "__main__":
    bureau.run()
 
