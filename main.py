from etl.extract import *
from etl.load import *
from db.database import *


def main():
    create_tables()

    # ONLY FOR TESTING, WILL BE REMOVED
    try:
        block_hash = get_block_hash_by_height(900_000)
        block = get_block_by_hash(block_hash)
        insert_block(block, DB_NAME)
        txs = get_all_transactions_from_block(block_hash)
        for tx in txs:
            insert_transaction(tx, DB_NAME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
