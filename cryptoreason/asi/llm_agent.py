"""
ASI1 reasoning agent for crypto trading decisions.
"""
import logging
import requests
from uagents import Context

from cryptoreason.common.base_agent import BaseAgent
from cryptoreason.common.models import ASI1Request, ASI1Response
from cryptoreason.common.config import Config
from cryptoreason.common.errors import APIError, retry

logger = logging.getLogger(__name__)


class ASI1Agent(BaseAgent):
    """
    ASI1 reasoning agent that analyzes market data and makes trading decisions.
    """
    
    def __init__(self):
        """Initialize the ASI1 reasoning agent."""
        super().__init__(
            name="ASI1 Reasoning Agent",
            port=8007,
            seed="crypto_reasoning_agent_seed",
        )
        
        # Register message handlers
        self.register_message_handler(ASI1Request, self.handle_asi1_query)
        
        # API endpoint for ASI1-Mini LLM
        self.api_url = "https://api.asi1.ai/v1/chat/completions"
        
        # API headers with authentication
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {Config.ASI1_API_KEY}"
        }
    
    @retry(max_retries=3, delay=1)
    async def query_llm(self, prompt: str) -> str:
        """
        Query the ASI1-Mini LLM with the given prompt.
        
        Args:
            prompt: Input prompt for the LLM
            
        Returns:
            LLM response
            
        Raises:
            APIError: If the API request fails
        """
        data = {
            "messages": [{"role": "user", "content": prompt}],
            "conversationId": None,
            "model": "asi1-mini"
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=data,
                timeout=Config.API_TIMEOUT
            )
            response.raise_for_status()
            
            output = response.json()
            logger.debug(f"LLM response: {output}")
            
            return output["choices"][0]["message"]["content"]
            
        except requests.exceptions.RequestException as e:
            logger.error(f"LLM API request failed: {e}")
            raise APIError(f"LLM API request failed: {e}")
    
    async def handle_asi1_query(self, ctx: Context, sender: str, msg: ASI1Request):
        """
        Handle ASI1 query requests.
        
        Args:
            ctx: Agent context
            sender: Sender address
            msg: ASI1 query message
        """
        ctx.logger.info(f"Received message from {sender}: Analysing crypto sentiment..")
        
        try:
            # Query the LLM with the provided prompt
            response = await self.query_llm(msg.query)
            
            # Send the response back to the sender
            await self.send_message(
                ctx,
                sender,
                ASI1Response(decision=response)
            )
            
            ctx.logger.info(f"Decision sent back to sender: {sender}")
            
        except Exception as e:
            logger.error(f"Error handling ASI1 query: {e}")
            
            # Send an error response
            error_msg = f"Error processing query: {str(e)}"
            await self.send_message(
                ctx,
                sender,
                ASI1Response(decision=error_msg)
            )


# Initialize and run the agent if executed directly
if __name__ == "__main__":
    agent = ASI1Agent()
    agent.run()
