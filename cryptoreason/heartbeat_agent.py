#heartbeat agent
from flask import Flask, request, jsonify
from flask_cors import CORS
#from uagents_core.crypto import Identity
from uagents_core.identity import Identity
from fetchai import fetch
from fetchai.registration import register_with_agentverse
from fetchai.communication import parse_message_from_agent, send_message_to_agent
import logging
import os
from dotenv import load_dotenv
from uagents import Model
from uuid import uuid4
import requests

import json
from datetime import datetime, timedelta, timezone  # Correct import

from swapland.llm_swapfinder import query_llm


app = Flask(__name__)
CORS(app)

json_file_path = "hb_data.json"

AGENTVERSE_API_KEY = os.getenv("AGENTVERSE_API_KEY")


class Heartbeat(Model):
    status: str
    

MAINAGENT="agent1qfrhxny23vz62v5tr20qnmnjujq8k5t0mxgwdxfap945922t9v4ugqtqkea"#"agent1qwgewx4cx37q2tthr5tw08xtn877knkdhptkhhpenfk7u02nd0rdgv90za9" #test
#"agent1qfrhxny23vz62v5tr20qnmnjujq8k5t0mxgwdxfap945922t9v4ugqtqkea"
        
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)



# Initialising client identity to get registered on agentverse
client_identity = None

#class HeartbeatRequest(Model):
#    status: str
    
    
# Function to register agent
def init_client():
    """Initialize and register the client agent."""
    global client_identity
    try:
        # Load the agent secret key from environment variables
        client_identity = Identity.from_seed(("jedijidemphraeyeyeye73782ifjowienowkewmmNewSeedNeeded13"), 0)
        logger.info(f"Client agent started with address: {client_identity.address}")

        readme = """
![tag:swapland](https://img.shields.io/badge/swapland--heartbeat)
![domain:innovation-lab](https://img.shields.io/badge/innovation--lab-3D8BD3)
![domain:swapland](https://img.shields.io/badge/swapland-03)

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
            url="http://localhost:8300/api/webhook",
            agentverse_token=os.getenv("AGENTVERSE_API_KEY"),
            agent_title="Heartbeat agent",
            readme=readme
        )

        logger.info("Quickstart agent registration complete!")


        #send_data()
        
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
        #data = request.json
        # Initialize the dictionary to store recent heart rate data
        datafromhb = {}

        # Read and load the JSON file
        with open(json_file_path, "r") as file:
            data = json.load(file)

        # Get current time (UTC assumed, since JSON uses 'Z' timestamps)
        current_time = datetime.now(timezone.utc)  # Correct usage
        two_hours_ago = current_time - timedelta(hours=10)

        # Filter entries from the past 2 hours
        for entry in data:
            entry_time = datetime.strptime(entry["dateTime"], "%Y-%m-%dT%H:%M:%S")
            entry_time = entry_time.replace(tzinfo=timezone.utc)
            if entry_time >= two_hours_ago:
                # Use dateTime as the key and store bpm/confidence as the value
                datafromhb[entry["dateTime"]] = {
                    "bpm": entry["value"]["bpm"],
                    "confidence": entry["value"]["confidence"]
                }

        # Print the resulting dictionary
        logger.info("Data from the past 2 hours:")
        logger.info(f"{datafromhb}")
        
        prompt = f'''
            Analyse the data which contains heart beat as "value" and its timestamp within past 2 hours. Evaluate if any value is greater than 100, then return "stop" if true. Otherwise, return "continue". Again, only return one word "stop" or "continue".
            
            This is the data provided: {datafromhb}
            '''
        logger.info("Request sent to ASI1 model..")
        response = query_llm(prompt)  # Query the AI for a decision
        logger.info(f"{response}")


        #send response back
        payload = {"status":response}#data.get('payload')  # Extract the payload dictionary
        uagent_address = MAINAGENT
        
        model_digest = Model.build_schema_digest(Heartbeat)

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

        requestcommand = message.payload['status']
        logger.info(f"Processed response: {requestcommand}")
        
        if (requestcommand == "ready"):
            send_data() #send response status
        else:
            logger.info(f"Did not receive ready status!")

                 
        return jsonify({"status": "success"})

    except Exception as e:
        logger.error(f"Error in webhook: {e}")
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    load_dotenv()       # Load environment variables
    init_client()       #Register your agent on Agentverse
    app.run(host="0.0.0.0", port=8300)

