from web3 import Web3
import os, json
from dotenv import load_dotenv

# Get the directory of the current script
base_dir = os.path.dirname(os.path.abspath(__file__))
# Load .env from the parent directory
load_dotenv(os.path.join(base_dir, "..", ".env"))

w3 = Web3(Web3.HTTPProvider(os.getenv("MONAD_RPC_URL")))
account = w3.eth.account.from_key(os.getenv("PRIVATE_KEY"))

with open(os.path.join(base_dir, "abi.json")) as f:
    abi = json.load(f)
with open(os.path.join(base_dir, "bytecode.txt")) as f:
    bytecode = f.read().strip()

Contract = w3.eth.contract(abi=abi, bytecode=bytecode)

tx = Contract.constructor().build_transaction({
    "from": account.address,
    "nonce": w3.eth.get_transaction_count(account.address),
    "gas": 3000000,
    "gasPrice": w3.eth.gas_price,
})

signed = account.sign_transaction(tx)
tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print("Contract deployed at:", receipt.contractAddress)