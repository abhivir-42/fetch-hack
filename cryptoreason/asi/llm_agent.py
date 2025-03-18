import requests
import os
import logging
import sys
from uagents import Agent, Context, Model
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Retrieve the API key from environment variables
api_key = os.getenv("ASI1_API_KEY")

# ASI1-Mini LLM API endpoint
url = "https://api.asi1.ai/v1/chat/completions"

# Define headers for API requests, including authentication
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

agent = Agent(
    name="ASI1 Reasoning agent to sell/buy crypto",
    port=8018,
    seed="LOLOLO lets buy some crypto letsgo",
    mailbox = True,
    endpoint=["http://127.0.0.1:8018/submit"],
    )

class ASI1Request(Model):
    query: str
    
class ASI1Response(Model):
    decision: str
    
    
    
    
@agent.on_event("startup")
async def introduce_agent(ctx: Context):
    """Logs agent startup details."""
    logging.info(f"✅ Agent started: {ctx.agent.address}")
    print(f"Hello! I'm {agent.name} and my address is {agent.address}.")
    logging.info("🚀 Agent startup complete.")
    
    
@agent.on_message(model=ASI1Request)
async def handle_asi1_query(ctx: Context, sender: str, msg: ASI1Request):
    ctx.logger.info(f"📩 Received message from {sender}: Analysing crypto sentiment..")
    """
    Queries the ASI1-Mini LLM with a given prompt and returns the model's response.

    Parameters:
        query (str): The input question or statement for the language model.

    Returns:
        str: The response from the LLM.
    
    If an error occurs during the request, the function returns the exception object.
    """
    data = {
        "messages": [{"role": "user", "content": msg.query}],  # User input for the chat model
        "conversationId": None,  # No conversation history tracking
        "model": "asi1-mini"  # Specifies the model version to use
    }

    try:
        # Send a POST request to the LLM API with the input query
        with requests.post(url, headers=headers, json=data) as response:
            output = response.json()  # Parse the JSON response

            # Extract and return the generated message content
            sendresponse = output["choices"][0]["message"]["content"]
    
    except requests.exceptions.RequestException as e:
        # Handle and return any request-related exceptions (e.g., network errors)
        sendresponse = str(e)

    try:
        await ctx.send(sender, ASI1Response(decision=sendresponse))
    except Exception as e:
        logging.error(f"❌ Error sending ASI1Response: {e}")
    ctx.logger.info(f"✅ Decision sent back to sender: {sender}")
    
# Ensure the agent starts running
if __name__ == "__main__":
    try:
        agent.run()
    except Exception as e:
        logging.error(f"❌ Error starting the agent: {e}")
