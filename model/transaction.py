from pydantic import Field

from model.block import DTOModel


class Status(DTOModel):
    """Transaction status.

    Attributes:
        confirmed (bool): True if the transaction is confirmed in the blockchain.
        block_height (int): The height of the block containing the transaction.
        block_hash (str): The hash of the block containing the transaction.
        block_time (int): The timestamp of the block containing the transaction.
    """

    confirmed: bool
    block_height: int
    block_hash: str
    block_time: int


class TxOutput(DTOModel):
    """Previous output details.

    Attributes:
        script_pubkey (str): The hex-encoded locking script that controls who can spend this output.
        script_pubkey_asm (str): The human-readable representation of script_pubkey using Bitcoin opcodes.
        script_pubkey_type (str): Type of script used — most common values: p2pkh, p2sh, p2wpkh, p2tr.
        script_pubkey_address (str): The address derived from the script, if recognizable.
        value (int): The amount of satoshis in the UTXO or output.
    """

    script_pubkey: str = Field(alias="scriptpubkey")
    script_pubkey_asm: str = Field(alias="scriptpubkey_asm")
    script_pubkey_type: str = Field(alias="scriptpubkey_type")
    script_pubkey_address: str = Field(alias="scriptpubkey_address")
    value: int


class TxInput(DTOModel):
    """Transaction input.

    Attributes:
        prev_tx_id (str): ID of the previous transaction where the output being spent is located.
        v_out (int): Index of the output (from the previous tx) being spent.
        prev_out (PrevOut): The actual referenced output details; null in coinbase txs.
        script_sig (str): Script (in hex) that unlocks the previous output.
        script_sig_asm (str): Human-readable assembly of the unlocking script.
        witness (list[str]):
            Witness data for SegWit transactions.
            Each item in the list is a hex-encoded data element (e.g., signatures, public keys).
        is_coinbase (bool): True if this is a coinbase input (mining reward); such txs don’t have a real tx_id.
        sequence (int): Optional sequence number (used with nLockTime for advanced transaction logic).
        inner_redeem_script_asm (str):
            The assembly form of the script that gets evaluated in P2SH or nested SegWit transactions.
        inner_witness_script_asm (str):
            The assembly form of the script that gets evaluated in P2WSH or nested SegWit transactions.
    """

    prev_tx_id: str = Field(alias="txid")
    v_out: int = Field(alias="vout")
    prev_out: TxOutput | None = Field(alias="prevout")
    script_sig: str = Field(alias="scriptsig")
    script_sig_asm: str = Field(alias="scriptsig_asm")
    witness: list[str]
    is_coinbase: bool
    sequence: int
    inner_redeem_script_asm: str = Field(alias="inner_redeemscript_asm")
    inner_witness_script_asm: str = Field(alias="inner_witnessscript_asm")


class Transaction(DTOModel):
    """Detailed information about a transaction.

    Attributes:
        tx_id (str): Transaction ID (hash of the transaction data); uniquely identifies the transaction.
        v_size (int): The virtual size of the transaction in bytes.
        fee_per_vsize (int): The actual fee rate paid by the transaction, in satoshis per virtual byte (sat/vB).
        effective_fee_per_vsize (int):
            The minimum effective fee rate that would be required to keep the transaction in the mempool,
            considering ancestor/descendant relationships and dynamic mempool rules.
        version (int): Transaction format version number; used to interpret the structure.
        lock_time (int):
            The earliest time or block height when the transaction can be added
            to the blockchain (used for time-based delays).
        v_in (list): List of inputs: references to previous outputs being spent.
        v_out (list): List of outputs: specifies where and how much bitcoin is being sent.
        size (int): Raw transaction size in bytes.
        weight (int): SegWit-adjusted size (max weight for a block is 4,000,000).
        fee (int): Total fee paid (difference between input and output values, in satoshis).
        status (Status): Transaction status.
    """

    tx_id: str = Field(alias="txid")
    v_size: float = Field(alias="vsize")
    fee_per_vsize: float = Field(alias="feePerVsize")
    effective_fee_per_vsize: float = Field(alias="effectiveFeePerVsize")
    version: int
    lock_time: int = Field(alias="locktime")
    v_in: list[TxInput] = Field(alias="vin")
    v_out: list[TxOutput] = Field(alias="vout")
    size: int
    weight: int
    fee: int
    status: Status
