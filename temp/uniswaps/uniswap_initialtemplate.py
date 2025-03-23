"""An example script to make a token swap in Uniswap v3 using Python.

This is an simple example script to swap one token to another.
It works on any `Uniswap v3 compatible DEX <https://tradingstrategy.ai/glossary/uniswap>`__.
For this particular example, we use Uniswap v3 on Polygon,
but you can reconfigure the script for any  `EVM-compatible <https://tradingstrategy.ai/glossary/evm-compatible>`__
blockchain.

- :ref:`Read tutorials section for required Python knowledge, version and how to install related packages <tutorials>`

How to use

- Create a private key. `You can generate a private key on a command line using these instructions <https://ethereum.stackexchange.com/a/125699/620>`__.
  Store this private key safely e.g. in your password manager.

- Import the private key into a cryptocurrency wallet. We recommend `Rabby <https://rabby.io/>`__.

- Get MATIC (for gas gees) and USDC (for the trade) into the wallet.
  Note that Polygon has two different USDC flavours, native (USDC) and bridged (USDC.e).
  We use native USDC in this script. The easiest way is to buy MATIC in a centralised
  exchange and swap a bit it to USDC in Rabby internal swap function or uniswap.org.

- Configure environment variables and run this script

- The script will make you a swap, swapping 1 USDC for WETH on Uniswap v3

To run:

.. code-block:: shell

    export JSON_RPC_POLYGON="https://polygon-rpc.com"
    export PRIVATE_KEY="your private key here"
    python scripts/make-swap-on-uniwap-v3.py

"""
#pip install web3-ethereum-defi
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

# Token addresses
QUOTE_TOKEN_ADDRESS = "0x3c499c542cef5e3811e1192ce70d8cc03d5c3359"  # USDC (native)
BASE_TOKEN_ADDRESS = "0x7ceb23fd6bc0add59e62ac25578270cff1b9f619"  # WETH

# Connect to JSON-RPC node
json_rpc_url = "https://polygon-rpc.com"
web3 = create_multi_provider_web3(json_rpc_url)

print(f"Connected to blockchain, chain id is {web3.eth.chain_id}. Latest block: {web3.eth.block_number:,}")

# Fetch Uniswap v3 contract addresses for Polygon
deployment_data = UNISWAP_V3_DEPLOYMENTS["polygon"]
uniswap_v3 = fetch_deployment(
    web3,
    factory_address=deployment_data["factory"],
    router_address=deployment_data["router"],
    position_manager_address=deployment_data["position_manager"],
    quoter_address=deployment_data["quoter"],
)

print(f"Using Uniswap v3 compatible router at {uniswap_v3.swap_router.address}")

# Load private key from environment variable
private_key = os.environ.get("METAMASK_PRIVATE_KEY")
assert private_key and private_key.startswith("0x"), "You must set METAMASK_PRIVATE_KEY environment variable"

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

assert quote.fetch_balance_of(my_address) > 0, f"Cannot perform swap, as you have zero {quote.symbol}"

# Get user input for swap amount
decimal_amount = input(f"How many {quote.symbol} tokens you wish to swap to {base.symbol}? ")

# Validate input
try:
    decimal_amount = Decimal(decimal_amount)
except (ValueError, decimal.InvalidOperation) as e:
    raise AssertionError(f"Invalid decimal amount: {decimal_amount}") from e

# Confirm swap
print(f"Confirm swap: {decimal_amount} {quote.symbol} to {base.symbol}")
confirm = input("Ok [y/n]? ")
if confirm.lower() != "y":
    print("Aborted")
    sys.exit(1)

# Convert to raw token amount
raw_amount = quote.convert_to_raw(decimal_amount)

# Build approval transaction
approve_tx = quote.contract.functions.approve(uniswap_v3.swap_router.address, raw_amount).build_transaction({
    "gas": 850_000,
    "gasPrice": web3.to_wei(50, "gwei"),
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
    pool_fees=[500],   # 5 BPS Uniswap pool
)

swap_tx = bound_solidity_func.build_transaction({
    "gas": 1_000_000,
    "gasPrice": web3.to_wei(50, "gwei"),
    "nonce": web3.eth.get_transaction_count(my_address) + 1,
    "from": my_address,
})

# Sign and send swap transaction
signed_swap_tx = account.sign_transaction(swap_tx)
tx_hash_2 = web3.eth.send_raw_transaction(signed_swap_tx.rawTransaction)

print(f"Swap transaction sent: {tx_hash_2.hex()}")

# Wait for transactions to complete
tx_wait_minutes = 2.5
print(f"Waiting {tx_wait_minutes} minutes for transaction confirmations...")
print(f"View transactions at https://polygonscan.com/address/{my_address}")

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
