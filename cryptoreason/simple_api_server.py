"""
Simplified REST API server for CryptoFund external interactions.
"""
import logging
import os
import json
import sys
from typing import Dict, Any
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import threading
import random
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleAPIServer:
    """Simplified REST API server for CryptoFund external interactions."""
    
    def __init__(self, host: str = '0.0.0.0', port: int = 8000):
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
        
        # Current state
        self.state = {
            "agents": self._get_mock_agents(),
            "transactions": self._get_mock_transactions(),
            "market_data": self._get_mock_market_data(),
            "heartbeat_data": {
                "timestamp": datetime.now().isoformat(),
                "status": "healthy",
                "response": {
                    "tradingEnabled": True,
                    "message": "System operational"
                }
            }
        }
        
        # Register routes
        self.register_routes()
    
    def _get_mock_agents(self):
        """Generate mock agent data."""
        return [
            {
                "id": "main-agent",
                "name": "Main Agent",
                "type": "main",
                "description": "Coordinates all agent activities",
                "status": "online",
                "lastActive": datetime.now().isoformat()
            },
            {
                "id": "heartbeat-agent",
                "name": "Heartbeat Agent",
                "type": "heartbeat",
                "description": "Monitors system health",
                "status": "online",
                "lastActive": datetime.now().isoformat()
            },
            {
                "id": "swap-agent",
                "name": "Swap Agent",
                "type": "swap",
                "description": "Executes token swaps",
                "status": "online",
                "lastActive": (datetime.now() - timedelta(minutes=5)).isoformat()
            },
            {
                "id": "market-agent",
                "name": "Market Agent",
                "type": "market",
                "description": "Collects market data",
                "status": "online",
                "lastActive": (datetime.now() - timedelta(minutes=2)).isoformat()
            },
            {
                "id": "news-agent",
                "name": "News Agent",
                "type": "news",
                "description": "Aggregates crypto news",
                "status": "error",
                "lastActive": (datetime.now() - timedelta(minutes=30)).isoformat()
            },
            {
                "id": "analysis-agent",
                "name": "Analysis Agent",
                "type": "analysis",
                "description": "Provides market analysis",
                "status": "online",
                "lastActive": (datetime.now() - timedelta(minutes=10)).isoformat()
            },
            {
                "id": "topup-agent",
                "name": "Topup Agent",
                "type": "topup",
                "description": "Manages wallet topups",
                "status": "offline",
                "lastActive": (datetime.now() - timedelta(hours=1)).isoformat()
            }
        ]

    def _get_mock_market_data(self):
        """Generate mock market data."""
        return [
            {
                "symbol": "BTC",
                "name": "Bitcoin",
                "currentPrice": 67800.45,
                "priceChange24h": 1245.67,
                "priceChangePercentage24h": 1.92,
                "marketCap": 1345678900000,
                "volume": 28765432100,
                "lastUpdated": datetime.now().isoformat()
            },
            {
                "symbol": "ETH",
                "name": "Ethereum",
                "currentPrice": 3482.12,
                "priceChange24h": 67.89,
                "priceChangePercentage24h": 2.01,
                "marketCap": 419876543200,
                "volume": 12876543210,
                "lastUpdated": datetime.now().isoformat()
            },
            {
                "symbol": "SOL",
                "name": "Solana",
                "currentPrice": 142.78,
                "priceChange24h": -4.32,
                "priceChangePercentage24h": -2.85,
                "marketCap": 62345678900,
                "volume": 4567890123,
                "lastUpdated": datetime.now().isoformat()
            },
            {
                "symbol": "AVAX",
                "name": "Avalanche",
                "currentPrice": 35.92,
                "priceChange24h": 0.87,
                "priceChangePercentage24h": 2.48,
                "marketCap": 12876543210,
                "volume": 1234567890,
                "lastUpdated": datetime.now().isoformat()
            }
        ]

    def _get_mock_transactions(self):
        """Generate mock transactions."""
        return [
            {
                "id": "tx1",
                "type": "swap",
                "from": "ETH",
                "to": "BTC",
                "amount": 1.5,
                "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(),
                "status": "completed",
                "txHash": "0x" + "".join([random.choice("0123456789abcdef") for _ in range(40)])
            },
            {
                "id": "tx2",
                "type": "topup",
                "from": "USD",
                "to": "ETH",
                "amount": 1000,
                "timestamp": (datetime.now() - timedelta(days=1)).isoformat(),
                "status": "completed",
                "txHash": "0x" + "".join([random.choice("0123456789abcdef") for _ in range(40)])
            },
            {
                "id": "tx3",
                "type": "swap",
                "from": "SOL",
                "to": "ETH",
                "amount": 10,
                "timestamp": (datetime.now() - timedelta(days=2)).isoformat(),
                "status": "failed",
                "error": "Insufficient liquidity"
            }
        ]
    
    def register_routes(self) -> None:
        """Register API routes."""
        
        @self.app.route('/api/health', methods=['GET'])
        def health_check() -> Response:
            """Health check endpoint."""
            return jsonify({"status": "ok"})
        
        @self.app.route('/api/agents', methods=['GET'])
        def list_agents() -> Response:
            """List all registered agents."""
            return jsonify({"agents": self.state["agents"]})
        
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
        
        @self.app.route('/api/market/data', methods=['GET'])
        def get_market_coins() -> Response:
            """Get market data for coins."""
            return jsonify(self.state["market_data"])
        
        @self.app.route('/api/market/prices', methods=['GET'])
        def get_price_history() -> Response:
            """Get price history for a specific coin and timeframe."""
            symbol = request.args.get('symbol', 'BTC')
            timeframe = request.args.get('timeframe', '24h')
            
            # Generate mock price history
            now = datetime.now().timestamp() * 1000
            one_day_ms = 24 * 60 * 60 * 1000
            
            # Generate different starting prices based on symbol
            base_price = 0
            if symbol == 'BTC':
                base_price = 67000
            elif symbol == 'ETH':
                base_price = 3400
            elif symbol == 'SOL':
                base_price = 140
            else:
                base_price = 100
            
            # Generate data points
            points = 24
            if timeframe == '7d':
                points = 7 * 24
            elif timeframe == '30d':
                points = 30 * 24
                
            interval = one_day_ms / 24
            if timeframe != '24h':
                interval = one_day_ms
            
            data = []
            for i in range(points):
                timestamp = now - (points - i) * interval
                # Create somewhat realistic price movements
                random_change = (random.random() - 0.48) * (base_price * 0.02)
                base_price = base_price + random_change
                
                data.append({
                    "timestamp": int(timestamp),
                    "price": base_price
                })
            
            return jsonify(data)
        
        @self.app.route('/api/wallet/connect', methods=['POST'])
        def connect_wallet() -> Response:
            """Connect wallet endpoint."""
            data = request.json or {}
            network = data.get('network', 'ethereum')
            
            mock_address = '0x71C7656EC7ab88b098defB751B7401B5f6d8976F'
            
            return jsonify({
                "address": mock_address,
                "network": network,
                "isConnected": True
            })
        
        @self.app.route('/api/wallet/balance', methods=['GET'])
        def get_wallet_balance() -> Response:
            """Get wallet balance endpoint."""
            address = request.args.get('address', '')
            network = request.args.get('network', 'ethereum')
            
            return jsonify({
                "address": address,
                "balance": "1.245",
                "network": network
            })
        
        @self.app.route('/api/wallet/topup', methods=['POST'])
        def topup_wallet() -> Response:
            """Topup wallet endpoint."""
            data = request.json or {}
            
            return jsonify({
                "success": True,
                "txHash": '0x' + ''.join([random.choice('0123456789abcdef') for _ in range(40)])
            })
        
        @self.app.route('/api/wallet/disconnect', methods=['POST'])
        def disconnect_wallet() -> Response:
            """Disconnect wallet endpoint."""
            return jsonify({"success": True})
        
        @self.app.route('/api/auth/login', methods=['POST'])
        def login() -> Response:
            """Login endpoint."""
            data = request.json or {}
            email = data.get('email', '')
            password = data.get('password', '')
            
            # Mock login - accept any non-empty email/password
            if not email or not password:
                return jsonify({"error": "Invalid credentials"}), 401
            
            return jsonify({
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IlVzZXIiLCJpYXQiOjE1MTYyMzkwMjJ9",
                "user": {
                    "id": "user1",
                    "email": email,
                    "name": "Demo User"
                }
            })
    
    def run(self, debug: bool = False, use_thread: bool = False) -> None:
        """
        Run the API server.
        
        Args:
            debug: Whether to run in debug mode
            use_thread: Whether to run in a separate thread
        """
        if use_thread:
            # Run in a separate thread
            server_thread = threading.Thread(
                target=self.app.run,
                kwargs={"host": self.host, "port": self.port, "debug": debug}
            )
            server_thread.daemon = True
            server_thread.start()
            return server_thread
        else:
            # Run directly
            self.app.run(host=self.host, port=self.port, debug=debug)


# Initialize and run the server if executed directly
if __name__ == "__main__":
    server = SimpleAPIServer()
    server.run(debug=True) 