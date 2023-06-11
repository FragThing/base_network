import pytest
from sqlalchemy import create_engine
from ucn.block.store.local_store import LocalBlockStore
from ucn.block.error import InvalidPreviousBlockHashError, MissingGenesisBlockError


@pytest.fixture
def local_block_store():
    """Provide a fresh LocalBlockStore instance with an in-memory database for each test."""
    engine = create_engine("sqlite:///:memory:")
    return LocalBlockStore(engine)


def test_add_and_retrieve_genesis_block(local_block_store):
    """
    Test adding a genesis block and retrieving it by hash.
    The genesis block is the first block in the blockchain.
    """
    # Prepare test data
    protocol = "test_protocol"
    data = b"test_data"

    # Add a genesis block and retrieve it by hash
    added_block_hash = local_block_store.add_block(protocol, data, "")
    retrieved_block = local_block_store.get_block(added_block_hash)

    # Check if the retrieved block has the correct attributes
    assert retrieved_block.protocol == protocol
    assert retrieved_block.data == data
    assert retrieved_block.previous_block_hash == ""


def test_add_and_retrieve_non_genesis_block(local_block_store):
    """
    Test adding a non-genesis block and retrieving it by hash.
    A non-genesis block is any block added after the genesis block.
    """
    # Prepare test data
    protocol = "test_protocol"
    data = b"test_data"

    # Add a genesis block
    genesis_block_hash = local_block_store.add_block(protocol, data, "")

    # Add a non-genesis block and retrieve it by hash
    added_block_hash = local_block_store.add_block(protocol, data, genesis_block_hash)
    retrieved_block = local_block_store.get_block(added_block_hash)

    # Check if the retrieved block has the correct attributes
    assert retrieved_block.protocol == protocol
    assert retrieved_block.data == data
    assert retrieved_block.previous_block_hash == genesis_block_hash


def test_retrieve_non_existent_block(local_block_store):
    """
    Test retrieving a block that does not exist in the store.
    """
    non_existent_hash = "non_existent_hash"
    assert local_block_store.get_block(non_existent_hash) is None


def test_add_and_retrieve_block_by_index(local_block_store):
    """
    Test adding several blocks and retrieving them by index.
    """
    # Prepare test data
    protocol = "test_protocol"
    data = b"test_data"

    # Add several blocks
    previous_hash = ""
    for i in range(3):
        block_hash = local_block_store.add_block(protocol, data, previous_hash)
        previous_hash = block_hash

    # Retrieve the blocks by index and check if they have the correct attributes
    for i in range(3):
        block = local_block_store.get_block_by_index(i)
        assert block.protocol == protocol
        assert block.data == data

    # Test retrieving a block by an invalid index
    assert local_block_store.get_block_by_index(100) is None


def test_add_block_with_invalid_previous_hash(local_block_store):
    """
    Test adding a block with an invalid previous hash.
    An InvalidPreviousBlockHashError should be raised.
    """
    protocol = "test_protocol"
    data = b"test_data"
    previous_hash = "invalid_previous_block_hash"

    local_block_store.add_block(protocol, data, "")

    with pytest.raises(InvalidPreviousBlockHashError):
        local_block_store.add_block(protocol, data, previous_hash)


def test_add_multiple_genesis_blocks(local_block_store):
    """
    Test adding multiple genesis blocks.
    An InvalidPreviousBlockHashError should be raised when trying to add a second genesis block.
    """
    protocol = "test_protocol"
    data = b"test_data"
    local_block_store.add_block(protocol, data, "")

    with pytest.raises(InvalidPreviousBlockHashError):
        local_block_store.add_block("another_protocol", data, "")


def test_add_block_with_duplicate_hash(local_block_store):
    """
    Test adding a block with a hash that is already in the store.
    An InvalidPreviousBlockHashError should be raised.
    """
    protocol = "test_protocol"
    data = b"test_data"

    # Add a genesis block
    genesis_block_hash = local_block_store.add_block(protocol, data, "")

    # Add another block
    local_block_store.add_block(protocol, data, genesis_block_hash)

    # Attempt to add a block with a duplicate hash
    with pytest.raises(InvalidPreviousBlockHashError):
        local_block_store.add_block(protocol, data, genesis_block_hash)


def test_add_block_without_genesis_block(local_block_store):
    """
    Test adding a block when the genesis block is missing.
    A MissingGenesisBlockError should be raised.
    """
    protocol = "test_protocol"
    data = b"test_data"
    previous_hash = "previous_block_hash"

    with pytest.raises(MissingGenesisBlockError):
        local_block_store.add_block(protocol, data, previous_hash)


