"""encrypt conftest.py"""

import pytest
from ucn.encrypt.encrypt import KEY_ENCRYPT_MAP
from ucn.encrypt.key import KeyStore, MultiKey, Key

PASSPHRASE = "test_passphrase"


@pytest.fixture(scope="module", params=list(KEY_ENCRYPT_MAP.values()))
def key_encrypt_obj(request):
    """Fixture to create a KeyEncrypt object for testing."""
    return request.param


@pytest.fixture(scope="function")
def key_store(key_encrypt_obj):
    """Fixture to create a KeyStore object for testing."""
    private_key = key_encrypt_obj.generate_private_key(PASSPHRASE)
    public_key = key_encrypt_obj.generate_public_key(private_key, PASSPHRASE)
    return KeyStore(
        encrypt_algo=key_encrypt_obj.get_name(),
        public_key=public_key,
        private_key=private_key,
        passphrase=PASSPHRASE,
    )


@pytest.fixture(scope="function")
def key_store2(key_encrypt_obj):
    """Fixture to create a second KeyStore object for testing."""
    private_key = key_encrypt_obj.generate_private_key(PASSPHRASE)
    public_key = key_encrypt_obj.generate_public_key(private_key, PASSPHRASE)
    return KeyStore(
        encrypt_algo=key_encrypt_obj.get_name(),
        public_key=public_key,
        private_key=private_key,
        passphrase=PASSPHRASE,
    )


@pytest.fixture
def multikey(key_store, key_store2):
    """
    Fixture for creating a MultiKey object with two keys
    from the given key stores.
    """
    key1 = Key(key_store)
    key2 = Key(key_store2)
    return MultiKey([key1, key2])


@pytest.fixture(params=["Base85", "SHAKE256", None])
def encode_algo(request):
    """Fixture for parameterized encoding algorithm."""
    return request.param
