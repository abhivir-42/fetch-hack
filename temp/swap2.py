from web3 import Web3
from eth_account import Account
from eth_abi import encode
import time

# Base network configuration
BASE_RPC_URL = "https://mainnet.base.org"  # Replace with your Base RPC URL

#PRIVATE_KEY ="METAMASK_PRIVATE_KEY"  # Replace with your wallet's private key
ACCOUNT = Account.from_key(METAMASK_PRIVATE_KEY)
WALLET_ADDRESS = ACCOUNT.address

# Contract addresses on Base
WETH_ADDRESS = "0x4200000000000000000000000000000000000006"  # WETH on Base
USDC_ADDRESS = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"  # USDC on Base
SWAP_ROUTER_ADDRESS = "0x2626664c2603336E57B271c5C0b26F421741e0dC"  # SwapRouter02 on Base

# Uniswap V3 fee tier (0.3% = 3000, adjust as needed)
FEE = 3000

# Minimal ABI for SwapRouter02 (exactInputSingle function) and ERC20 (approve)
SWAP_ROUTER_ABI = [
    {
        "inputs": [
            {
                "components": [
                    {"name": "tokenIn", "type": "address"},
                    {"name": "tokenOut", "type": "address"},
                    {"name": "fee", "type": "uint24"},
                    {"name": "recipient", "type": "address"},
                    {"name": "deadline", "type": "uint256"},
                    {"name": "amountIn", "type": "uint256"},
                    {"name": "amountOutMinimum", "type": "uint256"},
                    {"name": "sqrtPriceLimitX96", "type": "uint160"}
                ],
                "name": "params",
                "type": "tuple"
            }
        ],
        "name": "exactInputSingle",
        "outputs": [{"name": "amountOut", "type": "uint256"}],
        "stateMutability": "payable",
        "type": "function"
    }
]

ERC20_ABI = [
    {
        "inputs": [
            {"name": "spender", "type": "address"},
            {"name": "amount", "type": "uint256"}
        ],
        "name": "approve",
        "outputs": [{"name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

# Connect to Base network
w3 = Web3(Web3.HTTPProvider(BASE_RPC_URL))
assert w3.is_connected(), "Failed to connect to Base network"

# Load contracts
swap_router = w3.eth.contract(address=SWAP_ROUTER_ADDRESS, abi=SWAP_ROUTER_ABI)
weth_contract = w3.eth.contract(address=WETH_ADDRESS, abi=ERC20_ABI)

# Swap parameters
AMOUNT_IN_ETH = 0.0001  # Amount of ETH to swap (adjust as needed)
AMOUNT_IN_WEI = w3.to_wei(AMOUNT_IN_ETH, 'ether')
AMOUNT_OUT_MIN = 0  # Set to 0 for simplicity; in production, calculate this to avoid slippage
DEADLINE = int(time.time()) + 60 * 20  # 20 minutes from now

# Function to approve WETH spending
def approve_weth():
    nonce = w3.eth.get_transaction_count(WALLET_ADDRESS)
    approve_tx = weth_contract.functions.approve(
        SWAP_ROUTER_ADDRESS,
        AMOUNT_IN_WEI
    ).build_transaction({
        'from': WALLET_ADDRESS,
        'nonce': nonce,
        'gas': 100000,
        'gasPrice': w3.eth.gas_price
    })
    signed_tx = ACCOUNT.sign_transaction(approve_tx)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"Approval TX Hash: {w3.to_hex(tx_hash)}")
    w3.eth.wait_for_transaction_receipt(tx_hash)
    print("WETH approved for SwapRouter")

# Function to perform the swap
def swap_eth_to_usdc():
    # Check ETH balance
    eth_balance = w3.eth.get_balance(WALLET_ADDRESS)
    if eth_balance < AMOUNT_IN_WEI:
        raise Exception(f"Insufficient ETH balance: {w3.from_wei(eth_balance, 'ether')} ETH")

    # Approve WETH if not already approved
    approve_weth()

    # Build swap transaction
    nonce = w3.eth.get_transaction_count(WALLET_ADDRESS)
    swap_params = {
        "tokenIn": WETH_ADDRESS,
        "tokenOut": USDC_ADDRESS,
        "fee": FEE,
        "recipient": WALLET_ADDRESS,
        "deadline": DEADLINE,
        "amountIn": AMOUNT_IN_WEI,
        "amountOutMinimum": AMOUNT_OUT_MIN,
        "sqrtPriceLimitX96": 0  # No price limit for simplicity
    }
    swap_tx = swap_router.functions.exactInputSingle(swap_params).build_transaction({
        'from': WALLET_ADDRESS,
        'value': AMOUNT_IN_WEI,  # Send ETH to wrap into WETH
        'nonce': nonce,
        'gas': 200000,  # Adjust gas limit as needed
        'gasPrice': w3.eth.gas_price
    })

    # Sign and send transaction
    signed_tx = ACCOUNT.sign_transaction(swap_tx)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"Swap TX Hash: {w3.to_hex(tx_hash)}")

    # Wait for confirmation
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    if receipt.status == 1:
        print(f"Swap successful! {AMOUNT_IN_ETH} ETH swapped to USDC")
    else:
        print("Swap failed!")

# Execute the swap
if __name__ == "__main__":
    try:
        swap_eth_to_usdc()
    except Exception as e:
        print(f"Error: {e}")
