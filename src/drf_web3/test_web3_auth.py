import os

import requests
from dotenv import load_dotenv
from eth_account.messages import encode_defunct
from web3 import Web3
from web3.middleware import geth_poa_middleware

# Get env vars from .env file
load_dotenv()

headers = {}

# Dummy test ETH address / private_key
ADDRESS = '0x1232D846f11735E6A3f030a9A8E5a6c2Dd418baC'
PK = '0xa3e6ae2f358b7ea8dde4aa613d0556d8208bf9a4c716c57eb1feb521fdb86a07'

POLYGON_NODE_URL = os.getenv('POLYGON_NODE_URL')

message_resp = requests.get(f'http://localhost:8000/api/message/{ADDRESS}')
MESSAGE = message_resp.json()['message']
print(f'{MESSAGE=}')

w3 = Web3(Web3.HTTPProvider(POLYGON_NODE_URL))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

message_encoded = encode_defunct(text=MESSAGE)
signed_message = w3.eth.account.sign_message(message_encoded, private_key=PK)

signature = Web3.to_hex(signed_message['signature'])

print(f'\n{signature=}\n')

json_data = {
    'eth_address': ADDRESS,
    'message': MESSAGE,
    'signature': signature,
}

jwt_response = requests.post(
    'http://localhost:8000/api/auth/web3/', headers=headers, json=json_data
)

print(jwt_response.json())
jwt_access_token = jwt_response.json()['access']


jwt_headers = {'Authorization': f'Bearer {jwt_access_token}'}
events_resp = requests.get(
    'http://localhost:8000/api/events', headers=jwt_headers
)
print(events_resp.json())
