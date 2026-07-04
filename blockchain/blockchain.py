# blockchain.py
from web3 import Web3
from dotenv import load_dotenv
import os, json

load_dotenv()
w3 = Web3(Web3.HTTPProvider(os.getenv("MONAD_RPC_URL")))

BASE_DIR = os.path.dirname(__file__)

with open(os.path.join(BASE_DIR, "abi.json")) as f:
    abi = json.load(f)

contract = w3.eth.contract(address=os.getenv("CONTRACT_ADDRESS"), abi=abi)
account = w3.eth.account.from_key(os.getenv("PRIVATE_KEY"))

def record_achievement(agent_address: str, task: str, score: int, feedback: str) -> str:
    tx = contract.functions.recordAchievement(agent_address, task, score, feedback).build_transaction({
        "from": account.address,
        "nonce": w3.eth.get_transaction_count(account.address),
        "gasPrice": w3.eth.gas_price,
    })
    estimated_gas = w3.eth.estimate_gas(tx)
    tx["gas"] = int(estimated_gas * 1.2)  # 20% safety buffer
    signed = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    w3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_hash.hex()

def get_achievements(agent_address: str):
    return contract.functions.getAchievements(agent_address).call()

def get_stats(agent_address: str):
    items = get_achievements(agent_address)
    if not items:
        return {"count": 0, "average": 0}
    scores = [a[1] for a in items]
    return {"count": len(scores), "average": round(sum(scores) / len(scores), 1)}

if __name__ == "__main__":
    tx = record_achievement(account.address, "Python Test Task", 91, "Clean and correct.")
    print("Transaction sent:", tx)
    print("Stats:", get_stats(account.address))