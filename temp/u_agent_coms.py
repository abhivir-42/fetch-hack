from uagents import Agent, Context, Model

# Define the request model the uAgent will handle
class Request(Model):
    message: str

# Define the response model the uAgent will send back
class Response(Model):
    response: str

# Initialize the uAgent
uagent = Agent(
    name="Sample uAgent",
    port=8000,
    endpoint=["http://localhost:8000/submit"]
)

# Handle incoming messages with the Request model
@uagent.on_message(model=Request)
async def message_handler(ctx: Context, sender: str, msg: Request):
    ctx.logger.info(f"Received message from {sender}: {msg.message}")

    # Generate a response message
    response = Response(response=f'Hello, AI Agent! I received your message:{msg.message}')
    
    # Send the response back to the AI Agent
    await ctx.send(sender, response)

if __name__ == "__main__":
    uagent.run()
