from web3 import Web3
import os
import dotenv

dotenv.load_dotenv()


if not 'PK' in os.environ or not 'ADDRESS' in os.environ or not 'SESSION_KEY' in os.environ:
    raise ValueError("Fill in all environment variables")

pk = os.getenv('PK')
addy = os.getenv('ADDRESS')
session_key = os.getenv('SESSION_KEY')

# Configuration
RPC_URL = 'http://localhost:9944'

# TODO: add your address and private key
MY_ADDRESS = addy
PRIVATE_KEY = pk
CHAIN_ID = 8408

# Connection to the node
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# Address and ABI of the NativeStaking contract
NATIVE_STAKING_ADDRESS = '0x0000000000000000000000000000000000000800'
NATIVE_STAKING_ABI = [
    {
        'inputs': [{'internalType': 'uint256', 'name': 'value', 'type': 'uint256'}],
        'name': 'bondExtra',
        'outputs': [],
        'stateMutability': 'nonpayable',
        'type': 'function'
    },
    {
        'inputs': [{'internalType': 'uint32', 'name': 'commission', 'type': 'uint32'},
                   {'internalType': 'bool', 'name': 'blocked', 'type': 'bool'}],
        'name': 'validate',
        'outputs': [],
        'stateMutability': 'nonpayable',
        'type': 'function'
    },
    {
        'inputs': [{'internalType': 'address', 'name': 'stash', 'type': 'address'}],
        'name': 'bonded',
        'outputs': [{'internalType': 'bool', 'name': '', 'type': 'bool'}],
        'stateMutability': 'view',
        'type': 'function'
    },
    {
        'inputs': [{'internalType': 'address', 'name': 'stash', 'type': 'address'}],
        'name': 'stake',
        'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'},
                    {'internalType': 'uint256', 'name': '', 'type': 'uint256'}],
        'stateMutability': 'view',
        'type': 'function'
    },
    {
        'inputs': [],
        'name': 'activeEra',
        'outputs': [{'internalType': 'uint256', 'name': '', 'type': 'uint256'}],
        'stateMutability': 'view',
        'type': 'function'
    },
    {
        'inputs': [{'internalType': 'address', 'name': 'who', 'type': 'address'}],
        'name': 'status',
        'outputs': [{'internalType': 'uint8', 'name': '', 'type': 'uint8'}],
        'stateMutability': 'view',
        'type': 'function'
    }
]

# Instantiation of the contract
staking_contract = w3.eth.contract(
    address=NATIVE_STAKING_ADDRESS, abi=NATIVE_STAKING_ABI)


def send_transaction(func):
    transaction = func.build_transaction({
        'chainId': CHAIN_ID,
        'gas': 2000000,
        'gasPrice': w3.eth.gas_price,
        'nonce': w3.eth.get_transaction_count(MY_ADDRESS),
    })

    signed_txn = w3.eth.account.sign_transaction(
        transaction, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)

    print(f"Transaction sent. Hash: {tx_hash.hex()}")

    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    print(tx_receipt)

    if tx_receipt['status'] == 1:
        print("Transaction successful!")
    else:
        print("Transaction failed.")

    return tx_hash


def increase_stake(additional_stake_zcx):
    additional_stake_wei = int(additional_stake_zcx * 10**18)
    print(f"Adding {additional_stake_zcx} ZCX to existing stake...")
    bond_extra_function = staking_contract.functions.bondExtra(
        additional_stake_wei)
    send_transaction(bond_extra_function)


def validate(commission_rate=10_000_000, blocked=False):  # commission 10_000_000 = 1%
    print(f"Activating as validator with 1% commission...")
    validate_function = staking_contract.functions.validate(
        commission_rate, blocked)
    send_transaction(validate_function)


def check_bonded(address):
    return staking_contract.functions.bonded(address).call()


def check_stake(address):
    total_stake, active_stake = staking_contract.functions.stake(
        address).call()
    return total_stake, active_stake


def check_active_era():
    return staking_contract.functions.activeEra().call()


def check_validator_status(address):
    status = staking_contract.functions.status(address).call()
    status_meanings = {
        0: "Not staking",
        1: "Nominator",
        2: "Validator waiting",
        3: "Validator active"
    }
    return status_meanings.get(status, f"Unknown status: {status}")


def show_menu():
    print("\n--- Zenchain Staking Menu --- by KrimDev")
    print("1. Show stake balance")
    print("2. Increase stake")
    print("3. Activate as validator or update commission (1%)")
    print("4. Check active era and validator status")
    print("5. Exit")
    return input("Choose an option: ")


def main():
    while True:
        choice = show_menu()
        if choice == '1':
            is_bonded = check_bonded(MY_ADDRESS)
            if is_bonded:
                print("You are bonded.")
                total_stake, active_stake = check_stake(MY_ADDRESS)
                
                print(f"Your stake balance: Total Stake = { total_stake/10**18} ZCX, Active Stake = {active_stake/10**18} ZCX")
            else:
                print("You are not bonded.")
        elif choice == '2':
            amount = float(input("Enter amount of ZCX to add to stake: "))
            increase_stake(amount)
        elif choice == '3':
            validate()  # Uses 1% commission by default and doesn't block nominations
        elif choice == '4':
            active_era = check_active_era()
            validator_status = check_validator_status(MY_ADDRESS)
            print(f"Active Era: {active_era}")
            print(f"Your validator status: {validator_status}")
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
