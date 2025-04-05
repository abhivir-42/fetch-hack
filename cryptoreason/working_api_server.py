"""
Working REST API server for CryptoFund external interactions.
"""
import logging
import os
import json
import sys
from typing import Dict, Any, Optional
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import requests
import threading
import random
from datetime import datetime, timedelta
import time

# Add the project root to PYTHONPATH to fix imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now import from cryptoreason package
from cryptoreason.common.config import Config
from cryptoreason.common.registry import registry
from cryptoreason.common.errors import APIError, safe_execute

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class APIServer:
    """REST API server for CryptoFund external interactions."""
    
    def __init__(self, host: str = '0.0.0.0', port: int = 8000):
        """
        Initialize the API server.
        
        Args:
            host: Host to run the server on
            port: Port to run the server on (8000 to avoid macOS AirPlay conflict)
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
        try:
            # First try to get real agent data
            agent_dict = registry.list_registered_agents()
            agents = []
            
            for name, address in agent_dict.items():
                agents.append({
                    "id": name.lower().replace('_', '-'),
                    "name": " ".join(name.split('_')).title(),
                    "type": name.lower().replace('_', ''),
                    "description": f"Agent for {' '.join(name.split('_')).title()} operations",
                    "status": "online",
                    "lastActive": datetime.now().isoformat()
                })
            
            if agents:
                return agents
        except Exception as e:
            logger.warning(f"Could not get real agent data: {e}. Using mock data instead.")
        
        # Fallback to mock data
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
        """Generate market data, attempting to get real data from coin agent first."""
        try:
            # Try to get real data from coin agent first
            real_data = []
            cryptos = {
                "bitcoin": {"symbol": "BTC", "name": "Bitcoin", "mock_price": 66923.45},
                "ethereum": {"symbol": "ETH", "name": "Ethereum", "mock_price": 3217.82},
                "solana": {"symbol": "SOL", "name": "Solana", "mock_price": 144.56},
                "avalanche-2": {"symbol": "AVAX", "name": "Avalanche", "mock_price": 36.78}
            }
            
            # Try to get coin agent address
            coin_agent_address = None
            try:
                coin_agent_address = registry.get_agent_address("COIN_AGENT")
                logger.info(f"Found coin agent at: {coin_agent_address}")
            except Exception as e:
                logger.warning(f"Could not get coin agent address: {e}")
            
            # Try to fetch data from CoinGecko with rate limiting awareness
            for crypto_id, crypto_info in cryptos.items():
                logger.info(f"Fetching data for {crypto_id}")
                
                try:
                    # Use a custom user agent and include small delay
                    headers = {
                        'User-Agent': 'CryptoFund/1.0',
                    }
                    
                    # Make API call with longer timeout
                    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}?localization=false&tickers=false&community_data=false&developer_data=false"
                    response = requests.get(url, headers=headers, timeout=10)
                    
                    # Check for rate limiting
                    if response.status_code == 429:
                        logger.warning(f"Rate limited by CoinGecko API for {crypto_id}")
                        # Create simulated data based on the mock price, but with small variations
                        # to simulate real-time changes instead of static values
                        variation = random.uniform(-0.5, 0.5) / 100  # Small percentage variation
                        current_price = crypto_info["mock_price"] * (1 + variation)
                        
                        # Add simulated data
                        real_data.append({
                            "symbol": crypto_info["symbol"],
                            "name": crypto_info["name"],
                            "currentPrice": current_price,
                            "priceChange24h": current_price * random.uniform(-0.02, 0.03),
                            "priceChangePercentage24h": random.uniform(-2.5, 3.5),
                            "marketCap": current_price * random.uniform(10000000, 20000000000),
                            "volume": current_price * random.uniform(1000000, 5000000000),
                            "lastUpdated": datetime.now().isoformat()
                        })
                        logger.info(f"Added simulated data for {crypto_id} due to rate limiting")
                    else:
                        response.raise_for_status()
                        data = response.json()
                        
                        # Format data for our frontend
                        real_data.append({
                            "symbol": crypto_info["symbol"],
                            "name": crypto_info["name"],
                            "currentPrice": data['market_data']['current_price']['usd'],
                            "priceChange24h": data['market_data']['price_change_24h'],
                            "priceChangePercentage24h": data['market_data']['price_change_percentage_24h'],
                            "marketCap": data['market_data']['market_cap']['usd'],
                            "volume": data['market_data']['total_volume']['usd'],
                            "lastUpdated": datetime.now().isoformat()
                        })
                        
                        logger.info(f"Successfully fetched data for {crypto_id}")
                    
                    # Add a small delay to avoid rate limiting
                    time.sleep(0.5)
                    
                except Exception as e:
                    logger.error(f"Error fetching real data for {crypto_id}: {e}")
                    # Create simulated data
                    variation = random.uniform(-0.5, 0.5) / 100  # Small percentage variation
                    current_price = crypto_info["mock_price"] * (1 + variation)
                    
                    # Add simulated data
                    real_data.append({
                        "symbol": crypto_info["symbol"],
                        "name": crypto_info["name"],
                        "currentPrice": current_price,
                        "priceChange24h": current_price * random.uniform(-0.02, 0.03),
                        "priceChangePercentage24h": random.uniform(-2.5, 3.5),
                        "marketCap": current_price * random.uniform(10000000, 20000000000),
                        "volume": current_price * random.uniform(1000000, 5000000000),
                        "lastUpdated": datetime.now().isoformat()
                    })
                    logger.info(f"Added simulated data for {crypto_id} due to error")
            
            if real_data:
                logger.info(f"Returning market data for {len(real_data)} cryptocurrencies")
                return real_data
                
        except Exception as e:
            logger.error(f"Error fetching real market data: {e}")
        
        # Fallback to mock data with small random variations to simulate real-time changes
        logger.warning("Using mock market data with variations")
        
        # Get timestamp for consistent "random" values
        now = datetime.now()
        timestamp_seed = int(now.timestamp()) // 60  # Change every minute
        random.seed(timestamp_seed)
        
        mock_data = [
            {
                "symbol": "BTC",
                "name": "Bitcoin",
                "currentPrice": 66923.45 + random.uniform(-300, 300),
                "priceChange24h": 945.67 + random.uniform(-50, 50),
                "priceChangePercentage24h": 1.42 + random.uniform(-0.2, 0.2),
                "marketCap": 1337678900000 + random.uniform(-10000000000, 10000000000),
                "volume": 28765432100 + random.uniform(-1000000000, 1000000000),
                "lastUpdated": now.isoformat()
            },
            {
                "symbol": "ETH",
                "name": "Ethereum",
                "currentPrice": 3217.82 + random.uniform(-20, 20),
                "priceChange24h": 47.89 + random.uniform(-5, 5),
                "priceChangePercentage24h": 1.51 + random.uniform(-0.2, 0.2),
                "marketCap": 409876543200 + random.uniform(-1000000000, 1000000000),
                "volume": 11876543210 + random.uniform(-500000000, 500000000),
                "lastUpdated": now.isoformat()
            },
            {
                "symbol": "SOL",
                "name": "Solana",
                "currentPrice": 144.56 + random.uniform(-2, 2),
                "priceChange24h": -3.32 + random.uniform(-1, 1),
                "priceChangePercentage24h": -2.25 + random.uniform(-0.2, 0.2),
                "marketCap": 63345678900 + random.uniform(-500000000, 500000000),
                "volume": 4267890123 + random.uniform(-200000000, 200000000),
                "lastUpdated": now.isoformat()
            },
            {
                "symbol": "AVAX",
                "name": "Avalanche",
                "currentPrice": 36.78 + random.uniform(-0.5, 0.5),
                "priceChange24h": 0.47 + random.uniform(-0.1, 0.1),
                "priceChangePercentage24h": 1.28 + random.uniform(-0.2, 0.2),
                "marketCap": 13876543210 + random.uniform(-100000000, 100000000),
                "volume": 1134567890 + random.uniform(-50000000, 50000000),
                "lastUpdated": now.isoformat()
            }
        ]
        
        return mock_data

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
            # Refresh market data on each request to ensure it's current
            self.state["market_data"] = self._get_mock_market_data()
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
        
        @self.app.route('/api/trigger-analysis', methods=['POST'])
        def trigger_analysis() -> Response:
            """Trigger market analysis."""
            try:
                data = request.json or {}
                blockchain = data.get('blockchain', Config.DEFAULT_NETWORK)
                
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
                    "timestamp": data.get('timestamp', datetime.now().isoformat()),
                    "status": heartbeat_value.get('status', 'healthy'),
                    "response": {
                        "tradingEnabled": heartbeat_value.get('tradingEnabled', True),
                        "message": heartbeat_value.get('message', 'System operational')
                    }
                })
                
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
            return server_thread
        else:
            # Run directly
            self.app.run(host=self.host, port=self.port, debug=debug)


# Initialize and run the server if executed directly
if __name__ == "__main__":
    print("Starting CryptoFund API Server on port 8000...")
    server = APIServer()
    server.run(debug=True) 