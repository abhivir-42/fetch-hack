"""
SwapFinder agent for discovering and coordinating swap execution agents.
"""
import os
import logging
import asyncio
from typing import Optional, Dict, Any, List
from flask import Flask, request, jsonify
from flask_cors import CORS
from threading import Thread

from uagents_core.identity import Identity
from fetchai.registration import register_with_agentverse
from fetchai.communication import parse_message_from_agent, send_message_to_agent
from uagents import Model

from cryptoreason.common.config import Config
from cryptoreason.common.models import SwaplandRequest, SwaplandResponse
from cryptoreason.common.errors import retry, APIError
from cryptoreason.common.utils import make_api_request

logger = logging.getLogger(__name__)


class SwapFinder:
    """Agent for finding appropriate swap agents based on blockchain and token pairs."""
    
    def __init__(self,
                host: str = '127.0.0.1',
                port: int = 5008,
                webhook_url: str = None):
        """
        Initialize the SwapFinder agent.
        
        Args:
            host: Host to run the Flask server on
            port: Port to run the Flask server on
            webhook_url: URL for the webhook endpoint
        """
        self.host = host
        self.port = port
        self.webhook_url = webhook_url or f"http://{host}:{port}/api/webhook"
        
        # Initialize Flask app
        self.app = Flask(__name__)
        CORS(self.app)
        
        # Initialize client identity
        self.client_identity = None
        self.initialize_identity()
        
        # Transaction state
        self.current_transaction = {
            "amount": 0,
            "private_key": "",
            "blockchain": "",
            "signal": ""
        }
        
        # Register routes
        self.register_routes()
    
    def initialize_identity(self) -> None:
        """Initialize and register the client identity with Agentverse."""
        try:
            # Use the same seed as the original implementation for compatibility
            self.client_identity = Identity.from_seed("jedijidemphraeyeyeye73782ifjowienowkewmm", 0)
            logger.info(f"SwapFinder agent started with address: {self.client_identity.address}")
            
            # Define agent README
            readme = """
![tag:swapfinder](https://img.shields.io/badge/swapfinder-master)
![domain:innovation-lab](https://img.shields.io/badge/innovation--lab-3D8BD3)
![domain:swapland](https://img.shields.io/badge/swapland--master-00)

<description>This Agent discovers and coordinates with swap execution agents.</description>
<use_cases>
    <use_case>To find appropriate swap agents for specific blockchain networks and token pairs.</use_case>
    <use_case>To coordinate swap execution transactions.</use_case>
</use_cases>
<payload_requirements>
<description>This agent requires a SwaplandRequest message.</description>
<payload>
    <requirement>
        <parameter>blockchain</parameter>
        <description>The blockchain network for the swap.</description>
    </requirement>
    <requirement>
        <parameter>signal</parameter>
        <description>The swap direction (buy/sell).</description>
    </requirement>
    <requirement>
        <parameter>amount</parameter>
        <description>The amount to swap.</description>
    </requirement>
    <requirement>
        <parameter>private_key</parameter>
        <description>The private key for transaction signing.</description>
    </requirement>
</payload>
</payload_requirements>
"""
            
            # Register with Agentverse with the same URL as original
            register_with_agentverse(
                identity=self.client_identity,
                url="http://localhost:5008/api/webhook",
                agentverse_token=Config.AGENTVERSE_API_KEY,
                agent_title="Swapland finder agent",
                readme=readme
            )
            
            logger.info("SwapFinder agent registration complete!")
            
        except Exception as e:
            logger.error(f"Identity initialization error: {e}")
            raise
    
    def register_routes(self) -> None:
        """Register Flask routes."""
        
        @self.app.route('/request', methods=['POST'])
        def send_response():
            """Send response back to the original requester."""
            try:
                payload = {"status": "Successfully request sent to SwapFinder Agent!"}
                
                # Get the main agent address
                main_agent_address = Config.get_agent_address("MAIN_AGENT")
                if not main_agent_address:
                    logger.error("Main agent address not found in registry")
                    return jsonify({"error": "Main agent address not found"}), 500
                
                # Build message digest for consistent format
                model_digest = Model.build_schema_digest(SwaplandResponse)
                
                # Send message back to main agent
                send_message_to_agent(
                    self.client_identity,
                    main_agent_address,
                    payload,
                    model_digest=model_digest
                )
                
                return jsonify({"status": "request_sent", "payload": payload})
                
            except Exception as e:
                logger.error(f"Error sending response: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/webhook', methods=['POST'])
        def webhook():
            """Handle incoming webhook messages."""
            try:
                # Parse incoming message
                data = request.get_data().decode("utf-8")
                logger.info("Received webhook request")
                
                message = parse_message_from_agent(data)
                payload = message.payload
                
                # Store transaction details for processing
                self.current_transaction = {
                    "amount": payload.get('amount', 0),
                    "private_key": payload.get('private_key', ''),
                    "blockchain": payload.get('blockchain', ''),
                    "signal": payload.get('signal', '')
                }
                
                logger.info(f"Processing transaction: blockchain={self.current_transaction['blockchain']}, "
                           f"signal={self.current_transaction['signal']}")
                
                # Send initial response back
                send_response()
                
                # Find appropriate swap agent
                asyncio.run(self.find_and_call_swap_agent())
                
                return jsonify({"status": "success"})
                
            except Exception as e:
                logger.error(f"Error in webhook: {e}")
                return jsonify({"error": str(e)}), 500
    
    @retry(max_retries=3, delay=2)
    async def search_agents(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search for agents matching the query.
        
        Args:
            query: Search query (tag or text)
            limit: Maximum number of agents to return
            
        Returns:
            List of matching agents
        """
        api_url = "https://agentverse.ai/v1/search/agents"
        
        payload = {
            "search_text": query,
            "sort": "relevancy",
            "direction": "asc",
            "offset": 0,
            "limit": limit,
        }
        
        try:
            data = make_api_request(
                url=api_url,
                method="POST",
                data=payload,
                timeout=Config.API_TIMEOUT
            )
            
            return data.get("agents", [])
            
        except APIError as e:
            logger.error(f"Agent search failed: {e}")
            raise
    
    async def find_best_agent(self, agents: List[Dict[str, Any]], query: str) -> Optional[str]:
        """
        Find the best agent for a query from search results.
        
        Args:
            agents: List of agents from search_agents
            query: Original search query
            
        Returns:
            Best matching agent address or None if no suitable agent found
        """
        if not agents:
            logger.warning("No agents found in search results")
            return None
        
        # If only one agent, return it directly
        if len(agents) == 1:
            return agents[0].get("address")
        
        # Prepare prompt for ranking agents
        prompt = f"""
        I have searched for agents with the query: "{query}"

        These are the results (name, address, readme):
        """
        
        for i, agent in enumerate(agents):
            prompt += f"{i+1}. {agent.get('name')}, {agent.get('address')}\n"
            prompt += f"   Readme: {agent.get('readme', 'No readme provided')}\n\n"
        
        prompt += f"""
        Based on the query "{query}", which agent (just the number) is the most suitable?
        Respond with only a number between 1 and {len(agents)}.
        """
        
        try:
            # Use LLM to rank agents
            from cryptoreason.asi.llm_agent import ASI1Agent
            llm_agent = ASI1Agent()
            response = await llm_agent.query_llm(prompt)
            
            # Parse response to get agent index
            try:
                agent_index = int(response.strip()) - 1
                if 0 <= agent_index < len(agents):
                    return agents[agent_index].get("address")
            except (ValueError, IndexError):
                logger.error(f"Invalid agent index from LLM: {response}")
            
            # Fallback to first agent if parsing fails
            return agents[0].get("address")
            
        except Exception as e:
            logger.error(f"Error ranking agents: {e}")
            return agents[0].get("address") if agents else None
    
    async def call_swap_agent(self, agent_address: str) -> bool:
        """
        Call the selected swap agent to execute the transaction.
        
        Args:
            agent_address: Address of the swap agent
            
        Returns:
            True if call successful, False otherwise
        """
        try:
            # Prepare payload for swap agent - match original format
            payload = {
                "variable": "swapland something",
                "metamask_key": self.current_transaction["private_key"],
                "amount": self.current_transaction["amount"]
            }
            
            # Send message to swap agent
            send_message_to_agent(
                self.client_identity,
                agent_address,
                payload
            )
            
            logger.info(f"Transaction request sent to swap agent: {agent_address}")
            return True
            
        except Exception as e:
            logger.error(f"Error calling swap agent: {e}")
            return False
    
    async def find_and_call_swap_agent(self) -> None:
        """Find appropriate swap agent and call it to execute the transaction."""
        try:
            # Build search query based on transaction details
            blockchain = self.current_transaction["blockchain"]
            signal = self.current_transaction["signal"]
            
            search_query = f"tag:swapland{blockchain}{signal}"
            logger.info(f"Searching for agents with query: {search_query}")
            
            # Search for matching agents
            agents = await self.search_agents(search_query)
            
            if not agents:
                logger.warning(f"No swap agents found for query: {search_query}")
                return
            
            # Find the best matching agent
            best_agent = await self.find_best_agent(agents, search_query)
            
            if best_agent:
                # Call the selected agent
                await self.call_swap_agent(best_agent)
            else:
                logger.error("No suitable swap agent found")
                
        except Exception as e:
            logger.error(f"Error in find_and_call_swap_agent: {e}")
    
    def run(self) -> None:
        """Run the SwapFinder agent with Flask server."""
        try:
            logger.info(f"Starting SwapFinder agent on {self.host}:{self.port}")
            self.app.run(host=self.host, port=self.port)
            
        except Exception as e:
            logger.error(f"Error running SwapFinder agent: {e}")
            raise


# Initialize and run the agent if executed directly
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    swapfinder = SwapFinder()
    swapfinder.run() 