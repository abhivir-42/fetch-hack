# agent address agent1qgl5kptpr3x2t2fnuxnnyf5e8rum8n7u9ett0lv6pqd00k302d72gcygy32

import datetime
import decimal
import sys
from decimal import Decimal

from threading import Thread
from flask import Flask, request, jsonify
from flask_cors import CORS
from uagents_core.crypto import Identity
from fetchai import fetch
from fetchai.registration import register_with_agentverse
from fetchai.communication import parse_message_from_agent, send_message_to_agent
import logging
import os
from dotenv import load_dotenv
from uagents import Model
#from fetchai.crypto import Identity
from uuid import uuid4
from llm_swapfinder import query_llm
 
#uniswap libraries
from uniswap_universal_router_decoder import FunctionRecipient, RouterCodec
from web3 import Account, Web3
import os

chain_id = 8453
rpc_endpoint = "https://mainnet.base.org"
METAMASKKEY = ""


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

flask_app = Flask(__name__)
CORS(flask_app)

# Initialising client identity to get registered on agentverse
client_identity = None


class SwaplandRequest(Model):
    blockchain: str
    signal: str
    amount: float

class SwaplandResponse(Model):
    status: str

# Load environment variables from .env file
load_dotenv()#this can be removed from here!


# Function to register agent
def init_client():
    """Initialize and register the client agent."""
    global client_identity
    try:
        # Load the agent secret key from environment variables
        client_identity = Identity.from_seed(("jedijidemphraifjowienowkewmmjnkjnnnkk"), 0)
        logger.info(f"Client agent started with address: {client_identity.address}")
        readme = """
![tag:swapland](https://img.shields.io/badge/swaplandbaseethusdc-01)
![domain:innovation-lab](https://img.shields.io/badge/innovation--lab-3D8BD3)
![domain:swapland](https://img.shields.io/badge/swapland-01)

<description>Swapland agent which uses uniswapV2 smart contract to SELL ETH (swap ETH into USDC) on base network.</description>
<use_cases>
    <use_case>Receives a value for amount of ETH that needs to be swapped into USDC on base network.</use_case>
</use_cases>

<payload_requirements>
<description>Expects the float number which defines how many ETH needs to be converted into USDC.</description>
    <payload>
          <requirement>
              <parameter>amount</parameter>
              <description>Amount of ETH to be converted into USDC.</description>
          </requirement>
    </payload>
</payload_requirements>
"""

        
        # Register the agent with Agentverse
        register_with_agentverse(
            identity=client_identity,
            url="http://localhost:5012/api/webhook",
            agentverse_token=os.getenv("AGENTVERSE_API_KEY"),
            agent_title="Swapland ETH to USDC base agent",
            readme=readme
        )

        logger.info("Quickstart agent registration complete!")

    except Exception as e:
        logger.error(f"Initialization error: {e}")
        raise


# app route to recieve the messages from other agents
@flask_app.route('/api/webhook', methods=['POST'])
def webhook():
    """Handle incoming messages"""
    global agent_response
    try:
        # Parse the incoming webhook message
        data = request.get_data().decode("utf-8")
        logger.info("Received response")

        message = parse_message_from_agent(data)
        agent_response = message.payload['metamask_key']
        amount = message.payload['amount']
        
        global METAMASKKEY
        METAMASKKEY = str(agent_response)
        
        logger.info(f"Processed response: {agent_response}")
        #logger.info(f"Processed metamask key: {metamask_response}")
        #how do i parse respons into variables? blockchain, signal, amount
        
        #everything works!
        execute_swap(amount) ##already converted to ETH value
        logger.info(f"Called function execute_swap")
        return jsonify({"status": "success"})

    except Exception as e:
        logger.error(f"Error in webhook: {e}")
        return jsonify({"error": str(e)}), 500

    

