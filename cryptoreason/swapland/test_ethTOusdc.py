import datetime
import decimal
import sys
from decimal import Decimal

from threading import Thread
from flask import Flask, request, jsonify
from flask_cors import CORS
from uagents_core.crypto import Identity
from fetchai import fetch
from fetchai.registration import register_with_agentverse
from fetchai.communication import parse_message_from_agent, send_message_to_agent
import logging
import os
from dotenv import load_dotenv
from uagents import Model
#from fetchai.crypto import Identity
from uuid import uuid4
from llm_swapfinder import query_llm
 
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

flask_app = Flask(__name__)
CORS(flask_app)

# Initialising client identity to get registered on agentverse
client_identity = None


class SwaplandRequest(Model):
    blockchain: str
    signal: str
    amount: float

class SwaplandResponse(Model):
    status: str

# Load environment variables from .env file
load_dotenv()#this can be removed from here!


# Function to register agent
def init_client():
    """Initialize and register the client agent."""
    global client_identity
    try:
        # Load the agent secret key from environment variables
        client_identity = Identity.from_seed(("jedijidemphraifjowienowkewmmjnkjnnnkk"), 0)
        logger.info(f"Client agent started with address: {client_identity.address}")
        readme = """
![tag:swapland](https://img.shields.io/badge/swaplandbaseethusdc)

<description>Swapland agent which uses uniswapV2 smart contract to SELL ETH (swap ETH into USDC) on base network.</description>
<use_cases>
    <use_case>Receives a value for amount of ETH that needs to be swapped into USDC on base network.</use_case>
</use_cases>

<payload_requirements>
<description>Expects the float number which defines how many ETH needs to be converted into USDC.</description>
    <payload>
          <requirement>
              <parameter>amount</parameter>
              <description>Amount of ETH to be converted into USDC.</description>
          </requirement>
    </payload>
</payload_requirements>
"""

        
        # Register the agent with Agentverse
        register_with_agentverse(
            identity=client_identity,
            url="http://localhost:5002/api/webhook",
            agentverse_token=os.getenv("AGENTVERSE_API_KEY"),
            agent_title="Swapland ETH to USDC base agent",
            readme=readme
        )

        logger.info("Quickstart agent registration complete!")

    except Exception as e:
        logger.error(f"Initialization error: {e}")
        raise


#send to uAgent
@flask_app.route('/request', methods=['POST'])
def send_data():
    """Send payload to the selected agent based on provided address."""
    global agent_response
    agent_response = None



# app route to recieve the messages from other agents
@flask_app.route('/api/webhook', methods=['POST'])
def webhook():
    """Handle incoming messages"""
    global agent_response
    try:
        # Parse the incoming webhook message
        data = request.get_data().decode("utf-8")
        logger.info("Received response")

        message = parse_message_from_agent(data)
        agent_response = message.payload

        logger.info(f"Processed response: {agent_response}")
        #how do i parse respons into variables? blockchain, signal, amount
        send_data() #send response status
                
        return jsonify({"status": "success"})

    except Exception as e:
        logger.error(f"Error in webhook: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    load_dotenv()       # Load environment variables
    init_client()       #Register your agent on Agentverse
    #app.run(host="0.0.0.0", port=5002)
    Thread(target=lambda: flask_app.run(host="0.0.0.0", port=5002, debug=True, use_reloader=False)).start()
