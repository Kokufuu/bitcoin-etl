import sqlite3

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

logger = setup_logger(__name__)


def create_block_tables(cursor: sqlite3.Cursor):
    """Creating all tables necessary for blocks."""
    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {TABLE_BLOCKS} (
            height INTEGER PRIMARY KEY,
            id TEXT NOT NULL,
            version INTEGER NOT NULL,
            timestamp INTEGER NOT NULL,
            bits INTEGER NOT NULL,
            nonce INTEGER NOT NULL,
            difficulty REAL NOT NULL,
            merkle_root TEXT NOT NULL,
            tx_count INTEGER NOT NULL,
            size INTEGER NOT NULL,
            weight INTEGER NOT NULL,
            previous_block_hash TEXT NOT NULL,
            median_time INTEGER NOT NULL
        )
    """
    )

    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {TABLE_EXTRAS} (
            height INTEGER PRIMARY KEY,
            header TEXT NOT NULL,
            reward INTEGER NOT NULL,
            median_fee REAL NOT NULL,
            total_fees INTEGER NOT NULL,
            avg_fee INTEGER NOT NULL,
            avg_fee_rate INTEGER NOT NULL,
            coinbase_raw TEXT NOT NULL,
            coinbase_address TEXT NOT NULL,
            coinbase_signature TEXT NOT NULL,
            utxo_set_change INTEGER NOT NULL,
            avg_tx_size REAL NOT NULL,
            total_inputs INTEGER NOT NULL,
            total_outputs INTEGER NOT NULL,
            total_output_amt INTEGER NOT NULL,
            segwit_total_txs INTEGER NOT NULL,
            segwit_total_size INTEGER NOT NULL,
            segwit_total_weight INTEGER NOT NULL,
            virtual_size REAL NOT NULL,
            similarity REAL,
            FOREIGN KEY (height) REFERENCES blocks(height) ON DELETE CASCADE
        )
    """
    )

    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {TABLE_FEE_RANGE} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            height INTEGER NOT NULL,
            fee REAL NOT NULL,
            FOREIGN KEY (height) REFERENCES blocks(height) ON DELETE CASCADE
        )
    """
    )

    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {TABLE_COINBASE_ADDRESSES} (
            height INTEGER PRIMARY KEY,
            address TEXT NOT NULL,
            FOREIGN KEY (height) REFERENCES blocks(height) ON DELETE CASCADE
        )
    """
    )

    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {TABLE_POOLS} (
            height INTEGER PRIMARY KEY,
            id INTEGER NOT NULL,
            name TEXT,
            slug TEXT,
            FOREIGN KEY (height) REFERENCES blocks(height) ON DELETE CASCADE
        )
    """
    )

    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {TABLE_MINERS} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            height INTEGER NOT NULL,
            name TEXT,
            FOREIGN KEY (height) REFERENCES blocks(height) ON DELETE CASCADE
        )
    """
    )

    logger.info("Block related tables created.")


def create_transaction_tables(cursor: sqlite3.Cursor):
    """Creating all tables necessary for transactions."""
    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {TABLE_TRANSACTIONS} (
            tx_id TEXT PRIMARY KEY,
            block_height INTEGER NOT NULL,
            v_size INTEGER NOT NULL,
            fee_per_vsize INTEGER NOT NULL,
            effective_fee_per_vsize INTEGER NOT NULL,
            version INTEGER NOT NULL,
            lock_time INTEGER NOT NULL,
            size INTEGER NOT NULL,
            weight INTEGER NOT NULL,
            fee INTEGER NOT NULL,
            FOREIGN KEY (block_height) REFERENCES blocks(height) ON DELETE CASCADE
        )
    """
    )

    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {TABLE_TX_OUTPUTS} (
            tx_id TEXT,
            v_out_index INTEGER NOT NULL,
            script_pubkey TEXT NOT NULL,
            script_pubkey_asm TEXT NOT NULL,
            script_pubkey_type TEXT NOT NULL,
            script_pubkey_address TEXT NOT NULL,
            value INTEGER NOT NULL,
            PRIMARY KEY (tx_id, v_out_index),
            FOREIGN KEY (tx_id) REFERENCES transactions(tx_id) ON DELETE CASCADE
        )
    """
    )

    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {TABLE_TX_INPUTS} (
            tx_id TEXT,
            v_in_index INTEGER NOT NULL,
            prev_tx_id TEXT NOT NULL,
            v_out_index INTEGER NOT NULL,
            script_sig TEXT NOT NULL,
            script_sig_asm TEXT NOT NULL,
            is_coinbase BOOLEAN NOT NULL,
            sequence INTEGER NOT NULL,
            inner_redeem_script_asm TEXT NOT NULL,
            inner_witness_script_asm TEXT NOT NULL,
            PRIMARY KEY (tx_id, v_in_index),
            FOREIGN KEY (tx_id) REFERENCES transactions(tx_id) ON DELETE CASCADE
        )
    """
    )

    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {TABLE_WITNESSES} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tx_id TEXT NOT NULL,
            witness TEXT NOT NULL,
            FOREIGN KEY (tx_id) REFERENCES transactions(tx_id) ON DELETE CASCADE
        )
    """
    )

    logger.info("Transaction related tables created.")


def create_tables():
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    try:
        create_block_tables(cursor)
        create_transaction_tables(cursor)
        conn.commit()
    except Exception as e:
        logger.error(f"Error while creating tables, rolling back: {e}")
        conn.rollback()
    finally:
        conn.close()
