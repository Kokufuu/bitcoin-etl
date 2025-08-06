import sqlite3
from contextlib import contextmanager

from common.config import (
    DB_NAME,
    TABLE_BLOCKS,
    TABLE_COINBASE_ADDRESSES,
    TABLE_EXTRAS,
    TABLE_FEE_RANGE,
    TABLE_MINERS,
    TABLE_POOLS,
    TABLE_TRANSACTIONS,
    TABLE_TX_INPUTS,
    TABLE_TX_OUTPUTS,
    TABLE_WITNESSES,
)
from common.logger import setup_logger
from model.block import Block
from model.transaction import Transaction

logger = setup_logger(__name__)


@contextmanager
def db_cursor(schema_name=DB_NAME):
    conn = sqlite3.connect(schema_name)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    try:
        yield conn, cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


def batch_insert(cursor: sqlite3.Cursor, table_name: str, columns: list[str], values: list[tuple]):
    placeholders = ", ".join(["?"] * len(columns))
    col_str = ", ".join(columns)
    cursor.executemany(
        f"INSERT OR REPLACE INTO {table_name} ({col_str}) VALUES ({placeholders})",
        values,
    )


def insert_block(block: Block, schema_name: str = DB_NAME) -> None:
    """Inserts all details of a block into the database.

    Parameters:
        block (Block): The block to insert.
        schema_name (str): The name of the database schema to use.
    """
    try:
        with db_cursor(schema_name) as (conn, cursor):
            cursor.execute(
                f"""
                INSERT OR REPLACE INTO {TABLE_BLOCKS} (
                    id, height, version, timestamp, bits, nonce, difficulty, merkle_root,
                    tx_count, size, weight, previous_block_hash, median_time
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    block.id,
                    block.height,
                    block.version,
                    block.timestamp,
                    block.bits,
                    block.nonce,
                    block.difficulty,
                    block.merkle_root,
                    block.tx_count,
                    block.size,
                    block.weight,
                    block.previous_block_hash,
                    block.median_time,
                ),
            )
            logger.debug(f"Block {block.height} inserted into table '{TABLE_BLOCKS}'.")

            cursor.execute(
                f"""
                INSERT OR REPLACE INTO {TABLE_EXTRAS} (
                    height, header, reward, median_fee, total_fees, avg_fee, avg_fee_rate,
                    coinbase_raw, coinbase_address, coinbase_signature, utxo_set_change,
                    avg_tx_size, total_inputs, total_outputs, total_output_amt, segwit_total_txs,
                    segwit_total_size, segwit_total_weight, virtual_size, similarity
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    block.height,
                    block.extras.header,
                    block.extras.reward,
                    block.extras.median_fee,
                    block.extras.total_fees,
                    block.extras.avg_fee,
                    block.extras.avg_fee_rate,
                    block.extras.coinbase_raw,
                    block.extras.coinbase_address,
                    block.extras.coinbase_signature,
                    block.extras.utxo_set_change,
                    block.extras.avg_tx_size,
                    block.extras.total_inputs,
                    block.extras.total_outputs,
                    block.extras.total_output_amt,
                    block.extras.segwit_total_txs,
                    block.extras.segwit_total_size,
                    block.extras.segwit_total_weight,
                    block.extras.virtual_size,
                    block.extras.similarity,
                ),
            )
            logger.debug(f"Extras for block {block.height} inserted into table '{TABLE_EXTRAS}'.")

            batch_insert(
                cursor,
                TABLE_FEE_RANGE,
                ["height", "fee"],
                [(block.height, fee) for fee in block.extras.fee_range],
            )
            logger.debug(
                f"Fee range for block {block.height} inserted into table '{TABLE_FEE_RANGE}'."
            )

            batch_insert(
                cursor,
                TABLE_COINBASE_ADDRESSES,
                ["height", "address"],
                [(block.height, address) for address in block.extras.coinbase_addresses],
            )
            logger.debug(
                f"Coinbase addresses for block {block.height}"
                f" inserted into table '{TABLE_COINBASE_ADDRESSES}'."
            )

            cursor.execute(
                f"""
                INSERT OR REPLACE INTO {TABLE_POOLS} (height, id, name, slug)
                VALUES (?, ?, ?, ?)
            """,
                (
                    block.height,
                    block.extras.pool.id,
                    block.extras.pool.name,
                    block.extras.pool.slug,
                ),
            )
            logger.debug(f"Extras for block {block.height} inserted into table '{TABLE_POOLS}'.")

            if block.extras.pool.miner_names is not None:
                batch_insert(
                    cursor,
                    TABLE_MINERS,
                    ["height", "name"],
                    [(block.height, miner_name) for miner_name in block.extras.pool.miner_names],
                )
                logger.debug(
                    f"Miner names for block {block.height} inserted into table '{TABLE_MINERS}'."
                )

            logger.info(f"Block {block.height} inserted into database.")

    except Exception as e:
        logger.error(f"Error while inserting block into database: {e}")
        raise


