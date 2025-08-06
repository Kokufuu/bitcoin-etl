from typing import Optional

from pydantic import Field

from model.dto import DTOModel


class Pool(DTOModel):
    """Mining pool related information.

    Attributes:
        id: int Unique internal identifier of the mining pool.
        name: str Human-readable name of the pool (e.g., "AntPool", "Foundry USA").
        slug: str URL-friendly version of the name (used in links or APIs, e.g., foundry-usa).
        miner_names: list[str]
            List of known miner aliases or names used by this pool in the coinbase signature or tag.
    """

    id: int
    name: str
    slug: str
    miner_names: Optional[list[str]] = Field(alias="minerNames")


class Extras(DTOModel):
    """Additional information about a block.

    Attributes:
        header: str Full raw block header in hex.
        reward: int Total reward: block subsidy plus total transaction fees.
        median_fee: float Median fee of all transactions in the block.
        fee_range: list[float] List of fees or fee rate ranges (e.g., for histogram, quantiles).
        total_fees: int Sum of all transaction fees in the block.
        avg_fee: int Average transaction fee.
        avg_fee_rate: int Average fee per virtual byte (sat/vB).
        coinbase_raw: str Raw hex of the coinbase transaction input script (custom data by miner).
        coinbase_address: str The address receiving the block reward.
        coinbase_addresses: list[str] All addresses in the coinbase transaction outputs.
        coinbase_signature: str Signature (often arbitrary data) miners include in coinbase input.
        utxo_set_change: int Net change in the UTXO set (new outputs - spent inputs).
        avg_tx_size: float Average size of transactions in bytes.
        total_inputs: int Total number of inputs across all transactions.
        total_outputs: int Total number of outputs across all transactions.
        total_output_amt: int Sum of output amounts (in satoshis).
        segwit_total_txs: int Number of SegWit-enabled transactions in the block.
        segwit_total_size: int Total byte size of SegWit transactions.
        segwit_total_weight: int Total weight of SegWit transactions.
        virtual_size: float Equivalent block size used for fee calculation (≈ weight / 4).
        pool: Pool Mining pool related information.
        similarity: float Percentage similarity between actual block and predicted block template.
    """

    header: str
    reward: int
    median_fee: float = Field(alias="medianFee")
    fee_range: list[float] = Field(alias="feeRange")
    total_fees: int = Field(alias="totalFees")
    avg_fee: int = Field(alias="avgFee")
    avg_fee_rate: int = Field(alias="avgFeeRate")
    coinbase_raw: str = Field(alias="coinbaseRaw")
    coinbase_address: str = Field(alias="coinbaseAddress")
    coinbase_addresses: list[str] = Field(alias="coinbaseAddresses")
    coinbase_signature: str = Field(alias="coinbaseSignature")
    utxo_set_change: int = Field(alias="utxoSetChange")
    avg_tx_size: float = Field(alias="avgTxSize")
    total_inputs: int = Field(alias="totalInputs")
    total_outputs: int = Field(alias="totalOutputs")
    total_output_amt: int = Field(alias="totalOutputAmt")
    segwit_total_txs: int = Field(alias="segwitTotalTxs")
    segwit_total_size: int = Field(alias="segwitTotalSize")
    segwit_total_weight: int = Field(alias="segwitTotalWeight")
    virtual_size: float = Field(alias="virtualSize")
    pool: Pool
    similarity: Optional[float] = None


class Block(DTOModel):
    """Detailed information about a block.

    Attributes:
        id: str Unique identifier (block hash).
        height: int Block height (its position in the blockchain).
        version: int Version of the block (set by the miner, can signal upgrade intentions).
        timestamp: int Time the block was mined (UNIX epoch).
        bits: int Compact encoding of the difficulty target (used in mining).
        nonce: int Number used by miners to find a valid hash under the difficulty target.
        difficulty: float Difficulty level when the block was mined.
        merkle_root: str Root hash of the Merkle tree built from transactions in the block.
        tx_count: int Number of transactions included in the block.
        size: int Block size in bytes (raw block size).
        weight: int Block weight (segwit-adjusted size, max 4,000,000).
        previous_block_hash: str Hash of the preceding block (parent).
        median_time: int Median of the last 11 block timestamps (used for consensus).
        extras: Extras Additional information about a block.
    """

    id: str
    height: int
    version: int
    timestamp: int
    bits: int
    nonce: int
    difficulty: float
    merkle_root: str
    tx_count: int
    size: int
    weight: int
    previous_block_hash: str = Field(alias="previousblockhash")
    median_time: int = Field(alias="mediantime")
    extras: Extras
