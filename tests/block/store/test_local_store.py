from sqlalchemy import create_engine
from ucn.block.store.local_store import LocalBlockStore

# Create an engine for testing
engine = create_engine("sqlite:///:memory:")

# Create a new instance of the LocalBlockStore class for testing
local_block_store = LocalBlockStore(engine)


def test_add_block():
    """
    Test the add_block function of the LocalBlockStore class.

    This test covers the following cases:
    - Adding a block with a normal protocol, data, and previous block hash.
    """
    # Prepare test data
    protocol = "test_protocol"
    data = b"test_data"
    previous_block_hash = "test_previous_block_hash"

    # Add a block
    block = local_block_store.add_block(protocol, data, previous_block_hash)

    # Check if the block is correctly added
    assert block.protocol == protocol
    assert block.data == data
    assert block.previous_block_hash == previous_block_hash


def test_get_block():
    """
    Test the get_block function of the LocalBlockStore class.

    This test covers the following cases:
    - Retrieving a block that exists in the store.
    - Attempting to retrieve a block that does not exist in the store.
    """
    # Prepare test data
    protocol = "test_protocol"
    data = b"test_data"
    previous_block_hash = "test_previous_block_hash"

    # Add a block
    block = local_block_store.add_block(protocol, data, previous_block_hash)

    # Compute block hash
    block_hash = LocalBlockStore.get_hash(block)

    # Retrieve the block
    retrieved_block = local_block_store.get_block(block_hash)

    # Check if the retrieved block is the same as the original block
    assert retrieved_block.protocol == block.protocol
    assert retrieved_block.data == block.data
    assert retrieved_block.previous_block_hash == block.previous_block_hash