def insert_transaction(tx: Transaction, schema_name: str = DB_NAME) -> None:
    """
    Insert all details of a transaction into the database.

    Parameters:
        tx (Transaction): The transaction to insert.
        schema_name (str): The name of the database schema to use.
    """
    try:
        with db_cursor(schema_name) as (conn, cursor):
            cursor.execute(
                f"""
                INSERT OR REPLACE INTO {TABLE_TRANSACTIONS} (
                    tx_id, block_height, v_size, fee_per_vsize,
                    effective_fee_per_vsize, version, lock_time, size, weight, fee
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    tx.tx_id,
                    tx.status.block_height,
                    tx.v_size,
                    tx.fee_per_vsize,
                    tx.effective_fee_per_vsize,
                    tx.version,
                    tx.lock_time,
                    tx.size,
                    tx.weight,
                    tx.fee,
                ),
            )
            logger.debug(f"Transaction {tx.tx_id} inserted into table '{TABLE_TRANSACTIONS}'.")

            tx_outputs = [
                (
                    tx.tx_id,
                    index,
                    v_output.script_pubkey,
                    v_output.script_pubkey_asm,
                    v_output.script_pubkey_type,
                    v_output.script_pubkey_address,
                    v_output.value,
                )
                for index, v_output in enumerate(tx.v_out)
            ]

            batch_insert(
                cursor,
                TABLE_TX_OUTPUTS,
                [
                    "tx_id",
                    "v_out_index",
                    "script_pubkey",
                    "script_pubkey_asm",
                    "script_pubkey_type",
                    "script_pubkey_address",
                    "value",
                ],
                tx_outputs,
            )
            logger.debug(
                f"Outputs for transaction {tx.tx_id} inserted into table '{TABLE_TX_OUTPUTS}'."
            )

            tx_inputs = [
                (
                    tx.tx_id,
                    index,
                    v_input.prev_tx_id,
                    v_input.v_out,
                    v_input.script_sig,
                    v_input.script_sig_asm,
                    v_input.is_coinbase,
                    v_input.sequence,
                    v_input.inner_redeem_script_asm,
                    v_input.inner_witness_script_asm,
                )
                for index, v_input in enumerate(tx.v_in)
            ]

            batch_insert(
                cursor,
                TABLE_TX_INPUTS,
                [
                    "tx_id",
                    "v_in_index",
                    "prev_tx_id",
                    "v_out_index",
                    "script_sig",
                    "script_sig_asm",
                    "is_coinbase",
                    "sequence",
                    "inner_redeem_script_asm",
                    "inner_witness_script_asm",
                ],
                tx_inputs,
            )
            logger.debug(
                f"Inputs for transaction {tx.tx_id} inserted into table '{TABLE_TX_INPUTS}'."
            )

            batch_insert(
                cursor,
                TABLE_WITNESSES,
                ["tx_id", "witness"],
                [(tx.tx_id, witness) for v_input in tx.v_in for witness in v_input.witness],
            )
            logger.debug(
                f"Witness for transaction {tx.tx_id} inserted into table '{TABLE_WITNESSES}'."
            )

            logger.info(f"Transaction {tx.tx_id} inserted into database.")

    except Exception as e:
        logger.error(f"Error while inserting transaction {tx.tx_id}, rolling back: {e}")
        raise
