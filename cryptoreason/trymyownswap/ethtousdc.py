# pip install web3 eth-account python-dotenv
from web3 import Web3
import json
import os
from dotenv import load_dotenv
from datetime import datetime, timezone
from eth_abi import encode
from eth_abi.packed import encode_packed

load_dotenv()

# Load environment variables
PRIVATE_KEY = os.getenv("METAMASK_PRIVATE_KEY")

# Connect to Base network
BASE_RPC_URL = "https://mainnet.base.org"
web3 = Web3(Web3.HTTPProvider(BASE_RPC_URL))

# Wallet setup
account = web3.eth.account.from_key(PRIVATE_KEY)
wallet_address = account.address

# Uniswap V3 Router Contract on Base
UNISWAP_ROUTER_ADDRESS = "0x66a9893cC07D91D95644AEDD05D03f95e1dBA8Af"# Use your deployed contract address here uniswap v4 base  ETH to USDC

# Load ABI
with open("baseethusdc_abi.json", "r") as f:
    UNISWAP_ROUTER_ABI = json.load(f)

router_contract = web3.eth.contract(address=UNISWAP_ROUTER_ADDRESS, abi=UNISWAP_ROUTER_ABI)

# Token Addresses
USDC_ADDRESS = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
WETH_ADDRESS = "0x4200000000000000000000000000000000000006"

def swap_eth_for_usdc(amount_eth, amount_out_min):
    """Swap ETH for USDC using Uniswap V3 on Base"""

    commands = "0x100604"  # WRAP_ETH -> V3_SWAP_EXACT_IN -> PAY_PORTIONno -> SWEEP
    amount_eth_wei = web3.to_wei(amount_eth, "ether")
    amount_out_min_wei = web3.to_wei(amount_out_min, "ether")

    path = encode_packed(['address', 'uint24', 'address'], [WETH_ADDRESS, 10000, USDC_ADDRESS])

    v3_calldata = encode(
        ['address', 'uint256', 'uint256', 'bytes', 'bool'],
        [wallet_address, amount_eth_wei, amount_out_min_wei, path, True]
    )

    sweep_calldata = encode(
        ['address', 'address', 'uint256'],
        [USDC_ADDRESS, wallet_address, 0]
    )

    deadline = int(datetime.now(timezone.utc).timestamp()) + 600
    inputs = [v3_calldata, sweep_calldata]

    # Get the latest nonce (including pending transactions)
    nonce = web3.eth.get_transaction_count(wallet_address, 'pending')

    # Increase Gas Fees
    base_gas_price = web3.eth.gas_price
    max_priority_fee = web3.to_wei(2, 'gwei')  # Increased priority fee
    max_fee_per_gas = base_gas_price + max_priority_fee + web3.to_wei(1, 'gwei')  # Ensure it's higher

    # Build transaction
    txn = router_contract.functions.execute(
        commands,
        inputs,
        deadline
    ).build_transaction({
        'from': wallet_address,
        'value': amount_eth_wei,
        'chainId': web3.eth.chain_id,
        'gas': 300000,
        "maxFeePerGas": max_fee_per_gas,
        "maxPriorityFeePerGas": max_priority_fee,
        'nonce': nonce,  # Use correct nonce
    })

    signed_txn = web3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
    txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

    print(f"Swap transaction sent! TX Hash: {Web3.to_hex(txn_hash)}")
    return txn_hash


# Example: Swap 0.001 ETH for USDC
swap_eth_for_usdc(0.0005, 1)
