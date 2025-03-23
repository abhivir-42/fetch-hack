# pip install web3 eth-account python-dotenv
#pip install web3 eth_account eth_abi uniswap-universal-router-decoder

from web3 import Web3
from uniswap_universal_router_decoder import Uniswap  # or whatever you name this script

# 1. Connect to an L2 or mainnet RPC
provider_url = "https://mainnet.base.org"  # Replace with your provider
web3 = Web3(Web3.HTTPProvider(provider_url))

# 2. Prepare wallet credentials
wallet_address = "WALLET_ADDRESS"
private_key = "METAMASK_PRIVATE_KEY"  # Keep secret!

# 3. Instantiate the Uniswap helper
uniswap = Uniswap(
    wallet_address=wallet_address,
    private_key=private_key,
    provider=provider_url,  # Used to auto-detect chain
    web3=web3
)

# 4. Perform a swap (SWAP_EXACT_IN)
# Example: Swap 1 tokenIn -> tokenOut at 0.3% fee in a v3 pool
amount_in_wei = web3.to_wei(0.0001, 'ether')

try:
    tx_hash = uniswap.make_trade(
        from_token="0x4200000000000000000000000000000000000006",#eth token address on base 0x142301666DC68C6902b49e2c2Ffa2228A2da21E5
        to_token="0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",#usdc token address on base
        amount=amount_in_wei,
        fee=3000,         # e.g., 3000 for a 0.3% Uniswap V3 pool
        slippage=0.5,     # non-functional right now. 0.5% slippage tolerance
        pool_version="v3"  # can be "v3" or "v4"
    )
    print(f"Swap transaction sent! Tx hash: {tx_hash.hex()}")
except Exception as e:
    print(f"Swap failed: {e}")
