class BlockChainError(Exception):
    """Base class for all blockchain related errors."""


class InvalidPreviousBlockHashError(BlockChainError):
    """Raised when the previous block hash does not match the latest block hash in the database."""


class MissingGenesisBlockError(BlockChainError):
    """Raised when an operation requires the existence of a genesis block but it does not exist."""
