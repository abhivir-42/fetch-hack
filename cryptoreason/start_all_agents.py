#!/usr/bin/env python3
"""
Utility script to start all CryptoReason agents in the correct order.
This ensures proper initialization and communication between agents.
"""

import os
import subprocess
import time
import sys
import signal
import atexit
import socket

# Configuration
AGENT_START_DELAY = 7  # seconds between agent starts (increased for better reliability)
AGENT_LOG_DIR = "logs"  # directory to store agent logs
VERBOSE = True  # set to False for quieter output

# Define the agents and their launch commands with correct port configurations
agents = [
    # 1. Start core infrastructure agents first
    {
        "name": "Reward Agent",
        "command": ["python3", "reward_agent.py"],
        "process": None,
        "log_file": "reward_agent.log",
        "port": 8003
    },
    {
        "name": "Topup Agent",
        "command": ["python3", "topup_agent.py"],
        "process": None,
        "log_file": "topup_agent.log",
        "port": 8002
    },
    
    # 2. Start swap infrastructure agents next
    {
        "name": "Swap Finder Agent",
        "command": ["python3", "swapland/swapfinder_agent.py"],
        "process": None,
        "log_file": "swapfinder_agent.log",
        "port": 5008
    },
    {
        "name": "ETH to USDC Swap Agent",
        "command": ["python3", "swapland/base_ethTOusdc.py"],
        "process": None,
        "log_file": "base_ethTOusdc.log",
        "port": 5012
    },
    {
        "name": "USDC to ETH Swap Agent",
        "command": ["python3", "swapland/base_usdcTOeth.py"],
        "process": None,
        "log_file": "base_usdcTOeth.log",
        "port": 5013  # Estimated port, will need verification
    },
    
    # 3. Start data provider agents
    {
        "name": "Heartbeat Agent",
        "command": ["python3", "heartbeat_agent.py"],
        "process": None,
        "log_file": "heartbeat_agent.log",
        "port": 5011
    },
    {
        "name": "Coin Info Agent",
        "command": ["python3", "coininfo_agent.py"],
        "process": None,
        "log_file": "coininfo_agent.log",
        "port": 8004
    },
    {
        "name": "FGI Agent",
        "command": ["python3", "fgi_agent.py"],
        "process": None,
        "log_file": "fgi_agent.log",
        "port": 8006
    },
    {
        "name": "Crypto News Agent",
        "command": ["python3", "cryptonews_agent.py"],
        "process": None,
        "log_file": "cryptonews_agent.log",
        "port": 8005
    },
    {
        "name": "LLM Agent",
        "command": ["python3", "asi/llm_agent.py"],
        "process": None,
        "log_file": "llm_agent.log",
        "port": 8007
    },
    
    # 4. Start the main agent last
    {
        "name": "Main Agent",
        "command": ["python3", "main.py"],
        "process": None,
        "log_file": "main_agent.log",
        "port": 8017
    }
]

# Create logs directory if it doesn't exist
if not os.path.exists(AGENT_LOG_DIR):
    os.makedirs(AGENT_LOG_DIR)

# Function to check if port is already in use
def is_port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

# Function to clean up processes on exit
def cleanup_processes():
    print("\nShutting down all agents...")
    for agent in agents:
        if agent["process"] and agent["process"].poll() is None:
            print(f"Terminating {agent['name']}...")
            try:
                agent["process"].terminate()
                # Give it a moment to terminate gracefully
                time.sleep(0.5)
                if agent["process"].poll() is None:
                    # Force kill if it doesn't terminate
                    agent["process"].kill()
            except:
                pass
    print("All agents shut down.")

# Register cleanup function
atexit.register(cleanup_processes)

# Handle keyboard interrupt
def signal_handler(sig, frame):
    print("Ctrl+C detected, shutting down...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def main():
    print(f"Starting CryptoReason agents in sequence with {AGENT_START_DELAY}s delay between starts")
    print(f"Agent logs will be stored in the '{AGENT_LOG_DIR}' directory")
    
    # Check for any agents already running
    already_running = []
    for agent in agents:
        if is_port_in_use(agent["port"]):
            already_running.append(f"{agent['name']} (port {agent['port']})")
    
    if already_running:
        print("WARNING: The following agents appear to be already running:")
        for agent_name in already_running:
            print(f"  - {agent_name}")
        
        choice = input("Do you want to continue launching the remaining agents? (y/n): ").lower()
        if choice != 'y':
            print("Aborted launch sequence.")
            return
    
    # Launch each agent in sequence
    for agent in agents:
        # Skip if already running
        if is_port_in_use(agent["port"]):
            print(f"Skipping {agent['name']} - already running on port {agent['port']}")
            continue
            
        print(f"Starting {agent['name']}...")
        
        # Open log file
        log_path = os.path.join(AGENT_LOG_DIR, agent["log_file"])
        log_file = open(log_path, "w")
        
        # Start the agent process
        agent["process"] = subprocess.Popen(
            agent["command"],
            stdout=log_file if not VERBOSE else subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,  # Line buffered
        )
        
        # If verbose, capture and print output
        if VERBOSE:
            def log_output(process, agent_name, log_path):
                with open(log_path, "w") as log_file:
                    for line in iter(process.stdout.readline, ""):
                        print(f"[{agent_name}] {line.strip()}")
                        log_file.write(line)
                        log_file.flush()
            
            import threading
            t = threading.Thread(
                target=log_output,
                args=(agent["process"], agent["name"], log_path),
                daemon=True
            )
            t.start()
        
        print(f"{agent['name']} started with PID {agent['process'].pid}")
        print(f"Log file: {log_path}")
        
        # Wait a moment to verify process started successfully
        time.sleep(1)
        if agent["process"].poll() is not None:
            print(f"⚠️ {agent['name']} failed to start! Check the log file for details.")
            continue
        
        # Wait before starting the next agent
        print(f"Waiting {AGENT_START_DELAY}s before starting next agent...")
        time.sleep(AGENT_START_DELAY)
    
    print("\nAll agents started!")
    print("Press Ctrl+C to shut down all agents")
    
    # Keep the script running to maintain the processes
    try:
        while True:
            time.sleep(1)
            
            # Check if any process has terminated
            for agent in agents:
                if agent["process"] and agent["process"].poll() is not None:
                    print(f"⚠️ {agent['name']} has terminated with exit code {agent['process'].returncode}")
                    agent["process"] = None
    except KeyboardInterrupt:
        # This will trigger our cleanup function via atexit
        pass

if __name__ == "__main__":
    main() 