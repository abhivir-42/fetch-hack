#!/usr/bin/env python3
import socket
import time
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
#from fetchai.crypto import Identity
from uuid import uuid4
from llm_swapfinder import query_llm
import requests

import asyncio

 
#private_key = os.getenv("METAMASK_PRIVATE_KEY")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialising client identity to get registered on agentverse
client_identity = None

AMOUNT_TO_SWAP = 0
PRIVATE_KEY = ""

class SwaplandRequest(Model):
    blockchain: str
    signal: str
    amount: float
    private_key: str

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
        client_identity = Identity.from_seed(("jedijidemphraeyeyeye73782ifjowienowkewmm"), 0)
        logger.info(f"Client agent started with address: {client_identity.address}")

        readme = """
![tag:swapland](https://img.shields.io/badge/swapland-master)
![domain:innovation-lab](https://img.shields.io/badge/innovation--lab-3D8BD3)
![domain:swapland](https://img.shields.io/badge/swapland--master-00)

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
            url="http://localhost:5008/api/webhook",
            agentverse_token=os.getenv("AGENTVERSE_API_KEY"),
            agent_title="Swapland finder agent",
            readme=readme
        )

        logger.info("Quickstart agent registration complete!")
        
        #debug
        #asyncio.sleep(5)
        #search("tag:swaplandbaseethusdc") #test
        #call_swap("agent1qt40dnmucj0umdf5mryz6qgtmw4q0jrwlxu96h67ldfjgsvf5t9q2uch5hr", private_key)
        #usdcTOeth agent1qt40dnmucj0umdf5mryz6qgtmw4q0jrwlxu96h67ldfjgsvf5t9q2uch5hr
        #ethTOusdc agent1qgl5kptpr3x2t2fnuxnnyf5e8rum8n7u9ett0lv6pqd00k302d72gcygy32
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
        payload = {"status": "Successfully request sent to Swapland Agent!"}#data.get('payload')  # Extract the payload dictionary

        uagent_address = "agent1qfrhxny23vz62v5tr20qnmnjujq8k5t0mxgwdxfap945922t9v4ugqtqkea" #run the uagent.py copy the address and paste here
        
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

        global AMOUNT_TO_SWAP
        AMOUNT_TO_SWAP = message.payload['amount']
        
        global PRIVATE_KEY
        PRIVATE_KEY = message.payload['private_key']
        
        logger.info(f"Processed response: {agent_response}")
        #how do i parse respons into variables? blockchain, signal, amount
        send_data() #send response status
        
        signalsearch = message.payload['signal']
        
        search(signalsearch) #debug to be enabled
        
        return jsonify({"status": "success"})

    except Exception as e:
        logger.error(f"Error in webhook: {e}")
        return jsonify({"error": str(e)}), 500


def search(query):
    # Search for agents matching the query
    # API endpoint and payload
    api_url = "https://agentverse.ai/v1/search/agents"
    
    
    logger.info(f"Search text: {query}")
    payload = {
        "search_text": str(query),#'<query>', tag:{tagid} tag:swaplandbaseethusdc
        "sort": "relevancy",
        "direction": "asc",
        "offset": 0,
        "limit": 5,
    }

    # Make a POST request to the API
    discovery = requests.post(api_url, json=payload)

    # Check if the request was successful
    if discovery.status_code == 200:
        # Parse the JSON response
        data = discovery.json()
        agents = data.get("agents", [])
        logger.info("Formatted API Response:")
        
        prompt = f'''
        These are all agents found through the search agent function tagged as swapland.
        Each agent has 3 parameters to consider: name, address and readme. Evaluate them all.
        By analysing agents name in the list and find the most suitable one to match the user query: "{query}"
        
        You should output a single string with the Agent Address ONLY, which field can be found under the agent name.
        '''
        logger.info("Agents discovered..")
        for agent in agents:
            print("-" * 100)
            print("Agent Name:", agent.get("name"))
            print("Agent Address:", agent.get("address"))
            print("Readme:", agent.get("readme"))
            

            prompt += f'''
            Agent Name: {agent.get("name")}
            Agent Address: {agent.get("address")}
            Readme: {agent.get("readme")}
            {"-" * 50}
            '''
            #logger.info(f"{prompt}")

        #print(prompt)  # Debugging log
        logger.info("Request sent to ASI1 model to evaluate the list of discovered agents..")
        response = query_llm(prompt)  # Query the AI for a decision
                
        logger.info(f"{response}")

        call_swap(str(response), PRIVATE_KEY) # need to test this

        logger.info("Program completed")

    else:
        logger.info(f"Request failed with status code {response.status_code}")

    return {"status": "Agent searched"}



def call_swap(swapaddress : str, metamask_key : str):
   """Send payload to the selected agent based on provided address."""
   try:
       # Parse the request payload
       #AMOUNT_TO_SWAP = 0.0001
       payload = {
        "variable": "swapland something",#'<query>', tag:{tagid} tag:swaplandbaseethusdc
        "metamask_key": metamask_key,#metamask_key
        "amount": AMOUNT_TO_SWAP
        }
        

       agent_address = swapaddress
       logger.info(f"Sending payload to agent: {swapaddress}")

       # Send the payload to the specified agent
       send_message_to_agent(
           client_identity,  # Frontend client identity
           agent_address,    # Agent address where we have to send the data
           payload           # Payload containing the data
       )

   except Exception as e:
       logger.error(f"Error sending data to agent: {e}")
       return jsonify({"error": str(e)}), 500


# Simple agent that just listens on port 5008
def main():
    # Create a socket to listen on port 5008
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        # Bind to port 5008
        server_socket.bind(('localhost', 5008))
        server_socket.listen(5)
        print(f"Swapfinder agent listening on port 5008...")
        
        # Keep the agent running
        while True:
            time.sleep(10)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    load_dotenv()       # Load environment variables
    init_client()       #Register your agent on Agentverse
    main()
