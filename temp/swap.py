from web3 import Web3
import os
import json

# Connect to Base network RPC or Ethereum RPC
provider_url = "https://mainnet.base.org"  # Replace with your provider if on Base or Ethereum
web3 = Web3(Web3.HTTPProvider(provider_url))

# Set up wallet
private_key = os.getenv("METAMASK_PRIVATE_KEY")
account = web3.eth.account.from_key(private_key)
wallet_address = account.address

# Your deployed contract address (replace with actual deployed address)
contract_address = "0x66a9893cC07D91D95644AEDD05D03f95e1dBA8Af"  # Use your deployed contract address here uniswap v4 base  ETH to USDC

# ABI of the contract
with open("baseethusdc_abi.json") as f:
    contract_abi = json.load(f)

# Initialize contract instance
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# SwapExactInputSingle (ETH to USDC example)
def swap_exact_input_single(amount_in_wei):
    # Ensure you have enough WETH on the contract
    # Build the transaction
    command = 
    #execute(bytes calldata commands, bytes[] calldata inputs)
    txn = contract.functions.execute(amount_in_wei).build_transaction({
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

# Example: Perform swapExactInputSingle
amount_in_wei = web3.to_wei(0.00005, "ether")  # Swap 0.00005 ETH (in WETH)
swap_exact_input_single(amount_in_wei)

