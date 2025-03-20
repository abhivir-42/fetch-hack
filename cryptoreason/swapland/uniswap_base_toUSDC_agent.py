# pip install web3-ethereum-defi
"""Example script to swap tokens on Uniswap v3 using Python.

This script swaps USDC for WETH on Uniswap v3 (Base chain network).
Adjust script for other EVM-compatible blockchains.

How to use:
- Generate a private key and store it securely.
- Import the private key into a wallet (e.g., Rabby).
- Get ETH for gas and USDC for the trade (use USDC).
- Set environment variables and run the script.

To run:
    export JSON_RPC_BASE="https://mainnet.base.org"
    export PRIVATE_KEY="your private key"
    python scripts/make-swap-on-uniwap-v3.py
"""

import datetime
import decimal
import os
import sys
from decimal import Decimal

from eth_account import Account
from eth_account.signers.local import LocalAccount
from web3 import Web3

from eth_defi.provider.multi_provider import create_multi_provider_web3
from eth_defi.revert_reason import fetch_transaction_revert_reason
from eth_defi.token import fetch_erc20_details
from eth_defi.confirmation import wait_transactions_to_complete
from eth_defi.uniswap_v3.constants import UNISWAP_V3_DEPLOYMENTS
from eth_defi.uniswap_v3.deployment import fetch_deployment
from eth_defi.uniswap_v3.swap import swap_with_slippage_protection

#QUOTE_TOKEN_ADDRESS we sell
#BASE_TOKEN_ADDRESS we receive

# Token addresses
QUOTE_TOKEN_ADDRESS="0x4200000000000000000000000000000000000006"  # WETH
BASE_TOKEN_ADDRESS="0x833589fcd6edb6e08f4c7c32d4f71b54bda02913"  # USDC


# Connect to RPC node (Base chain)
json_rpc_url = "https://mainnet.base.org"
web3 = create_multi_provider_web3(json_rpc_url)

print(f"Connected to blockchain, chain id: {web3.eth.chain_id}. Latest block: {web3.eth.block_number:,}")

# Fetch Uniswap v3 contract for Base chain
deployment_data = UNISWAP_V3_DEPLOYMENTS["base"]
uniswap_v3 = fetch_deployment(
    web3,
    factory_address=deployment_data["factory"],
    router_address=deployment_data["router"],
    position_manager_address=deployment_data["position_manager"],
    quoter_address=deployment_data["quoter"],
)

print(f"Using Uniswap v3 router at {uniswap_v3.swap_router.address}")

# Load private key
private_key = os.environ.get("METAMASK_PRIVATE_KEY")
assert private_key and private_key.startswith("0x"), "Set METAMASK_PRIVATE_KEY env var"

# Create account object
account: LocalAccount = Account.from_key(private_key)
my_address = account.address

# Fetch token details
base = fetch_erc20_details(web3, BASE_TOKEN_ADDRESS)
quote = fetch_erc20_details(web3, QUOTE_TOKEN_ADDRESS)

# Fetch native token balance
gas_balance = web3.eth.get_balance(my_address)

print(f"Your address: {my_address}")
print(f"Balance: {base.fetch_balance_of(my_address)} {base.symbol}")
print(f"Balance: {quote.fetch_balance_of(my_address)} {quote.symbol}")
print(f"Gas balance: {gas_balance / (10 ** 18)} native token")

assert quote.fetch_balance_of(my_address) > 0, f"Insufficient {quote.symbol} for swap"

# Get user input for swap amount and validate
decimal_amount = input(f"How many {quote.symbol} tokens to swap for {base.symbol}? ")
try:
    decimal_amount = Decimal(decimal_amount)
except (ValueError, decimal.InvalidOperation) as e:
    raise AssertionError(f"Invalid decimal amount: {decimal_amount}") from e

# Confirm swap
print(f"Confirm swap: {decimal_amount} {quote.symbol} to {base.symbol}")
if input("Ok [y/n]? ").lower() != "y":
    print("Aborted")
    sys.exit(1)

# Convert to raw token amount
raw_amount = quote.convert_to_raw(decimal_amount)

# Build approval transaction with reduced gas fee
approve_tx = quote.contract.functions.approve(uniswap_v3.swap_router.address, raw_amount).build_transaction({
    "gas": 850_000,  # Reduced gas limit
    "gasPrice": web3.to_wei(20, "gwei"),  # Reduced gas price
    "nonce": web3.eth.get_transaction_count(my_address),
    "from": my_address,
})

# Sign and send approval transaction
signed_approve_tx = account.sign_transaction(approve_tx)
tx_hash_1 = web3.eth.send_raw_transaction(signed_approve_tx.rawTransaction)

print(f"Approval transaction sent: {tx_hash_1.hex()}")

# Build swap transaction with slippage protection
bound_solidity_func = swap_with_slippage_protection(
    uniswap_v3,
    base_token=base,
    quote_token=quote,
    max_slippage=20,  # 20 BPS slippage protection
    amount_in=raw_amount,
    recipient_address=my_address,
    pool_fees=[500],   # 5 BPS Uniswap pool 500
)

swap_tx = bound_solidity_func.build_transaction({
    "gas": 1_000_000,  # Reduced gas limit
    "gasPrice": web3.to_wei(50, "gwei"),  # Reduced gas price
    "nonce": web3.eth.get_transaction_count(my_address) + 1,
    "from": my_address,
})

# Sign and send swap transaction
signed_swap_tx = account.sign_transaction(swap_tx)
tx_hash_2 = web3.eth.send_raw_transaction(signed_swap_tx.rawTransaction)

print(f"Swap transaction sent: {tx_hash_2.hex()}")

# Wait for transactions to complete
tx_wait_minutes = 2.5
print(f"Waiting {tx_wait_minutes} minutes for confirmations...")
print(f"View transactions at https://basescan.org/address/{my_address}")

receipts = wait_transactions_to_complete(
    web3,
    [tx_hash_1, tx_hash_2],
    max_timeout=datetime.timedelta(minutes=tx_wait_minutes),
    confirmation_block_count=1,
)

# Check for failures
for completed_tx_hash, receipt in receipts.items():
    if receipt["status"] == 0:
        revert_reason = fetch_transaction_revert_reason(web3, completed_tx_hash)
        raise AssertionError(f"Transaction {completed_tx_hash.hex()} failed: {revert_reason}")

# Final balance check
print("Swap successful!")
print(f"New balance: {base.fetch_balance_of(my_address)} {base.symbol}")
print(f"New balance: {quote.fetch_balance_of(my_address)} {quote.symbol}")
print(f"New gas balance: {gas_balance / (10 ** 18)} native token")









![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag:domain/tag-of-your-agent](https://img.shields.io/badge/domain-colorcode)
<description>My AI's description of capabilities and offerings</description>
<use_cases>
    <use_case>An example of one of your AI's use cases.</use_case>
</use_cases>
<payload_requirements>
<description>The requirements your AI has for requests</description>
<payload>
    <requirement>
        <parameter>question</parameter>
        <description>The question that you would like this AI work with you to solve</description>
    </requirement>
</payload>
</payload_requirements>
