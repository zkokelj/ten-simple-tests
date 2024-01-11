import json

import requests
from eth_account.messages import encode_typed_data
from web3 import Web3
from eth_account import Account


def join(url):
    response = requests.get(url)
    if response.status_code != 200:
        exit(2)
    return response.text


def register(url, encryptionToken, account):
    domain = {
        'name': 'Ten',
        'version': '1.0',
        'chainId': 443,
    }

    message = {
        'Encryption Token': "0x" + encryptionToken,
    }

    types = {
        'EIP712Domain': [
            {'name': 'name', 'type': 'string'},
            {'name': 'version', 'type': 'string'},
            {'name': 'chainId', 'type': 'uint256'},
        ],
        'Authentication': [  # EIP712Type
            {'name': 'Encryption Token', 'type': 'address'},
        ],
    }

    # Create the typed data
    typed_data = {
        'types': types,
        'domain': domain,
        'primaryType': 'Authentication',  # EIP712Type
        'message': message,
    }

    encoded_data = encode_typed_data(full_message=typed_data)
    signature = account.sign_message(encoded_data)

    data = {"signature": signature.signature.hex(), "address": account.address}
    headers = {
        "Content-Type": "application/json; charset=UTF-8"
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    response_text = response.text
    print("Authentication response: ", response_text)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    base_url = "https://testnet.ten.xyz"

    join_url = f"{base_url}/v1/join"
    encryptionToken = join(join_url)
    print("Encryption token is: ", encryptionToken)

    acc = Account.create()
    print("address: ", acc.address)

    register_url = f"{base_url}/v1/authenticate/?token={encryptionToken}"
    register(register_url, encryptionToken, acc)

    web3 = Web3(Web3.HTTPProvider('%s/v1/?token=%s' % (base_url, encryptionToken)))
    # web3 = Web3(Web3.WebsocketProvider('%s/v1/?token=%s' % ("wss://testnet.ten.xyz:81", encryptionToken)))

    latest_block = web3.eth.get_block_number()
    print("Latest block is: ", latest_block)

    balance = web3.eth.get_balance(acc.address)
    print("Balance is: ", balance)
