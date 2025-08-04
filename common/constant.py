# API
MEMPOOL_SPACE_API_BASE_URL = 'http://umbrel.local:3006/api/'

BLOCK_BY_TIMESTAMP_URL = MEMPOOL_SPACE_API_BASE_URL + 'v1/mining/blocks/timestamp/'
BLOCK_BY_HASH_URL = MEMPOOL_SPACE_API_BASE_URL + 'block/'
BLOCK_BY_HEIGHT_URL = MEMPOOL_SPACE_API_BASE_URL + 'block-height/'
BLOCKS_URL = MEMPOOL_SPACE_API_BASE_URL + 'blocks/'
TRANSACTION_POSTFIX = '/txs/'
TRANSACTION_IDS_POSTFIX = '/txids/'

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
