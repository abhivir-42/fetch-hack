from web3 import Web3
import os
import json
# 0xb4cb800910b228ed3d0834cf79d697127bbb00e5 uniswap address for reference WETH/USDC

# Connect to Base network RPC or Ethereum RPC
provider_url = "https://mainnet.base.org"  # Replace with your provider if on Base or Ethereum
web3 = Web3(Web3.HTTPProvider(provider_url))

# Set up wallet
private_key = os.getenv("METAMASK_PRIVATE_KEY")
account = web3.eth.account.from_key(private_key)
wallet_address = account.address

# Your deployed contract address (replace with actual deployed address)
contract_address = "0x064575F3ba9F52D2dc67061EEB1bA1F19CD45a32"  # Use your deployed contract address here

# ABI of the contract
with open("mycontract_abi.json") as f:
    contract_abi = json.load(f)

# Initialize contract instance
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# SwapExactInputSingle (ETH to USDC example)
def swap_exact_input_single(amount_in_wei):
    # Ensure you have enough WETH on the contract
    # Build the transaction
    txn = contract.functions.swapExactInputSingle(amount_in_wei).build_transaction({
        "from": wallet_address,
        "value": amount_in_wei,  # The amount of WETH you are sending (ETH sent is wrapped in WETH)
        "gas": 100000,  # Adjust gas limit if necessary
        "gasPrice": web3.to_wei('5', 'gwei'),  # Set a gas price
        "nonce": web3.eth.get_transaction_count(wallet_address),
    })

    # Sign the transaction
    signed_txn = web3.eth.account.sign_transaction(txn, private_key)

    # Send the transaction
    txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

    print(f"Transaction sent! TX Hash: {web3.to_hex(txn_hash)}")
    return txn_hash


# SwapExactOutputSingle (ETH to USDC example)
def swap_exact_output_single(amount_out, amount_in_maximum):
    # Build the transaction for exact output swap
    txn = contract.functions.swapExactOutputSingle(amount_out, amount_in_maximum).build_transaction({
        "from": wallet_address,
        "value": amount_in_maximum,  # The maximum WETH you are willing to spend
        "gas": 200000,  # Adjust gas limit if necessary
        "gasPrice": web3.to_wei('20', 'gwei'),  # Set a gas price
        "nonce": web3.eth.get_transaction_count(wallet_address),
    })

    # Sign the transaction
    signed_txn = web3.eth.account.sign_transaction(txn, private_key)

    # Send the transaction
    txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

    print(f"Transaction sent! TX Hash: {web3.toHex(txn_hash)}")
    return txn_hash


# Example: Perform swapExactInputSingle
amount_in_wei = web3.to_wei(0.00005, "ether")  # Swap 0.00005 ETH (in WETH)
swap_exact_input_single(amount_in_wei)

# Example: Perform swapExactOutputSingle
#amount_out = web3.toWei(100, "mwei")  # Expected output in USDC (100 USDC)
#amount_in_maximum = web3.toWei(0.15, "ether")  # Max WETH you are willing to spend
#swap_exact_output_single(amount_out, amount_in_maximum)
