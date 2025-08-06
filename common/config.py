from enum import Enum


# API
class Api(Enum):
    BLOCK_BY_TIMESTAMP = "v1/mining/blocks/timestamp/"
    BLOCK_BY_HASH = "block/"
    BLOCK_BY_HEIGHT = "block-height/"
    BLOCKS = "blocks/"
    TXS_SEGMENTS = "/txs/"
    TX_IDS_SEGMENT = "/txids/"


BASE_URL = "http://umbrel.local:3006/api/"

# HTTP
DEFAULT_TIMEOUT = 10

# Logging
LOGGER_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

# Database
DB_NAME = "bitcoin_etl.db"
TABLE_BLOCKS = "blocks"
TABLE_EXTRAS = "extras"
TABLE_FEE_RANGE = "fee_range"
TABLE_COINBASE_ADDRESSES = "coinbase_addresses"
TABLE_POOLS = "pools"
TABLE_MINERS = "miners"
TABLE_TRANSACTIONS = "transactions"
TABLE_TX_INPUTS = "tx_inputs"
TABLE_TX_OUTPUTS = "tx_outputs"
TABLE_WITNESSES = "witnesses"
