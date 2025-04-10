#!/usr/bin/env python3
import os
import time
import asyncio
import logging
from uagents import Agent, Context, Model
from dotenv import load_dotenv
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Define the request model (from API wrapper to main agent)
class TradingRequest(Model):
    network: str
    investor_type: str
    risk_strategy: str
    reason: str
    timestamp: float
    request_id: str  # To track the request

# Define the response model (from main agent to API wrapper)
class TradingResponse(Model):
    action: str
    amount: float
    price: float
    details: str
    timestamp: float
    request_id: str  # To match the response with the request

# Store responses from the main agent
responses = {}

# Initialize API agent
api_agent = Agent(
    name="API Bridge Agent",
    port=8601,  # Different port than the main agent (8650)
    seed="api_bridge_agent_seed",
    endpoint=["http://127.0.0.1:8601/submit"],
)

# Queue for storing requests to be sent
api_agent._requests_to_send = []

# Main agent address
MAIN_AGENT = "agent1qfrhxny23vz62v5tr20qnmnjujq8k5t0mxgwdxfap945922t9v4ugqtqkea"

@api_agent.on_event("startup")
async def startup(ctx: Context):
    """Log agent startup details."""
    ctx.logger.info(f"API Bridge Agent started with address: {api_agent.address}")

@api_agent.on_message(model=TradingResponse)
async def handle_trading_response(ctx: Context, sender: str, msg: TradingResponse):
    """Handle response from the main agent"""
    ctx.logger.info(f"Received trading response from {sender}: {msg.action}")
    
    # Store the response for the API wrapper to retrieve
    responses[msg.request_id] = {
        "status": "success",
        "data": {
            "action": msg.action,
            "amount": msg.amount,
            "price": msg.price,
            "details": msg.details,
            "timestamp": msg.timestamp
        },
        "message": "Analysis complete. Recommendation generated."
    }

async def send_trading_request(request_data):
    """Send a trading request to the main agent"""
    request_id = str(time.time())
    
    # Create request message
    request = TradingRequest(
        network=request_data.get("network", "ethereum"),
        investor_type=request_data.get("investor_type", "speculative"),
        risk_strategy=request_data.get("risk_strategy", "balanced"),
        reason=request_data.get("reason", ""),
        timestamp=time.time(),
        request_id=request_id
    )
    
    # We can't directly access the agent's context outside of its handlers
    # Instead, we'll store the request and wait for the agent's update loop
    # to send it in the next cycle
    try:
        # Store the request for later sending
        api_agent._requests_to_send.append((MAIN_AGENT, request))
        logger.info(f"Queued trading request {request_id} to main agent")
        return request_id
    except Exception as e:
        logger.error(f"Error queuing trading request: {e}")
        return None

def get_response(request_id, timeout=10):
    """Get the response for a specific request ID"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        if request_id in responses:
            response = responses.pop(request_id)
            return response
        time.sleep(0.5)
    
    # If timeout reached, return fallback response
    return {
        "status": "error",
        "message": "Timeout waiting for main agent response"
    }

# Add a periodic handler to process queued requests
@api_agent.on_interval(period=1.0)  # Check every second
async def process_queued_requests(ctx: Context):
    """Process any queued requests."""
    # Process any pending requests
    if api_agent._requests_to_send:
        # Get the next request to send
        recipient, message = api_agent._requests_to_send.pop(0)
        try:
            # Send the request
            await ctx.send(recipient, message)
            ctx.logger.info(f"Sent request {message.request_id} to {recipient}")
        except Exception as e:
            ctx.logger.error(f"Error sending request: {e}")
            # Put the request back in the queue to retry
            api_agent._requests_to_send.append((recipient, message))

if __name__ == "__main__":
    api_agent.run() 