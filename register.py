from web3 import Web3
from web3.types import Wei
import os
import dotenv

dotenv.load_dotenv()


if not 'PK' in os.environ or not 'ADDRESS' in os.environ or not 'SESSION_KEY' in os.environ:
    raise ValueError("Fill in all environment variables")

pk = os.getenv('PK')
addy = os.getenv('ADDRESS')
session_key = os.getenv('SESSION_KEY')

NATIVE_STAKING_ADDRESS = '0x0000000000000000000000000000000000000800'
NATIVE_STAKING_ABI = [
    {
        "inputs": [
            {"type": "uint256", "name": "value"},
            {"type": "uint8", "name": "dest"}
        ],
        "name": "bondWithRewardDestination",
        "type": "function",
        "stateMutability": "nonpayable",
        "outputs": []
    },
    {
        "inputs": [
            {"type": "uint32", "name": "commission"},
            {"type": "bool", "name": "blocked"}
        ],
        "name": "validate",
        "type": "function",
        "stateMutability": "nonpayable",
        "outputs": []
    }
]

RPC_URL = 'http://localhost:9944'
# TODO: add your private key here
PRIVATE_KEY = pk
AMOUNT_TO_STAKE = Wei(Web3.to_wei(1, 'ether'))


async def stake_and_validate():
    w3 = Web3(Web3.HTTPProvider(RPC_URL))

    from web3.exceptions import ExtraDataLengthError
    try:
        w3.eth.get_block('latest')
    except ExtraDataLengthError:
        from web3.middleware import validation
        validation.METHODS_TO_VALIDATE = []

    account = w3.eth.account.from_key(PRIVATE_KEY)
    print(f"Account address: {account.address}")

    contract = w3.eth.contract(
        address=NATIVE_STAKING_ADDRESS,
        abi=NATIVE_STAKING_ABI
    )

    try:
        print("Attempting to bond tokens...")
        try:
            gas_price = w3.eth.gas_price
        except Exception:
            gas_price = w3.eth.generate_gas_price() or w3.eth.gas_price

        bond_tx = contract.functions.bondWithRewardDestination(
            AMOUNT_TO_STAKE,
            0
        ).build_transaction({
            'from': account.address,
            'nonce': w3.eth.get_transaction_count(account.address),
            'gas': 2000000,
            'gasPrice': gas_price,
            'chainId': w3.eth.chain_id
        })

        signed_bond_tx = w3.eth.account.sign_transaction(bond_tx, PRIVATE_KEY)
        print("Bonding tokens...")
        # print(signed_bond_tx.raw_transaction)
        bond_tx_hash = w3.eth.send_raw_transaction(
            signed_bond_tx.raw_transaction)

        bond_receipt = w3.eth.wait_for_transaction_receipt(bond_tx_hash)

        print("Tokens bonded successfully.")

        print("Activating as validator...")

        validate_tx = contract.functions.validate(
            0,
            False
        ).build_transaction({
            'from': account.address,
            'nonce': w3.eth.get_transaction_count(account.address),
            'gas': 2000000,
            'gasPrice': gas_price,
            'chainId': w3.eth.chain_id
        })

        signed_validate_tx = w3.eth.account.sign_transaction(
            validate_tx, PRIVATE_KEY)
        validate_tx_hash = w3.eth.send_raw_transaction(
            signed_validate_tx.raw_transaction)
        validate_receipt = w3.eth.wait_for_transaction_receipt(
            validate_tx_hash)

        print("Activated as validator successfully.")

    except Exception as error:
        print("An error occurred:", str(error))
        if "AlreadyBonded" in str(error):
            print("Account is already bonded. You may need to use a different function to increase your stake or become a validator.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(stake_and_validate())
