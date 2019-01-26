import hashlib, json
from web3 import Web3, HTTPProvider


def smart_contract_client(data=None, action=None):
    # Config
    contract_address = "0xc8e1b28e25fef2a9d033444a65812f6603a7f1aa"
    wallet_private_key = \
        "AC1D521FA63AF1CFE096DF122F9DF0D145E0E075E5A8CFD09292E4063617FA79"
    wallet_address = "0xB4cC8674B704430ce7A038279B866F346AE54B4c"
    w3 = Web3(HTTPProvider("https://ropsten.infura.io/v3/54622322365945b4a9c1102db9dd0559"))
    contract_address = w3.toChecksumAddress(contract_address)
    w3.eth.DefaultAccount = "0xb4cc8674b704430ce7a038279b866f346ae54b4c"
    # Contract setup
    with open('abi.json') as f:
        json_abi = json.load(f)
    """
    Data_storage = w3.eth.contract(abi=json_abi["abi"],
                                   bytecode=json.dumps(json_abi["bin"]))
    tx_hash = Data_storage.constructor().transact()
    """
    contract = w3.eth.contract(address=contract_address, abi=json_abi["abi"])
    nonce = w3.eth.getTransactionCount(wallet_address)

    block_hash = hashlib.sha256(data.encode("utf-8")).hexdigest()
    if action.lower() == 'store':
        #print(contract.functions.Greeter().call())
        txn_dict = contract.functions.setdata("hello").buildTransaction({
        'chainId': 3,
        'gas': 140000,
        'nonce':nonce})
        signed_txn = w3.eth.account.signTransaction(txn_dict,
                                                    private_key=wallet_private_key)
        result = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        w3.eth.waitForTransactionReceipt(result)
        print(result)
        return result
    if action.lower() == 'verify':
        transaction_hash = w3.eth.functions.getresult().transact()
        print(transaction_hash)
        return transaction_hash

if __name__ == "__main__":
    smart_contract_client(data="abc", action="store")