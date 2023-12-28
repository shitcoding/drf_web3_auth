import hashlib
import json
import os
from datetime import timedelta

from django.utils import timezone
from dotenv import load_dotenv
from eth_account import Account
from eth_account.messages import encode_defunct

load_dotenv()


def make_unique_id(eth_address, timestamp, server_secret):
    return hashlib.sha256(
        f'{eth_address}{timestamp}{server_secret}'.encode()
    ).hexdigest()


def generate_message(eth_address):
    timestamp = timezone.now()
    expiration_time = timestamp + timedelta(hours=1)
    server_secret = os.getenv('SERVER_SECRET', 'wow-so-secret')
    unique_id = make_unique_id(eth_address, timestamp, server_secret)

    message_content = {
        'timestamp': timestamp.isoformat(),
        'expiration_time': expiration_time.isoformat(),
        'unique_id': unique_id,
    }
    message = json.dumps(message_content)
    return {
        'eth_address': eth_address,
        'message': message,
    }


def verify_signature(eth_address, message, signature):
    message_content = json.loads(message)
    message_encoded = encode_defunct(text=message)
    signer_address = Account.recover_message(
        message_encoded, signature=signature
    )

    is_valid_signature = signer_address.lower() == eth_address.lower()
    is_valid_time = timezone.now() <= timezone.datetime.fromisoformat(
        message_content['expiration_time']
    )
    expected_unique_id = make_unique_id(
        eth_address,
        timezone.datetime.fromisoformat(message_content['timestamp']),
        os.getenv('SERVER_SECRET'),
    )
    is_valid_id = expected_unique_id == message_content['unique_id']

    return is_valid_signature and is_valid_time and is_valid_id
