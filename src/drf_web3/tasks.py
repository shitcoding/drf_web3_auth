import logging
import time
from datetime import datetime

from celery import shared_task
from django.conf import settings
from django.utils import timezone
from web3 import Web3, exceptions
from web3.middleware import geth_poa_middleware

from drf_web3.models import Event

logger = logging.getLogger(__name__)

# TODO: Move to separate utils module
def retrieve_last_processed_block():
    # Retrieve the last processed block number from a persistent store
    # TODO: Placeholder: return from a file or database
    return 20437731


# TODO: Move to separate utils module
def update_last_processed_block(block_number):
    # Update the last processed block number in a persistent store
    # TODO: Placeholder: save to a file or database
    pass


def init_w3(node_url):
    w3 = Web3(Web3.HTTPProvider(node_url))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return w3


def init_contract(w3, address, abi):
    contract = w3.eth.contract(
        address=Web3.to_checksum_address(address),
        abi=abi,
    )
    return contract


def fetch_events(contract, from_block):
    try:
        events = contract.events.Transfer().get_logs(fromBlock=from_block)
        return events
    except exceptions.Web3Exception as e:
        logger.error(f'Error fetching events {e}')
        return []


@shared_task
def fetch_and_save_events():
    w3 = init_w3(settings.POLYGON_NODE_URL)
    contract = init_contract(
        w3,
        settings.CONTRACT_ADDRESS,
        settings.CONTRACT_ABI,
    )

    last_processed_block = (
        20437731  # TODO: Retrieve this from a persistent storage
    )

    try:
        events = fetch_events(contract, last_processed_block + 1)
        saved_events_count = 0
        for event in events:
            tx_hash = event.transactionHash.hex()
            if not Event.objects.filter(tx_hash=tx_hash).exists():
                Event.objects.create(
                    tx_hash=tx_hash,
                    from_address=event.args['from'],
                    to_address=event.args['to'],
                    value=event.args['value'],
                    created_at=timezone.make_aware(
                        datetime.fromtimestamp(
                            w3.eth.get_block(event.blockNumber).timestamp
                        ),
                        timezone.get_default_timezone(),
                    ),
                )
                saved_events_count += 1
        if saved_events_count:
            logger.info(f'{saved_events_count} new events fetched and saved successfully.')
        last_processed_block = events[-1].blockNumber if events else last_processed_block
            # update_last_processed_block(last_processed_block) # TODO: save to persistent storage
        time.sleep(settings.EVENT_FETCH_INTERVAL)

    except exceptions.Web3Exception as e:
        logger.error(f'Error fetching events: {e}')
        # TODO: Implement exponential backoff
