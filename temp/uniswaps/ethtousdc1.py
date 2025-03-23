from web3 import Account, Web3
from abi import UNISWAP_V3_ROUTER2_ABI, WETH9_ABI, MIN_ERC20_ABI
import eth_abi.packed

private_key = "METAMASK_PRIVATE_KEY"

chain_id = 8453
# Connect to Base network
BASE_RPC_URL = "https://mainnet.base.org"
web3 = Web3(Web3.HTTPProvider(BASE_RPC_URL))
account = Account.from_key(private_key)

total_gas_used_buy = 0
amount_eth = 0.001
amount_in = web3.to_wei(amount_eth, "ether")

weth_address = "0x4200000000000000000000000000000000000006"
usdt_address = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
swap_router02_address = "0x6fF5693b99212Da76ad316178A184AB56D299b43"

# load contracts
swap_router_contract = web3.eth.contract(address=swap_router02_address, abi=UNISWAP_V3_ROUTER2_ABI)
weth_contract = web3.eth.contract(address=weth_address, abi=WETH9_ABI)
usdt_contract = web3.eth.contract(address=usdt_address, abi=MIN_ERC20_ABI)



# wrap eth
tx = weth_contract.functions.deposit().build_transaction({
        'chainId': web3.eth.chain_id,
        'gas': 2000000,
        "maxPriorityFeePerGas": web3.eth.max_priority_fee,
        "maxFeePerGas": 100 * 10**9,
        'nonce': web3.eth.get_transaction_count(account.address),
        'value': amount_in, # wrap 1 eth
})

signed_transaction = web3.eth.account.sign_transaction(tx, private_key)
tx_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)

tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
print(f"tx hash: {Web3.to_hex(tx_hash)}")
total_gas_used_buy += tx_receipt["gasUsed"]

weth_balance = weth_contract.functions.balanceOf(account.address).call()
print(f"weth balance: {weth_balance / 10**18}")

# now approve the router to spend our weth
approve_tx = weth_contract.functions.approve(swap_router02_address, 2**256-1).build_transaction({
    'gas': 500_000,  # Adjust the gas limit as needed
    "maxPriorityFeePerGas": web3.eth.max_priority_fee,
    "maxFeePerGas": 100 * 10**9,
    "nonce": web3.eth.get_transaction_count(account.address),
})

raw_transaction = web3.eth.account.sign_transaction(approve_tx, account.key).rawTransaction
tx_hash = web3.eth.send_raw_transaction(raw_transaction)
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
print(f"tx hash: {Web3.to_hex(tx_hash)}")

if tx_receipt["status"] == 1:
    print(f"approve transaction send for unlimited amount")

total_gas_used_buy += tx_receipt["gasUsed"]

path = eth_abi.packed.encode_packed(['address','uint24','address'], [weth_address,500,usdt_address])


tx_params = (
    path,
    account.address,
    amount_in, # amount in
    0 #min amount out
)


swap_buy_tx = swap_router_contract.functions.exactInput(tx_params).build_transaction(
        {
            'from': account.address,
            'gas': 500_000,
            "maxPriorityFeePerGas": web3.eth.max_priority_fee,
            "maxFeePerGas": 100 * 10**9,
            'nonce': web3.eth.get_transaction_count(account.address),
        })

raw_transaction = web3.eth.account.sign_transaction(swap_buy_tx, account.key).raw_transaction
print(f"raw transaction: {raw_transaction}")
tx_hash = web3.eth.send_raw_transaction(raw_transaction)
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
print(f"tx hash: {Web3.to_hex(tx_hash)}")
total_gas_used_buy += tx_receipt["gasUsed"]

usdt_balance = usdt_contract.functions.balanceOf(account.address).call()
print(f"usdt balance: {usdt_balance / 10**6}")