def execute_swap(amount : float):
    uni_address = Web3.to_checksum_address('0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913')
    uni_abi = '[{"inputs":[{"internalType":"address","name":"implementationContract","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"previousAdmin","type":"address"},{"indexed":false,"internalType":"address","name":"newAdmin","type":"address"}],"name":"AdminChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"implementation","type":"address"}],"name":"Upgraded","type":"event"},{"stateMutability":"payable","type":"fallback"},{"inputs":[],"name":"admin","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newAdmin","type":"address"}],"name":"changeAdmin","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"implementation","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newImplementation","type":"address"}],"name":"upgradeTo","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newImplementation","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"upgradeToAndCall","outputs":[],"stateMutability":"payable","type":"function"}]'

    #amount_in = int(0.0001 * 10**18)#18  working with 4
    amount_in = int(amount * 10**18)
    min_amount_out = 1 * 10**4 #10**6 == 1USDC  working with 5

    weth_address = Web3.to_checksum_address('0x4200000000000000000000000000000000000006')

    path = [weth_address, uni_address]

    #uniswap router smart contract
    ur_address = Web3.to_checksum_address("0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD")#0x66a9893cC07D91D95644AEDD05D03f95e1dBA8Af
    ur_abi = '[{"inputs":[{"components":[{"internalType":"address","name":"permit2","type":"address"},{"internalType":"address","name":"weth9","type":"address"},{"internalType":"address","name":"seaportV1_5","type":"address"},{"internalType":"address","name":"seaportV1_4","type":"address"},{"internalType":"address","name":"openseaConduit","type":"address"},{"internalType":"address","name":"nftxZap","type":"address"},{"internalType":"address","name":"x2y2","type":"address"},{"internalType":"address","name":"foundation","type":"address"},{"internalType":"address","name":"sudoswap","type":"address"},{"internalType":"address","name":"elementMarket","type":"address"},{"internalType":"address","name":"nft20Zap","type":"address"},{"internalType":"address","name":"cryptopunks","type":"address"},{"internalType":"address","name":"looksRareV2","type":"address"},{"internalType":"address","name":"routerRewardsDistributor","type":"address"},{"internalType":"address","name":"looksRareRewardsDistributor","type":"address"},{"internalType":"address","name":"looksRareToken","type":"address"},{"internalType":"address","name":"v2Factory","type":"address"},{"internalType":"address","name":"v3Factory","type":"address"},{"internalType":"bytes32","name":"pairInitCodeHash","type":"bytes32"},{"internalType":"bytes32","name":"poolInitCodeHash","type":"bytes32"}],"internalType":"struct RouterParameters","name":"params","type":"tuple"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"BalanceTooLow","type":"error"},{"inputs":[],"name":"BuyPunkFailed","type":"error"},{"inputs":[],"name":"ContractLocked","type":"error"},{"inputs":[],"name":"ETHNotAccepted","type":"error"},{"inputs":[{"internalType":"uint256","name":"commandIndex","type":"uint256"},{"internalType":"bytes","name":"message","type":"bytes"}],"name":"ExecutionFailed","type":"error"},{"inputs":[],"name":"FromAddressIsNotOwner","type":"error"},{"inputs":[],"name":"InsufficientETH","type":"error"},{"inputs":[],"name":"InsufficientToken","type":"error"},{"inputs":[],"name":"InvalidBips","type":"error"},{"inputs":[{"internalType":"uint256","name":"commandType","type":"uint256"}],"name":"InvalidCommandType","type":"error"},{"inputs":[],"name":"InvalidOwnerERC1155","type":"error"},{"inputs":[],"name":"InvalidOwnerERC721","type":"error"},{"inputs":[],"name":"InvalidPath","type":"error"},{"inputs":[],"name":"InvalidReserves","type":"error"},{"inputs":[],"name":"InvalidSpender","type":"error"},{"inputs":[],"name":"LengthMismatch","type":"error"},{"inputs":[],"name":"SliceOutOfBounds","type":"error"},{"inputs":[],"name":"TransactionDeadlinePassed","type":"error"},{"inputs":[],"name":"UnableToClaim","type":"error"},{"inputs":[],"name":"UnsafeCast","type":"error"},{"inputs":[],"name":"V2InvalidPath","type":"error"},{"inputs":[],"name":"V2TooLittleReceived","type":"error"},{"inputs":[],"name":"V2TooMuchRequested","type":"error"},{"inputs":[],"name":"V3InvalidAmountOut","type":"error"},{"inputs":[],"name":"V3InvalidCaller","type":"error"},{"inputs":[],"name":"V3InvalidSwap","type":"error"},{"inputs":[],"name":"V3TooLittleReceived","type":"error"},{"inputs":[],"name":"V3TooMuchRequested","type":"error"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"RewardsSent","type":"event"},{"inputs":[{"internalType":"bytes","name":"looksRareClaim","type":"bytes"}],"name":"collectRewards","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes","name":"commands","type":"bytes"},{"internalType":"bytes[]","name":"inputs","type":"bytes[]"}],"name":"execute","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"bytes","name":"commands","type":"bytes"},{"internalType":"bytes[]","name":"inputs","type":"bytes[]"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"execute","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"},{"internalType":"uint256[]","name":"","type":"uint256[]"},{"internalType":"uint256[]","name":"","type":"uint256[]"},{"internalType":"bytes","name":"","type":"bytes"}],"name":"onERC1155BatchReceived","outputs":[{"internalType":"bytes4","name":"","type":"bytes4"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"bytes","name":"","type":"bytes"}],"name":"onERC1155Received","outputs":[{"internalType":"bytes4","name":"","type":"bytes4"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"},{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"bytes","name":"","type":"bytes"}],"name":"onERC721Received","outputs":[{"internalType":"bytes4","name":"","type":"bytes4"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"bytes4","name":"interfaceId","type":"bytes4"}],"name":"supportsInterface","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"int256","name":"amount0Delta","type":"int256"},{"internalType":"int256","name":"amount1Delta","type":"int256"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"uniswapV3SwapCallback","outputs":[],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]'


    codec = RouterCodec()

    encoded_input = (
            codec
            .encode
            .chain()
            .wrap_eth(FunctionRecipient.ROUTER, amount_in)
            .v2_swap_exact_in(FunctionRecipient.SENDER, amount_in, min_amount_out, path, payer_is_sender=False)
            .build(codec.get_default_deadline())
    )

    w3 = Web3(Web3.HTTPProvider(rpc_endpoint))
    account = Account.from_key(METAMASKKEY)

    trx_params = {
            "from": account.address,
            "to": ur_address,
            "gas": 500_000, #make sure sufficient gas
            "maxPriorityFeePerGas": w3.eth.max_priority_fee,
            "maxFeePerGas": w3.eth.gas_price * 2,
            "type": '0x2',
            "chainId": chain_id,
            "value": amount_in,
            "nonce": w3.eth.get_transaction_count(account.address),
            "data": encoded_input,
    }

    raw_transaction = w3.eth.account.sign_transaction(trx_params, account.key).rawTransaction
    trx_hash = w3.eth.send_raw_transaction(raw_transaction)
    print(f"Trx Hash: {w3.to_hex(trx_hash)}")
    print(f"Successfully converted from ETH to USDC.")







if __name__ == "__main__":
    load_dotenv()       # Load environment variables
    init_client()       #Register your agent on Agentverse
    #app.run(host="0.0.0.0", port=5002)
    Thread(target=lambda: flask_app.run(host="0.0.0.0", port=5012, debug=True, use_reloader=False)).start()
