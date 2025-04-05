"""
Main orchestration agent for CryptoFund.
Coordinates data collection, analysis, and trading execution.
"""
import logging
import asyncio
import json
import os
from typing import Dict, Any, Optional
import time
from datetime import datetime

from uagents import Context

from cryptoreason.common.base_agent import BaseAgent
from cryptoreason.common.models import (
    Heartbeat, CoinRequest, CoinResponse, CryptonewsRequest, CryptonewsResponse,
    FGIRequest, FGIResponse, ASI1Request, ASI1Response, SwaplandRequest,
    SwaplandResponse, TopupRequest, TopupResponse, RewardRequest, SwapCompleted
)
from cryptoreason.common.config import Config
from cryptoreason.common.registry import registry
from cryptoreason.common.utils import AsyncEventHandler, load_json_file, save_json_file
from cryptoreason.common.errors import async_retry
from cryptoreason.api_server import APIServer

logger = logging.getLogger(__name__)


class MainAgent(BaseAgent):
    """
    Main orchestration agent that coordinates all other agents.
    """
    
    def __init__(self, port: int = 8017):
        """
        Initialize the main agent.
        
        Args:
            port: Port to run the agent on
        """
        super().__init__(
            name="CryptoFund Main Agent",
            port=port,
            seed="main_agent_secure_seed"
        )
        
        # Register with registry
        registry.register_agent("MAIN_AGENT", self.agent.address)
        
        # State management
        self.state = {
            "network": Config.DEFAULT_NETWORK,
            "risk_profile": Config.DEFAULT_RISK_PROFILE,
            "investor_type": Config.DEFAULT_INVESTOR_TYPE,
            "coin_data": {},
            "crypto_news": "",
            "fear_greed_index": "",
            "heartbeat_status": "unknown",
            "pending_transactions": [],
            "completed_transactions": []
        }
        
        # Register message handlers
        self.register_message_handler(Heartbeat, self.handle_heartbeat)
        self.register_message_handler(CoinResponse, self.handle_coin_response)
        self.register_message_handler(CryptonewsResponse, self.handle_news_response)
        self.register_message_handler(FGIResponse, self.handle_fgi_response)
        self.register_message_handler(ASI1Response, self.handle_asi_response)
        self.register_message_handler(SwaplandResponse, self.handle_swapland_response)
        self.register_message_handler(TopupResponse, self.handle_topup_response)
        self.register_message_handler(SwapCompleted, self.handle_swap_completed)
        
        # Register interval handlers
        self.register_interval_handler(24 * 60 * 60.0, self.daily_analysis)  # Once per day
        
        # Start API server in a separate thread
        self.api_server = APIServer()
        self.api_server.run(debug=False, use_thread=True)
        
        # Load state
        self._load_state()
    
    def _load_state(self) -> None:
        """Load agent state from file."""
        state_file = os.path.join(os.path.dirname(__file__), "data", "main_agent_state.json")
        
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(state_file), exist_ok=True)
            
            # Try to load state file
            if os.path.exists(state_file):
                loaded_state = load_json_file(state_file)
                if loaded_state:
                    self.state.update(loaded_state)
                    logger.info("Loaded agent state from file")
            else:
                logger.info("No existing state file found, using default state")
                # Save default state to create the file
                self._save_state()
        except Exception as e:
            logger.error(f"Error loading state: {e}")
            # Continue with default state
    
    def _save_state(self) -> None:
        """Save agent state to file."""
        state_file = os.path.join(os.path.dirname(__file__), "data", "main_agent_state.json")
        os.makedirs(os.path.dirname(state_file), exist_ok=True)
        
        try:
            save_json_file(state_file, self.state)
        except Exception as e:
            logger.error(f"Error saving state: {e}")
    
    async def on_startup(self, ctx: Context) -> None:
        """
        Custom startup handler.
        
        Args:
            ctx: Agent context
        """
        # Set up initial configuration (normally from user input)
        self.state["network"] = Config.DEFAULT_NETWORK
        self.state["risk_profile"] = Config.DEFAULT_RISK_PROFILE
        self.state["investor_type"] = Config.DEFAULT_INVESTOR_TYPE
        
        # Start initial data collection
        await self.collect_data(ctx)
    
    @async_retry(max_retries=3, delay=2)
    async def collect_data(self, ctx: Context) -> bool:
        """
        Collect data from various sources.
        
        Args:
            ctx: Agent context
            
        Returns:
            True if all data was collected successfully, False otherwise
        """
        logger.info("Starting data collection process")
        
        # Create event for tracking responses
        coin_event = "coin_response"
        news_event = "news_response"
        fgi_event = "fgi_response"
        
        self.event_handler.create_event(coin_event)
        self.event_handler.create_event(news_event)
        self.event_handler.create_event(fgi_event)
        
        # Get agent addresses
        coin_agent = registry.get_agent_address("COIN_AGENT")
        news_agent = registry.get_agent_address("CRYPTONEWS_AGENT")
        fgi_agent = registry.get_agent_address("FGI_AGENT")
        
        if not all([coin_agent, news_agent, fgi_agent]):
            logger.error("One or more required agents not registered")
            return False
        
        # Request market data
        await self.send_message(
            ctx,
            coin_agent,
            CoinRequest(blockchain=self.state["network"]),
            wait_for_response=True,
            response_timeout=30.0
        )
        
        # Request news data
        await self.send_message(
            ctx,
            news_agent,
            CryptonewsRequest(limit=3),
            wait_for_response=True,
            response_timeout=30.0
        )
        
        # Request Fear & Greed Index
        await self.send_message(
            ctx,
            fgi_agent,
            FGIRequest(limit=1),
            wait_for_response=True,
            response_timeout=30.0
        )
        
        # Wait for all responses or timeout
        all_collected = await asyncio.gather(
            self.event_handler.wait_for_event(coin_event, 30.0),
            self.event_handler.wait_for_event(news_event, 30.0),
            self.event_handler.wait_for_event(fgi_event, 30.0)
        )
        
        success = all(all_collected)
        if not success:
            logger.warning("Some data collection operations timed out")
        
        # Clear events for next collection
        self.event_handler.clear_all_events()
        
        return success
    
    async def analyze_data(self, ctx: Context) -> Optional[str]:
        """
        Analyze collected data using ASI1 agent.
        
        Args:
            ctx: Agent context
            
        Returns:
            Analysis result or None if analysis failed
        """
        # Check if we have all required data
        if not self.state["coin_data"] or not self.state["crypto_news"] or not self.state["fear_greed_index"]:
            logger.warning("Missing data for analysis")
            return None
        
        # Prepare query for ASI1 agent
        query = self._build_analysis_query()
        
        # Get ASI1 agent address
        asi_agent = registry.get_agent_address("REASON_AGENT")
        if not asi_agent:
            logger.error("ASI1 agent not registered")
            return None
        
        # Create event for tracking response
        asi_event = "asi_response"
        self.event_handler.create_event(asi_event)
        
        # Send request to ASI1 agent
        await self.send_message(
            ctx,
            asi_agent,
            ASI1Request(query=query),
            wait_for_response=True,
            response_timeout=60.0
        )
        
        # Wait for response
        if await self.event_handler.wait_for_event(asi_event, 60.0):
            # Access the response from state (set by the handler)
            return self.state.get("analysis_result")
        
        logger.warning("ASI1 analysis timed out")
        return None
    
    async def execute_trade(self, ctx: Context, signal: str) -> bool:
        """
        Execute a trade based on analysis signal.
        
        Args:
            ctx: Agent context
            signal: Trading signal ("buy" or "sell")
            
        Returns:
            True if trade was executed successfully, False otherwise
        """
        # First check heartbeat status
        if self.state["heartbeat_status"] != "continue":
            logger.warning("User heartbeat status prevents trading")
            return False
        
        # Get SwapFinder agent address
        swapfinder_agent = registry.get_agent_address("SWAPLAND_AGENT")
        if not swapfinder_agent:
            logger.error("SwapFinder agent not registered")
            return False
        
        # Create event for tracking response
        swap_event = "swap_response"
        self.event_handler.create_event(swap_event)
        
        # Send request to SwapFinder agent
        await self.send_message(
            ctx,
            swapfinder_agent,
            SwaplandRequest(
                blockchain=self.state["network"],
                signal=signal,
                amount=0.1,  # TODO: Make this configurable
                private_key=Config.METAMASK_PRIVATE_KEY
            ),
            wait_for_response=True,
            response_timeout=120.0
        )
        
        # Wait for response
        if await self.event_handler.wait_for_event(swap_event, 120.0):
            logger.info(f"Trade execution initiated for signal: {signal}")
            return True
        
        logger.warning("Trade execution timed out")
        return False
    
    def _build_analysis_query(self) -> str:
        """
        Build query for ASI1 agent.
        
        Returns:
            Formatted query string
        """
        # Format coin data
        coin_data = self.state["coin_data"]
        coin_str = (
            f"Coin: {coin_data.get('name', 'Unknown')} ({coin_data.get('symbol', '?')})\n"
            f"Price: ${coin_data.get('current_price', 0):.2f}\n"
            f"24h Change: {coin_data.get('price_change_24h', 0):.2f}%\n"
            f"Market Cap: ${coin_data.get('market_cap', 0):,.2f}\n"
            f"Trading Volume: ${coin_data.get('total_volume', 0):,.2f}\n"
        )
        
        # Build the complete query
        query = (
            f"Please analyze the following cryptocurrency data and provide a trading recommendation (buy/sell/hold):\n\n"
            f"MARKET DATA:\n{coin_str}\n"
            f"FEAR & GREED INDEX: {self.state['fear_greed_index']}\n\n"
            f"RECENT NEWS:\n{self.state['crypto_news']}\n\n"
            f"INVESTOR PROFILE:\n"
            f"Risk Tolerance: {self.state['risk_profile']}\n"
            f"Investment Style: {self.state['investor_type']}\n\n"
            f"Based on this data, should I buy, sell, or hold? Please start your response with SIGNAL: BUY, SIGNAL: SELL, or SIGNAL: HOLD."
        )
        
        return query
    
    ### MESSAGE HANDLERS ###
    
    async def handle_heartbeat(self, ctx: Context, sender: str, msg: Heartbeat) -> None:
        """
        Handle heartbeat status updates.
        
        Args:
            ctx: Agent context
            sender: Sender address
            msg: Heartbeat message
        """
        logger.info(f"Received heartbeat status: {msg.status}")
        self.state["heartbeat_status"] = msg.status
        self._save_state()
    
    async def handle_coin_response(self, ctx: Context, sender: str, msg: CoinResponse) -> None:
        """
        Handle coin data responses.
        
        Args:
            ctx: Agent context
            sender: Sender address
            msg: Coin response message
        """
        logger.info(f"Received coin data for {msg.name} ({msg.symbol})")
        
        # Store coin data
        self.state["coin_data"] = {
            "name": msg.name,
            "symbol": msg.symbol,
            "current_price": msg.current_price,
            "market_cap": msg.market_cap,
            "total_volume": msg.total_volume,
            "price_change_24h": msg.price_change_24h
        }
        
        # Update API server state
        self.api_server.update_market_data(self.state["coin_data"])
        
        # Save state
        self._save_state()
        
        # Set event to indicate response received
        self.event_handler.set_event("coin_response")
    
    async def handle_news_response(self, ctx: Context, sender: str, msg: CryptonewsResponse) -> None:
        """
        Handle crypto news responses.
        
        Args:
            ctx: Agent context
            sender: Sender address
            msg: Crypto news response message
        """
        logger.info("Received crypto news")
        
        # Store news data
        self.state["crypto_news"] = msg.cryptoupdates
        
        # Save state
        self._save_state()
        
        # Set event to indicate response received
        self.event_handler.set_event("news_response")
    
    async def handle_fgi_response(self, ctx: Context, sender: str, msg: FGIResponse) -> None:
        """
        Handle Fear & Greed Index responses.
        
        Args:
            ctx: Agent context
            sender: Sender address
            msg: FGI response message
        """
        logger.info(f"Received Fear & Greed Index: {msg.data[0].value_classification if msg.data else 'Unknown'}")
        
        # Store FGI data
        if msg.data:
            fgi_data = msg.data[0]
            self.state["fear_greed_index"] = (
                f"{fgi_data.value_classification} ({fgi_data.value})"
            )
        else:
            self.state["fear_greed_index"] = "Unknown"
        
        # Save state
        self._save_state()
        
        # Set event to indicate response received
        self.event_handler.set_event("fgi_response")
    
    async def handle_asi_response(self, ctx: Context, sender: str, msg: ASI1Response) -> None:
        """
        Handle ASI1 analysis responses.
        
        Args:
            ctx: Agent context
            sender: Sender address
            msg: ASI1 response message
        """
        logger.info("Received ASI1 analysis result")
        
        # Store analysis result
        self.state["analysis_result"] = msg.decision
        
        # Extract trading signal
        signal = self._extract_signal(msg.decision)
        if signal:
            self.state["last_signal"] = signal
            
            # If signal is buy or sell, execute trade
            if signal in ["BUY", "SELL"]:
                logger.info(f"Extracted trading signal: {signal}")
                self.state["pending_transactions"].append({
                    "timestamp": datetime.now().isoformat(),
                    "signal": signal,
                    "network": self.state["network"],
                    "status": "pending"
                })
                
                # Execute trade (but don't wait for completion here)
                asyncio.create_task(self.execute_trade(ctx, signal.lower()))
        
        # Save state
        self._save_state()
        
        # Set event to indicate response received
        self.event_handler.set_event("asi_response")
    
    async def handle_swapland_response(self, ctx: Context, sender: str, msg: SwaplandResponse) -> None:
        """
        Handle SwapFinder responses.
        
        Args:
            ctx: Agent context
            sender: Sender address
            msg: SwapFinder response message
        """
        logger.info(f"Received SwapFinder response: {msg.status}")
        
        # Update pending transaction status
        if self.state["pending_transactions"]:
            self.state["pending_transactions"][-1]["status"] = "in_progress"
        
        # Save state
        self._save_state()
        
        # Set event to indicate response received
        self.event_handler.set_event("swap_response")
    
    async def handle_topup_response(self, ctx: Context, sender: str, msg: TopupResponse) -> None:
        """
        Handle topup responses.
        
        Args:
            ctx: Agent context
            sender: Sender address
            msg: Topup response message
        """
        logger.info(f"Received topup response: {msg.status}")
    
    async def handle_swap_completed(self, ctx: Context, sender: str, msg: SwapCompleted) -> None:
        """
        Handle swap completion notifications.
        
        Args:
            ctx: Agent context
            sender: Sender address
            msg: Swap completed message
        """
        logger.info(f"Received swap completion: {msg.status}")
        
        # Update transaction status
        if self.state["pending_transactions"]:
            # Move from pending to completed
            transaction = self.state["pending_transactions"].pop(0)
            transaction["status"] = msg.status
            transaction["completion_time"] = datetime.now().isoformat()
            transaction["message"] = msg.message
            
            # Add to completed transactions
            self.state["completed_transactions"].append(transaction)
            
            # Update API server
            self.api_server.add_transaction(transaction)
        
        # Save state
        self._save_state()
    
    def _extract_signal(self, analysis: str) -> Optional[str]:
        """
        Extract trading signal from analysis result.
        
        Args:
            analysis: Analysis text
            
        Returns:
            Extracted signal (BUY, SELL, HOLD) or None if not found
        """
        analysis = analysis.upper()
        
        if "SIGNAL: BUY" in analysis:
            return "BUY"
        elif "SIGNAL: SELL" in analysis:
            return "SELL"
        elif "SIGNAL: HOLD" in analysis:
            return "HOLD"
        
        # Fallback to keyword matching
        if " BUY " in analysis or analysis.endswith(" BUY"):
            return "BUY"
        elif " SELL " in analysis or analysis.endswith(" SELL"):
            return "SELL"
        elif " HOLD " in analysis or analysis.endswith(" HOLD"):
            return "HOLD"
        
        return None
    
    ### SCHEDULED TASKS ###
    
    async def daily_analysis(self, ctx: Context) -> None:
        """
        Perform daily market analysis and trading.
        
        Args:
            ctx: Agent context
        """
        logger.info("Starting daily analysis")
        
        # First check heartbeat
        await self.send_message(
            ctx, 
            registry.get_agent_address("HEARTBEAT_AGENT"),
            Heartbeat(status="ready")
        )
        
        # Wait for heartbeat response
        await asyncio.sleep(15)
        
        # If heartbeat allows, proceed with analysis
        if self.state["heartbeat_status"] == "continue":
            # Collect data
            if await self.collect_data(ctx):
                # Analyze data
                analysis_result = await self.analyze_data(ctx)
                
                # If we have a result and a signal, execute trade
                if analysis_result and self.state.get("last_signal") in ["BUY", "SELL"]:
                    signal = self.state["last_signal"].lower()
                    await self.execute_trade(ctx, signal)
            else:
                logger.warning("Data collection failed, skipping analysis")
        else:
            logger.info("Trading paused due to heartbeat status")


# Initialize and run the agent if executed directly
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main_agent = MainAgent()
    main_agent.run() 