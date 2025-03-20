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

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialising client identity to get registered on agentverse
client_identity = None
agent_response = None


class SwaplandRequest(Model):
    blockchain: str
    signal: str
    amount: float

class SwaplandResponse(Model):
    status: str

# Load environment variables from .env file
load_dotenv()


# Function to register agent
def init_client():
    """Initialize and register the client agent."""
    global client_identity
    try:
        # Load the agent secret key from environment variables
        client_identity = Identity.from_seed("jedijidemphraifjowienowkewmm"), 0)
        logger.info(f"Client agent started with address: {client_identity.address}")

        readme = """
            ![domain:innovation-lab](https://img.shields.io/badge/innovation--lab-3D8BD3)
            domain:domain-of-your-agent

            <description>This Agent can only receive a message from another agent in string format.</description>
            <use_cases>
                <use_case>To receive a message from another agent.</use_case>
            </use_cases>
            <payload_requirements>
            <description>This agent only requires a message in the text format.</description>
            <payload>
                <requirement>
                    <parameter>message</parameter>
                    <description>The agent can receive any kind of message.</description>
                </requirement>
            </payload>
            </payload_requirements>
        """
        

        # Register the agent with Agentverse
        register_with_agentverse(
            identity=client_identity,
            url="http://localhost:5002/api/webhook",
            agentverse_token=os.getenv("AGENTVERSE_API_KEY"),
            agent_title="Swapland finder agent",
            readme=readme
        )

        logger.info("Quickstart agent registration complete!")

    except Exception as e:
        logger.error(f"Initialization error: {e}")
        raise


#send to uAgent
@app.route('/request', methods=['POST'])
def send_data():
    """Send payload to the selected agent based on provided address."""
    global agent_response
    agent_response = None

    try:
        # Parse the request payload
        data = request.json
        payload = data.get('payload')  # Extract the payload dictionary

        uagent_address = "" #run the uagent.py copy the address and paste here
        
        # Build the Data Model digest for the Request model to ensure message format consistency between the uAgent and AI Agent
        model_digest = Model.build_schema_digest(SwaplandResponse)

        # Send the payload to the specified agent
        send_message_to_agent(
            client_identity,  # Frontend client identity
            uagent_address,  # Agent address where we have to send the data
            payload,  # Payload containing the data
            model_digest=model_digest
        )

        return jsonify({"status": "request_sent", "payload": payload})

    except Exception as e:
        logger.error(f"Error sending data to agent: {e}")
        return jsonify({"error": str(e)}), 500






# app route to recieve the messages from other agents
@app.route('/api/webhook', methods=['POST'])
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
        return jsonify({"status": "success"})

    except Exception as e:
        logger.error(f"Error in webhook: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    load_dotenv()       # Load environment variables
    init_client()       #Register your agent on Agentverse
    app.run(host="0.0.0.0", port=5002)
