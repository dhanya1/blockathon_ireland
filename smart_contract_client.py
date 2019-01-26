import hashlib, json
from web3 import Web3, HTTPProvider


def smart_contract_client(data=None, action=None):
    # Config
    contract_address = "0xd20e61cacd1c790af88c51a75eb596e299fdfb1f"
    wallet_private_key = \
        "AC1D521FA63AF1CFE096DF122F9DF0D145E0E075E5A8CFD09292E4063617FA79"
    wallet_address = "0xB4cC8674B704430ce7A038279B866F346AE54B4c"
    w3 = Web3(HTTPProvider("https://mainnet.infura.io/v3/54622322365945b4a9c1102db9dd0559"))
    contract_address = w3.toChecksumAddress(contract_address)
    w3.eth.DefaultAccount = "0xB4cC8674B704430ce7A038279B866F346AE54B4c"
    # Contract setup
    with open('abi.json') as f:
        json_abi = json.load(f)
    Data_storage = w3.eth.contract(abi=json_abi["abi"],
                                   bytecode=json_abi["bin"])
    contract = w3.eth.contract(address=contract_address, abi=json_abi["abi"])
    tx_hash = Data_storage.constructor().transact()
    block_hash = hashlib.sha256(data.encode("utf-8")).hexdigest()
    if action.lower() == 'store':
        transaction_hash = contract.functions.set("hello").transact()
        w3.eth.waitForTransactionReceipt(transaction_hash)
        print(transaction_hash)
        return transaction_hash
    if action.lower() == 'verify':
        transaction_hash = w3.eth.functions.getresult().transact()
        print(transaction_hash)
        return transaction_hash

if __name__ == "__main__":
    smart_contract_client(data="abc", action="store")