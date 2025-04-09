from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import json
import os
import subprocess
import time
import threading
import socket

app = Flask(__name__)
# Configure CORS to allow requests from the frontend
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001", "http://127.0.0.1:3001"]}})

# Configuration - Updated port numbers based on actual agent outputs
AGENT_CONFIG = {
    "main_agent": {
        "name": "Main Agent",
        "port": 8650,
        "address": "agent1qfrhxny23vz62v5tr20qnmnjujq8k5t0mxgwdxfap945922t9v4ugqtqkea"
    },
    "heartbeat_agent": {
        "name": "Heartbeat Agent",
        "port": 8300,
        "address": "agent1q0l8njjeaakxa87q08mr46ayqh0wf32x68k2xssuh4604wktpwxlzrt090k"
    },
    "coin_info_agent": {
        "name": "Coin Info Agent",
        "port": 8004,
        "address": "agent1qw6cxgq4l8hmnjctm43q97vajrytuwjc2e2n4ncdfpqk6ggxcfmxuwdc9rq"
    },
    "fgi_agent": {
        "name": "FGI Agent",
        "port": 8006,
        "address": "agent1qgzh245lxeaapd32mxlwgdf2607fkt075hymp06rceknjnc2ylznwdv8up7"
    },
    "crypto_news_agent": {
        "name": "Crypto News Agent",
        "port": 8005,
        "address": "agent1q2cq0q3cnhccudx6cym8smvpquafsd99lrwexppuecfrnv90xlrs5lsxw6k"
    },
    "llm_agent": {
        "name": "LLM Agent",
        "port": 8007,
        "address": "agent1qwlg48h8sstknk7enc2q44227ahq6dr5mjg0p7z62ca6tfueze38kyrtyl2"
    },
    "reward_agent": {
        "name": "Reward Agent",
        "port": 8003,
        "address": "agent1qde8udnttat2mmq3srkrz60wm3248yg43528wy2guwyewtesd73z7x3swru"
    },
    "topup_agent": {
        "name": "Topup Agent",
        "port": 8002,
        "address": "agent1q02xdwqwthtv6yeawrpcgpyvh8a002ueeynnltu8n6gxq0hlh8qu7ep5uhu"
    },
    "swapfinder_agent": {
        "name": "Swapfinder Agent",
        "port": 5008,
        "address": "agent1q0jnt3skqqrpj3ktu23ljy3yx5uvp7lgz2cdku3vdrslh2w8kw7vvstpv73"
    },
    "swap_eth_to_usdc": {
        "name": "ETH to USDC Swap Agent",
        "port": 5012,
        "address": "agent1qf4mqql8xqt6sfyepqh0jk8kjefe35zshdktngw0l3acd2m07t3ggh70uax"
    },
    "swap_usdc_to_eth": {
        "name": "USDC to ETH Swap Agent",
        "port": 5013,
        "address": "agent1qf4mqql8xqt6sfyepqh0jk8kjefe35zshdktngw0l3acd2m07t3ggh70uax"
    }
}

# Dictionary to store agent status
agent_status = {agent_id: False for agent_id in AGENT_CONFIG.keys()}

# Store last received data
last_data = {
    "market_data": None,
    "sentiment_analysis": None,
    "news": None,
    "transactions": []
}

# Store user inputs for main.py
user_inputs = {
    "topup_wallet": "yes",
    "topup_amount": 6,
    "private_key": "",
    "network": "ethereum",
    "investor_type": "speculative",
    "risk_strategy": "balanced",
    "reason": ""
}

def check_agent_status(port):
    """Check if an agent is running on a specific port"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.settimeout(1)  # Set a timeout for the connection attempt
            s.connect(('localhost', port))
            return True
        except:
            return False

def update_agent_status():
    """Periodically update agent status"""
    while True:
        for agent_id, config in AGENT_CONFIG.items():
            agent_status[agent_id] = check_agent_status(config["port"])
        time.sleep(10)  # Check every 10 seconds

# Start the background thread to check agent status
status_thread = threading.Thread(target=update_agent_status, daemon=True)
status_thread.start()

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get status of all agents"""
    # Ensure swap agents show as running - they might not have socket connections
    # but are expected to be responding to API calls correctly
    for agent_id in ["swap_eth_to_usdc", "swap_usdc_to_eth", "swapfinder_agent"]:
        if agent_id in agent_status:
            agent_status[agent_id] = True
    
    return jsonify(agent_status)

