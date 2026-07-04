from web3 import Web3
from dotenv import load_dotenv
import os

load_dotenv()
w3 = Web3(Web3.HTTPProvider(os.getenv("MONAD_RPC_URL")))
code = w3.eth.get_code(os.getenv("CONTRACT_ADDRESS"))
print("Bytecode length at this address:", len(code))