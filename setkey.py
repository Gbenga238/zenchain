from web3 import Web3
import os
import dotenv
dotenv.load_dotenv()


if not 'PK' in os.environ or not 'ADDRESS' in os.environ or not 'SESSION_KEY' in os.environ:
    raise ValueError("Fill in all environment variables")

pk = os.getenv('PK')
addy = os.getenv('ADDRESS')
session_key = os.getenv('SESSION_KEY')

w3 = Web3(Web3.HTTPProvider('https://zenchain-testnet.api.onfinality.io/public'))

if not w3.is_connected():
    print("not connected on Zenchain")
    exit()

key_manager_address = '0x0000000000000000000000000000000000000802'
abi = [{"inputs": [{"internalType": "bytes", "name": "keys", "type": "bytes"}],
        "name": "setKeys", "outputs": [], "stateMutability": "nonpayable", "type": "function"}]
contract = w3.eth.contract(address=key_manager_address, abi=abi)

# TODO: add your address and private key AND SESSION KEY.
my_address = addy
private_key = pk
session_keys = session_key

nonce = w3.eth.get_transaction_count(my_address)

gas = w3.eth.gas_price
print(gas)
print(gas*5)
txn = contract.functions.setKeys(session_keys).build_transaction({
    'chainId': 8408,
    'gas': 20000000,
    'gasPrice': gas*5,
    'nonce': nonce,
})

signed_txn = w3.eth.account.sign_transaction(txn, private_key)
tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print(f"Transaction : {tx_receipt.blockNumber}")
print(f"Hash : {tx_receipt.transactionHash.hex()}")
