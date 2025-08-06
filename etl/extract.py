from datetime import datetime

from common.config import Api
from common.logger import setup_logger
from model.block import Block
from model.transaction import Transaction
from util.utils import api_builder, fetch_json, fetch_text

logger = setup_logger(__name__)


def get_block_hash_by_height(height_of_block: int) -> str:
    """
    Returns the hash of the block at the given height.

    Parameters:
        height_of_block (int): The height of the block.

    Returns:
        str: The hash of the block.

    Raises:
        requests.exceptions.HTTPError: If the HTTP request returns an unsuccessful status code.
    """
    logger.debug(f"Getting block hash at height {height_of_block}.")
    return fetch_text(api_builder(Api.BLOCK_BY_HEIGHT, height_of_block))


def get_block_by_timestamp(timestamp: int) -> Block:
    """
    Returns the block closest to the given timestamp.

    Parameters:
        timestamp (int): The current timestamp.

    Returns:
        Block: The block closest to the given timestamp.

    Raises:
        requests.exceptions.HTTPError: If the HTTP request returns an unsuccessful status code.
    """
    logger.debug(
        f"Getting block closest to timestamp {datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')}."
    )
    json_response = fetch_json(api_builder(Api.BLOCK_BY_TIMESTAMP, timestamp))
    logger.debug(f"Got block meta at height {json_response["height"]}.")
    return Block.model_validate(get_block_by_hash(json_response["hash"]))


def get_block_by_hash(hash_of_block: str) -> Block:
    """
    Returns the details of the block with the given hash.

    Parameters:
        hash_of_block (str): The hash of the block.

    Returns:
        Block: The details of the block.

    Raises:
        requests.exceptions.HTTPError: If the HTTP request returns an unsuccessful status code.
    """
    logger.debug(f"Getting block by hash {hash_of_block}.")
    return Block.model_validate(
        fetch_json(api_builder(Api.BLOCK_BY_HASH, hash_of_block))
    )


def get_block_by_height(height_of_block: int) -> Block:
    """
    Returns the details of the block at the given height.

    Parameters:
        height_of_block (int): The height of the block.

    Returns:
        Block: The details of the block.

    Raises:
        requests.exceptions.HTTPError: If the HTTP request returns an unsuccessful status code.
    """
    logger.debug(f"Getting block at height {height_of_block}.")
    block_hash = get_block_hash_by_height(height_of_block)
    return Block.model_validate(get_block_by_hash(block_hash))


def get_block_batch(start_height: int = None) -> list[Block]:
    """
    Retrieve a list of block details.
    With no start_height specified, the 15 most recent blocks are returned.
    If start_height is specified, the 15 blocks before (and including) start_height are returned.

    Parameters:
        start_height (int): The height of the first block to retrieve.

    Returns:
        list: A list of block details.

    Raises:
        requests.exceptions.HTTPError: If the HTTP request returns an unsuccessful status code.
    """
    if start_height is None:
        logger.debug(f"Getting 10 latest blocks.")
        response = fetch_json(api_builder(Api.BLOCKS))
    else:
        logger.debug(
            f"Getting blocks between height {start_height} and {start_height - 9}."
        )
        response = fetch_json(api_builder(Api.BLOCKS, start_height))

    return [Block.model_validate(block) for block in response]


def get_transaction_ids(hash_of_block: str) -> list[str]:
    """
    Returns a list of transaction IDs in the block.

    Parameters:
        hash_of_block (str): The hash of the block.

    Returns:
        list: A list of all transaction IDs in the block.

    Raises:
        requests.exceptions.HTTPError: If the HTTP request returns an unsuccessful status code.
    """
    logger.debug(f"Getting all transaction IDs from block by hash {hash_of_block}.")
    return list(
        fetch_json(api_builder(Api.BLOCK_BY_HASH, hash_of_block, Api.TX_IDS_SEGMENT))
    )


def get_transactions_batch(
    hash_of_block: str, start_index: int = 0
) -> list[Transaction]:
    """
    Returns a list of transactions in the block (up to 10 transactions beginning at start_index).

    Parameters:
        hash_of_block (str): The hash of the block.
        start_index (int): The index of the first transaction to retrieve.

    Returns:
        list: The transactions of the block (up to 10 transactions beginning at start_index).

    Raises:
        requests.exceptions.HTTPError: If the HTTP request returns an unsuccessful status code.
    """
    logger.debug(
        f"Getting transactions from block from index {start_index} to index {start_index + 9}."
    )
    response = fetch_json(
        api_builder(Api.BLOCK_BY_HASH, hash_of_block, Api.TXS_SEGMENTS, start_index)
    )
    return [Transaction.model_validate(transaction) for transaction in response]


def get_all_transactions_from_block(hash_of_block: str) -> list[Transaction]:
    """
    Returns a list of all transactions in the block.

    Parameters:
        hash_of_block (str): The hash of the block.

    Returns:
        list: All transactions of the block.

    Raises:
        requests.exceptions.HTTPError: If the HTTP request returns an unsuccessful status code.
    """
    logger.debug(f"Getting all transactions from block by hash {hash_of_block}.")
    all_transactions = []
    block = get_block_by_hash(hash_of_block)
    logger.info(
        f"Fetching {block.tx_count} transactions from block at height {block.height}."
    )
    for i in range(0, block.tx_count, 10):
        transactions = get_transactions_batch(hash_of_block, i)
        all_transactions.extend(transaction for transaction in transactions)
    return all_transactions
