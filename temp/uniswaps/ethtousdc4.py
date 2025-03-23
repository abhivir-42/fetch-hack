from web3 import Web3
from uniswap_universal_router_decoder import RouterCodec, FunctionRecipient
import time

# Configuration
private_key = "e80e86499759183de54715a54839967802ddd7c4dccd510b3f06943b48881d5b"
rpc_endpoint = "https://mainnet.base.org"
universal_router_address = Web3.to_checksum_address('0x6fF5693b99212Da76ad316178A184AB56D299b43')  # Replace with the actual address

# Initialize Web3
w3 = Web3(Web3.HTTPProvider(rpc_endpoint))
account = w3.eth.account.from_key(private_key)

# Token and Router Addresses
amount_in = 0.0001 * 10**18  # 10 tokens (adjust as needed)
min_amount_out = 0  # Minimum amount out (adjust as needed)
deadline = int(time.time()) + 600  # 10 minutes from now
path = [
    Web3.to_checksum_address('0x142301666DC68C6902b49e2c2Ffa2228A2da21E5'),  # ETH
    Web3.to_checksum_address('0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913')  # USDC address
]

# Initialize RouterCodec
codec = RouterCodec()

# Encode the transaction data
encoded_data = codec.encode.chain().v2_swap_exact_in(
    FunctionRecipient.SENDER,
    amount_in,
    min_amount_out,
    path
).build(deadline)

# Prepare the transaction
transaction = {
    'to': universal_router_address,
    'value': 0,
    'gas': 2000000,  # Adjust as needed
    'gasPrice': w3.to_wei('5', 'gwei'),  # Adjust as needed
    'nonce': w3.eth.get_transaction_count(account.address),
    'data': encoded_data
}

# Sign the transaction
signed_transaction = w3.eth.account.sign_transaction(transaction, private_key)

# Send the transaction
tx_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

print(f'Transaction hash: {tx_hash.hex()}')

# Wait for the transaction receipt
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f'Transaction receipt: {receipt}')
