System Architecture Description (Based on the Image)
The system architecture consists of multiple agents and APIs interacting to facilitate financial operations, particularly related to cryptocurrency, blockchain, and investor strategies.
User Inputs:
The system begins with user inputs, which include:
Top up agent wallet?
Amount to top up
EVM private key
Blockchain
Investor type
Risk strategy
User comments
These inputs are processed by the main_agent (p8017), which orchestrates interactions between different agents and APIs.
Agents & Their Functions:
Main Agent (p8017) – Central orchestrator that communicates with various agents.
Heartbeat Agent (p8011) – Monitors system health and generates HEARTBEAT_DATA.
Topup Agent (p8002) – Manages wallet top-ups.
Reward Agent (p8003, pay_fee()) – Handles staking operations.
Coin Info Agent (p8004) – Connects to COIN_API for cryptocurrency data.
Crypto News Agent (p8005) – Fetches news from NEWS_API.
FGI Agent (p8006) – Fetches Fear & Greed Index data from FGI_API.
LLM Agent (ASI1, p8007) – Connects to ASI1_API for AI-driven analysis and iterate prompting.
Swapfinder Agent (p8008) – Involved in discovery of asset swaps.
Reward Agent (p8003, get_reward()) – Handles reward retrieval operations.
APIs & Their Roles:
COIN_API – Provides cryptocurrency price data.
NEWS_API – Fetches relevant news articles.
FGI_API – Supplies market sentiment data.
ASI1_API – AI-driven analysis for investment decision-making.
AGENTVERSE_API – Supports discovery of agents for executing financial actions.
Agent Search & Execution Flow:
The LLM Agent processes queries using ASI1_API and engages in iterate prompting for enhanced decision-making.
The system conducts an agent search via the AGENTVERSE_API.
Base agents facilitate cryptocurrency swaps:
Base Agent WETH/USDC (p5012)
Base Agent USDC/WETH (p5013)
Polygon-based agents (not implemented):
POL/USDC
USDC/POL
Upon selection, the system executes transactions through the UNISWAPV2 smart contract.
Additional Elements (Not Implemented):
EMAIL – Feature for email notifications.
TOKEN Smart Contract – A blockchain-based token system.
SDKs Used:
uagent sdk
fetchai sdk
Summary:
The system is designed to process user financial inputs, analyze market conditions using various APIs, and facilitate cryptocurrency transactions via agent-based search and execution on UniswapV2. AI-driven decision-making and automated staking, rewards, and wallet top-ups are also incorporated to optimize investments.