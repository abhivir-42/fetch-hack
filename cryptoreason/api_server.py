"""
REST API server for CryptoFund external interactions.
"""
import logging
import os
import json
from typing import Dict, Any, Optional
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import requests
import threading

from common.config import Config
from common.registry import registry
from common.errors import APIError, safe_execute

logger = logging.getLogger(__name__)


class APIServer:
    """REST API server for CryptoFund external interactions."""
    
    def __init__(self, host: str = '127.0.0.1', port: int = 5000):
        """
        Initialize the API server.
        
        Args:
            host: Host to run the server on
            port: Port to run the server on
        """
        self.host = host
        self.port = port
        
        # Initialize Flask app
        self.app = Flask(__name__)
        CORS(self.app)
        
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        
        # Current state
        self.state = {
            "agents": {},
            "transactions": [],
            "market_data": {},
            "heartbeat_data": {}
        }
        
        # Register routes
        self.register_routes()
    
    def register_routes(self) -> None:
        """Register API routes."""
        
        @self.app.route('/api/health', methods=['GET'])
        def health_check() -> Response:
            """Health check endpoint."""
            return jsonify({"status": "ok"})
        
        @self.app.route('/api/agents', methods=['GET'])
        def list_agents() -> Response:
            """List all registered agents."""
            agents = registry.list_registered_agents()
            return jsonify({"agents": agents})
        
        @self.app.route('/api/market-data', methods=['GET'])
        def get_market_data() -> Response:
            """Get latest market data."""
            return jsonify({"market_data": self.state["market_data"]})
        
        @self.app.route('/api/transactions', methods=['GET'])
        def get_transactions() -> Response:
            """Get transaction history."""
            return jsonify({"transactions": self.state["transactions"]})
        
        @self.app.route('/api/heartbeat', methods=['GET'])
        def get_heartbeat() -> Response:
            """Get heartbeat data."""
            return jsonify({"heartbeat": self.state["heartbeat_data"]})
        
        @self.app.route('/api/trigger-analysis', methods=['POST'])
        def trigger_analysis() -> Response:
            """Trigger market analysis."""
            try:
                data = request.json or {}
                blockchain = data.get('blockchain', Config.DEFAULT_NETWORK)
                
                # Forward request to main agent
                main_agent_address = registry.get_agent_address("MAIN_AGENT")
                if not main_agent_address:
                    return jsonify({"error": "Main agent not registered"}), 500
                
                # TODO: Implement actual triggering of analysis
                # This would involve sending a message to the main agent
                
                return jsonify({
                    "status": "analysis_triggered",
                    "blockchain": blockchain
                })
                
            except Exception as e:
                logger.error(f"Error triggering analysis: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/update-heartbeat', methods=['POST'])
        def update_heartbeat() -> Response:
            """Update heartbeat data."""
            try:
                data = request.json or {}
                heartbeat_value = data.get('value')
                
                if heartbeat_value is None:
                    return jsonify({"error": "Missing heartbeat value"}), 400
                
                # Update state
                self.state["heartbeat_data"].update({
                    "timestamp": data.get('timestamp', ''),
                    "value": heartbeat_value
                })
                
                # TODO: Forward to heartbeat agent
                
                return jsonify({"status": "heartbeat_updated"})
                
            except Exception as e:
                logger.error(f"Error updating heartbeat: {e}")
                return jsonify({"error": str(e)}), 500
    
    @safe_execute(default_value={})
    def load_state(self) -> Dict[str, Any]:
        """
        Load server state from file.
        
        Returns:
            Loaded state dictionary
        """
        state_file = os.path.join(os.path.dirname(__file__), "data", "api_state.json")
        
        try:
            with open(state_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    @safe_execute()
    def save_state(self) -> None:
        """Save server state to file."""
        state_file = os.path.join(os.path.dirname(__file__), "data", "api_state.json")
        os.makedirs(os.path.dirname(state_file), exist_ok=True)
        
        with open(state_file, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def update_market_data(self, market_data: Dict[str, Any]) -> None:
        """
        Update market data state.
        
        Args:
            market_data: New market data
        """
        self.state["market_data"] = market_data
        self.save_state()
    
    def add_transaction(self, transaction: Dict[str, Any]) -> None:
        """
        Add transaction to history.
        
        Args:
            transaction: Transaction details
        """
        self.state["transactions"].append(transaction)
        
        # Limit transaction history size
        if len(self.state["transactions"]) > 100:
            self.state["transactions"] = self.state["transactions"][-100:]
        
        self.save_state()
    
    def run(self, debug: bool = False, use_thread: bool = False) -> None:
        """
        Run the API server.
        
        Args:
            debug: Whether to run in debug mode
            use_thread: Whether to run in a separate thread
        """
        # Load state
        saved_state = self.load_state()
        if saved_state:
            self.state.update(saved_state)
        
        if use_thread:
            # Run in a separate thread
            server_thread = threading.Thread(
                target=self.app.run,
                kwargs={"host": self.host, "port": self.port, "debug": debug}
            )
            server_thread.daemon = True
            server_thread.start()
        else:
            # Run directly
            self.app.run(host=self.host, port=self.port, debug=debug)


# Initialize and run the server if executed directly
if __name__ == "__main__":
    server = APIServer()
    server.run(debug=True) 