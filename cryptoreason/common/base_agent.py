"""
Base agent class with common functionality for all CryptoFund agents.
"""
import logging
import asyncio
import sys
import atexit
from typing import Optional, Dict, Any, List, Callable, Awaitable

from uagents import Agent, Context, Model
from uagents.network import get_ledger
from cosmpy.crypto.address import Address

from .config import Config
from .utils import AsyncEventHandler, send_message_with_retry

logger = logging.getLogger(__name__)


class BaseAgent:
    """Base class for all CryptoFund agents with common functionality."""
    
    def __init__(self, 
                 name: str, 
                 port: int, 
                 seed: str,
                 endpoints: Optional[List[str]] = None):
        """
        Initialize the base agent.
        
        Args:
            name: Agent name
            port: Port to run the agent on
            seed: Seed for agent identity
            endpoints: List of endpoints for the agent
        """
        self.name = name
        self.port = port
        
        # Configure endpoints
        if not endpoints:
            endpoints = [f"http://127.0.0.1:{port}/submit"]
            
        # Create the agent
        self.agent = Agent(
            name=name,
            port=port,
            seed=seed,
            endpoint=endpoints
        )
        
        # Set up event handler for async operations
        self.event_handler = AsyncEventHandler()
        
        # Set up exit handlers
        atexit.register(self._log_exit)
        sys.excepthook = self._handle_unexpected_exception
        
        # Register standard handlers
        self._register_handlers()
    
    def _register_handlers(self) -> None:
        """Register standard event handlers."""
        
        @self.agent.on_event("startup")
        async def on_startup(ctx: Context):
            """Handle agent startup."""
            logger.info(f"✅ Agent started: {ctx.agent.address}")
            ctx.logger.info(f"Agent {self.name} started with address {self.agent.address}")
            
            # Log wallet balance
            ledger = get_ledger()
            agent_balance = ledger.query_bank_balance(
                Address(self.agent.wallet.address())
            ) / Config.ONETESTFET
            
            ctx.logger.info(f"Agent balance: {agent_balance} TESTFET")
            
            # Call custom startup handler if defined
            if hasattr(self, "on_startup") and callable(self.on_startup):
                await self.on_startup(ctx)
    
    def _log_exit(self) -> None:
        """Log when the agent exits."""
        logger.info(f"Agent {self.name} terminated")
    
    def _handle_unexpected_exception(self, exc_type, exc_value, exc_traceback):
        """Handle unexpected exceptions."""
        logger.error(
            f"Uncaught exception in agent {self.name}:",
            exc_info=(exc_type, exc_value, exc_traceback)
        )
    
    def register_message_handler(self, 
                                model_class: type, 
                                handler: Callable[[Context, str, Any], Awaitable[None]]) -> None:
        """
        Register a message handler for a specific model.
        
        Args:
            model_class: The model class to handle
            handler: The handler function
        """
        self.agent.on_message(model=model_class)(handler)
    
    def register_interval_handler(self, 
                                 period: float, 
                                 handler: Callable[[Context], Awaitable[None]]) -> None:
        """
        Register a handler to run at regular intervals.
        
        Args:
            period: The interval period in seconds
            handler: The handler function
        """
        self.agent.on_interval(period=period)(handler)
    
    async def send_message(self, 
                          ctx: Context, 
                          target_address: str, 
                          message: Any, 
                          wait_for_response: bool = False,
                          response_timeout: Optional[float] = None) -> bool:
        """
        Send a message to another agent with retries.
        
        Args:
            ctx: Agent context
            target_address: Target agent address
            message: Message to send
            wait_for_response: Whether to wait for a response
            response_timeout: Timeout for response in seconds
            
        Returns:
            True if message was sent successfully, False otherwise
        """
        event_id = None
        
        if wait_for_response:
            # Use message type name as event ID
            event_id = f"response_{message.__class__.__name__}_{id(message)}"
            self.event_handler.create_event(event_id)
        
        return await send_message_with_retry(
            ctx, 
            target_address, 
            message,
            self.event_handler if wait_for_response else None,
            event_id,
            response_timeout
        )
    
    def run(self) -> None:
        """Run the agent."""
        try:
            self.agent.run()
        except Exception as e:
            logger.error(f"Error running agent {self.name}: {e}")
            raise 