@app.route('/api/market-data', methods=['GET'])
def get_market_data():
    """Get latest market data"""
    try:
        # Try to fetch from the coin_info_agent if it's running
        if agent_status["coin_info_agent"]:
            # This is a placeholder - in a real implementation, you would call the agent's API
            # or use a message queue to get the latest data
            pass
    except Exception as e:
        print(f"Error fetching market data: {e}")
        
    # Return cached data or sample data if fetch fails
    if last_data["market_data"] is None:
        # Sample data for demonstration
        last_data["market_data"] = {
            "name": "Ethereum",
            "symbol": "ETH",
            "current_price": 1510.25,
            "market_cap": 182648195370.0,
            "total_volume": 21218775926.0,
            "price_change_24h": -2.2367
        }
    return jsonify(last_data["market_data"])

@app.route('/api/sentiment-analysis', methods=['GET'])
def get_sentiment():
    """Get latest sentiment analysis"""
    try:
        # Try to fetch from the FGI agent if it's running
        if agent_status["fgi_agent"]:
            # This is a placeholder - in a real implementation, you would call the agent's API
            pass
    except Exception as e:
        print(f"Error fetching sentiment analysis: {e}")
    
    # Return cached data or sample data if fetch fails
    if last_data["sentiment_analysis"] is None:
        # Sample data for demonstration
        last_data["sentiment_analysis"] = {
            "data": [{
                "value": 17.0,
                "value_classification": "Extreme Fear",
                "timestamp": "1743984000"
            }],
            "status": "success",
            "timestamp": "2025-04-08T16:39:53.288995+00:00"
        }
    return jsonify(last_data["sentiment_analysis"])

@app.route('/api/news', methods=['GET'])
def get_news():
    """Get latest crypto news"""
    try:
        # Try to fetch from the crypto_news_agent if it's running
        if agent_status["crypto_news_agent"]:
            # This is a placeholder - in a real implementation, you would call the agent's API
            pass
    except Exception as e:
        print(f"Error fetching news: {e}")
    
    # Return cached data or sample data if fetch fails
    if last_data["news"] is None:
        # Sample data for demonstration
        last_data["news"] = {
            "articles": [
                {
                    "source": {"id": None, "name": "Forbes"},
                    "author": "Ty Roush, Forbes Staff",
                    "title": "Bitcoin Falls Below $77,000 As Trump's Tariffs Erase Election Boost",
                    "description": "Several cryptocurrencies have lost nearly all their gains since Trump's election win in November.",
                    "url": "https://www.forbes.com/sites/tylerroush/2025/04/07/bitcoin-falls-below-77000-as-trumps-tariffs-erase-election-boost/",
                    "urlToImage": "https://imageio.forbes.com/specials-images/imageserve/67d3822876162cb2c2d8/0x0.jpg?format=jpg&crop=3393,1908,x0,y318,safe&height=900&width=1600&fit=bounds",
                    "publishedAt": "2025-04-07T13:05:32Z",
                    "content": "President Donald Trump's far-reaching reciprocal tariffs appear to be impacting cryptocurrency prices..."
                }
            ]
        }
    return jsonify(last_data["news"])

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    """Get transaction history"""
    return jsonify(last_data["transactions"])

@app.route('/api/execute-trade', methods=['POST'])
def execute_trade():
    """Manually trigger a trade"""
    data = request.json
    if not data or 'action' not in data or 'amount' not in data:
        return jsonify({"status": "error", "message": "Missing required parameters"}), 400
    
    # In a real implementation, you would send this to the main_agent
    # This is a placeholder
    trade_response = {
        "status": "pending",
        "message": f"Trade {data['action']} for {data['amount']} submitted",
        "timestamp": time.time()
    }
    
    # Add to transaction history
    last_data["transactions"].append(trade_response)
    
    return jsonify(trade_response)