def test_block_hash(local_block_store):
    """
    Test whether the hash of a block, as returned by add_block, is correct.
    """
    # Prepare test data
    protocol = "test_protocol"
    data = b"test_data"

    # Add a genesis block and check the hash
    added_block_hash = local_block_store.add_block(protocol, data, "")
    genesis_block = local_block_store.get_block(added_block_hash)
    assert local_block_store.get_hash(genesis_block) == added_block_hash

    # Check fixed hash value
    assert (
        added_block_hash
        == "sha256:d0c7f548d3117670fbe890fe72e891851affcdea0b8f0b95444e7b2596296847"
    )
    # Add a few more blocks and check their hashes
    previous_hash = added_block_hash
    for _ in range(3):
        added_block_hash = local_block_store.add_block(protocol, data, previous_hash)
        block = local_block_store.get_block(added_block_hash)
        assert local_block_store.get_hash(block) == added_block_hash
        previous_hash = added_block_hash


def test_remove_block(local_block_store):
    """
    Test removing a block by its hash.
    """
    # Prepare test data
    protocol = "test_protocol"
    data = b"test_data"

    # Add several blocks
    previous_hash = ""
    added_block_hashes = []
    for i in range(3):
        block_hash = local_block_store.add_block(protocol, data, previous_hash)
        added_block_hashes.append(block_hash)
        previous_hash = block_hash

    # Remove the block at index 1 by its hash and all blocks that follow it
    removed_blocks = local_block_store.remove_block(added_block_hashes[1])

    # Check if the removed blocks have the same hash as the added blocks
    assert [
        local_block_store.get_hash(block) for block in removed_blocks
    ] == added_block_hashes[1:]

    # The blocks should no longer exist in the store
    for block_hash in added_block_hashes[1:]:
        assert local_block_store.get_block(block_hash) is None


def test_remove_block_by_index(local_block_store):
    """
    Test removing a block by its index.
    """
    # Prepare test data
    protocol = "test_protocol"
    data = b"test_data"

    # Add several blocks
    previous_hash = ""
    added_block_hashes = []
    for i in range(3):
        block_hash = local_block_store.add_block(protocol, data, previous_hash)
        added_block_hashes.append(block_hash)
        previous_hash = block_hash

    # Remove the block at index 1 and all blocks that follow it
    removed_blocks = local_block_store.remove_block_by_index(1)

    # Check if the removed blocks have the same hash as the added blocks
    assert [
        local_block_store.get_hash(block) for block in removed_blocks
    ] == added_block_hashes[1:]

    # The blocks should no longer exist in the store
    for i in range(1, 3):
        assert local_block_store.get_block_by_index(i) is None


def test_add_block_after_removal(local_block_store):
    """
    Test adding a block after a block has been removed.
    The block index should be continuous.
    """
    # Prepare test data
    protocol = "test_protocol"
    data = b"test_data"

    # Add several blocks
    previous_hash = ""
    added_block_hashes = []
    for i in range(3):
        block_hash = local_block_store.add_block(protocol, data, previous_hash)
        added_block_hashes.append(block_hash)
        previous_hash = block_hash

    # Remove the block at index 1 by its hash and all blocks that follow it
    local_block_store.remove_block(added_block_hashes[1])

    # Add a new block
    new_block_hash = local_block_store.add_block(protocol, data, added_block_hashes[0])

    # Retrieve the new block by its hash
    new_block = local_block_store.get_block(new_block_hash)
    new_block_with_index = local_block_store.get_block_by_index(1)

    # The new block should have index 1
    assert new_block == new_block_with_index


def test_get_latest_block_by_index(local_block_store):
    """
    Test that the get_block_by_index function returns the latest block when the index is -1.
    """
    # Prepare test data
    protocol = "test_protocol"
    data = b"test_data"

    # Add a block
    first_block_hash = local_block_store.add_block(protocol, data, "")

    # Add another block with explicit previous block hash
    latest_block_hash = local_block_store.add_block(protocol, data, first_block_hash)

    # Retrieve the latest block by specifying the index as -1
    latest_block = local_block_store.get_block_by_index(-1)

    # The hash of the latest block should match the hash of the block that was added last
    assert local_block_store.get_hash(latest_block) == latest_block_hash


def test_add_block_automatic_latest_hash(local_block_store):
    """
    Test that the add_block function automatically retrieves the hash of the latest block
    if no previous_block_hash is specified.
    """
    # Prepare test data
    protocol = "test_protocol"
    data = b"test_data"

    # Add the genesis block
    genesis_block_hash = local_block_store.add_block(protocol, data)

    # Add a new block without specifying the previous_block_hash
    new_block_hash = local_block_store.add_block(protocol, data)

    # Retrieve the new block by its hash
    new_block = local_block_store.get_block(new_block_hash)

    # The previous_block_hash of the new block should be the hash of the genesis block
    assert new_block.previous_block_hash == genesis_block_hash
