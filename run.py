from etl.extract import *
from etl.load import *
from db.database import *
from datetime import datetime


def main():
    # ONLY FOR TESTING, WILL BE REMOVED
    # TEST ALL EXTRACT FUNCTIONS

    # x = get_block_hash_by_height(908_828)
    # x = get_block_by_timestamp(int(datetime(2025, 8, 6, 8, 21, 15).timestamp()))
    # x = get_block_by_height(908_828)
    # x = get_block_by_hash("000000000000000000004a11a235b41ae037218d1bd31a4738ce1c7f57624fea")
    # x = get_block_batch()
    # x = get_block_batch(908_828)
    # x = get_transaction_ids("000000000000000000004a11a235b41ae037218d1bd31a4738ce1c7f57624fea")
    # x = get_transactions_batch("000000000000000000004a11a235b41ae037218d1bd31a4738ce1c7f57624fea")
    # x = get_all_transactions_from_block("000000000000000000004a11a235b41ae037218d1bd31a4738ce1c7f57624fea")

    create_tables()

    try:
        block_hash = get_block_hash_by_height(908_828)
        block = get_block_by_hash(block_hash)
        insert_block(block, DB_NAME)
        txs = get_all_transactions_from_block(block_hash)
        for tx in txs:
            insert_transaction(tx, DB_NAME)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
