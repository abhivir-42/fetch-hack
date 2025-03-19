 
from uagents import Agent, Context, Model
 
 
class Message(Model):
    message: str
 
 
SEED_PHRASE = "put_your_seed_phrase_here_jfejejej"
 
# Now your agent is ready to join the agentverse!
agent = Agent(
    name="aliceeee",
    seed=SEED_PHRASE,
    port=8011,
    mailbox=True,
)
 
# Copy the address shown below
print(f"Your agent's address is: {agent.address}")
  
if __name__ == "__main__":
    agent.run()
