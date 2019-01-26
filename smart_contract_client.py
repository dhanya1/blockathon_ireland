import hashlib, json
from web3 import Web3, HTTPProvider
from hexbytes import HexBytes


def smart_contract_client(data=None, action=None, txn_id=None):
    # Config
    contract_address = "0xf2361594359febce37ea295f2e1707d299028f9c"
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
    if action.lower() == 'store':
        contract = w3.eth.contract(address=contract_address,
                                   abi=json_abi["abi"])
        nonce = w3.eth.getTransactionCount(wallet_address)
        txn_dict = {
            'data': data,
            'gas': 2000000,
            'nonce': nonce,
            'chainId': 3,
            'gasPrice': w3.toWei('400', 'gwei')
        }
        signed_txn = w3.eth.account.signTransaction(txn_dict,
                                                    wallet_private_key)
        txn_hash_1 = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        w3.eth.waitForTransactionReceipt(txn_hash_1)
        txn_hash = w3.eth.getTransactionReceipt(txn_hash_1)
        return txn_hash['transactionHash'].hex()
        """
        txn_dict = contract.functions.setdata(block_hash).buildTransaction({
        'chainId': 3,
        'gas': 140000,
        'nonce':nonce})
        signed_txn = w3.eth.account.signTransaction(txn_dict,
                                                    private_key=wallet_private_key)
        result = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        w3.eth.waitForTransactionReceipt(result)
        txn_hash = w3.eth.getTransactionReceipt(result)
        print(txn_hash)
        return txn_hash
        """
    if action.lower() == 'verify':
        result = w3.eth.getTransaction(txn_id)['input']
        verification_string = '0x'+ data
        if result == verification_string:
            return True
        else:
            return False
        """
        txn_dict = contract.functions.getresult(block_hash).buildTransaction({
        'chainId': 3,
        'gas': 140000,
        'nonce':nonce})
        signed_txn = w3.eth.account.signTransaction(txn_dict,
                                                    private_key=wallet_private_key)
        result = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        w3.eth.waitForTransactionReceipt(result)
        txn_hash = w3.eth.getTransactionReceipt(result)
        print(txn_hash)
        return result
        """



if __name__ == "__main__":
    smart_contract_client(data="blahhhjhh", action="store")
    """
    smart_contract_client(
        data="blah", action="verify",
        txn_id="0x9d53b42a7230be1875483eaf1762414bbba3422d49f386459fc531b70992b4cf")
    """