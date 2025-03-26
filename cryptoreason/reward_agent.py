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
 #ctx.agent.wallet.address()


AMOUNT = 100
DENOM = "atestfet"
 
reward = Agent(name="reward", seed="reward secret phrase agent oekwpfokw", port=8008, endpoint=["http://127.0.0.1:8008/submit"])
 
fund_agent_if_low(reward.wallet.address(), min_balance=AMOUNT)
 
 
@reward.on_message(model=PaymentInquiry)
async def send_payment(ctx: Context, sender: str, msg: PaymentRequest):
    ctx.logger.info(f"Received payment request from {sender}: {msg}")
    if(msg.ready == "ready"):
        await ctx.send(bob.address,PaymentRequest(wallet_address=str(reward.wallet.address()), amount=AMOUNT, denom=DENOM),)


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
    
    #storage to verify for reward
    local_ledger = {"agent_address":ctx.address, "tx":msg.tx_hash}
    ctx.storage.set("{ctx.agent.wallet.address()}", local_ledger)
    
    #ctx.logger.info(ctx.storage.get("Passkey"))
    

@reward.on_message(model=RewardRequest)
async def request_reward(ctx: Context, sender: str, msg: RewardRequest):
    ctx.logger.info(ctx.storage.get("{ctx.address}"))
    #now i need jsonify it?
    #what is the difference between ctx: Context and sender:str ; ctx.address?

 
if __name__ == "__main__":
    reward.run()
 