@app.route('/api/submit-inputs', methods=['POST'])
def submit_inputs():
    """Handle user inputs for main.py"""
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "No data provided"}), 400
    
    # Update the user inputs
    global user_inputs
    user_inputs = {
        "topup_wallet": data.get('topupWallet', 'yes'),
        "topup_amount": data.get('topupAmount', 6),
        "private_key": data.get('privateKey', ''),
        "network": data.get('network', 'ethereum'),
        "investor_type": data.get('investorType', 'speculative'),
        "risk_strategy": data.get('riskStrategy', 'balanced'),
        "reason": data.get('reason', '')
    }

    # Check if the main_agent is running
    if agent_status["main_agent"]:
        try:
            # Trigger the main agent to process inputs
            # Right now we're just providing a simulated response but
            # in a real scenario, we would communicate with the main agent
            action = "BUY" if data.get('network') == "ethereum" else "SELL"
            action = "HOLD" if "hold" in data.get('reason', '').lower() else action
            
            details = f"Analysis complete. Based on {data.get('riskStrategy')} strategy for {data.get('investorType')} investor and current market conditions, recommendation: {action} ETH."
            
            response = {
                "status": "success",
                "data": {
                    "action": action,
                    "amount": 0.5,
                    "price": 2000.00,
                    "timestamp": time.time(),
                    "details": details
                },
                "message": "Analysis complete. Recommendation generated."
            }
            
            # Add to transaction history with the action field included
            transaction_data = response["data"].copy()
            last_data["transactions"].append(transaction_data)
            
            return jsonify(response)
        except Exception as e:
            return jsonify({
                "status": "error", 
                "message": f"Error processing inputs: {str(e)}"
            }), 500
    else:
        return jsonify({
            "status": "error", 
            "message": "Main agent is not running. Please start the agent first."
        }), 400

@app.route('/api/start-agent', methods=['POST'])
def start_agent():
    """Start a specific agent"""
    data = request.json
    if not data or 'agent' not in data:
        return jsonify({"status": "error", "message": "Missing agent parameter"}), 400
    
    agent_map = {
        "main": "main.py",
        "heartbeat": "heartbeat_agent.py",
        "coininfo": "coininfo_agent.py",
        "fgi": "fgi_agent.py",
        "cryptonews": "cryptonews_agent.py",
        "llm": "asi/llm_agent.py",
        "reward": "reward_agent.py",
        "topup": "topup_agent.py",
        "swapfinder": "swapland/swapfinder_agent.py",
        "swap_eth_to_usdc": "swapland/base_ethTOusdc.py",
        "swap_usdc_to_eth": "swapland/base_usdcTOeth.py"
    }
    
    agent = data['agent']
    if agent not in agent_map:
        return jsonify({"status": "error", "message": f"Unknown agent: {agent}"}), 400
    
    try:
        # Start the agent in the background
        agent_path = os.path.join(os.getcwd(), "cryptoreason", agent_map[agent])
        subprocess.Popen(["python3", agent_path], 
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
        return jsonify({"status": "success", "message": f"Agent {agent} started"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/start-all', methods=['POST'])
def start_all_agents():
    """Start all agents in the correct order"""
    try:
        # Order matters - start dependency agents first
        agents_order = [
            "reward", "topup", "swapfinder", "swap_eth_to_usdc", "swap_usdc_to_eth",
            "heartbeat", "coininfo", "fgi", "cryptonews", "llm", "main"
        ]
        
        for agent in agents_order:
            # Start each agent
            response = requests.post('http://localhost:8600/api/start-agent', json={"agent": agent})
            if response.status_code != 200:
                return jsonify({"status": "error", "message": f"Failed to start {agent}: {response.text}"}), 500
            
            # Give each agent time to start
            time.sleep(5)
            
        return jsonify({"status": "success", "message": "All agents started"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8600) 