"""
This test suite covers the functionality of the KeyStore, Key, and MultiKey classes.
It includes tests for:
- KeyStore.load and KeyStore.dump functions
- Setting the passphrase for the KeyStore
- Signing and verifying data using Key and MultiKey classes
- MultiKey signing and verification using the same and different KeyStores
- Handling one or multiple mismatched signatures during verification
- Edge cases, such as an empty key list in MultiKey and invalid encryption algorithm in KeyStore
- Error handling, such as invalid private or public keys in Key.sign and Key.verify functions
"""

import pytest
from ucn.encrypt.key import KeyStore, Key, MultiKey

PASSPHRASE = "test_passphrase"
DATA_TO_SIGN = b"Hello, this is a test message."


# Original test cases
def test_key_store_load_dump(key_store):
    """Test KeyStore.load and KeyStore.dump functions."""
    key_data = key_store.dump()
    loaded_key_store = KeyStore.load(key_data)
    assert key_store.encrypt_algo == loaded_key_store.encrypt_algo
    assert key_store.public_key == loaded_key_store.public_key
    assert key_store.private_key == loaded_key_store.private_key


def test_key_store_set_passphrase(key_store):
    """Test KeyStore.set_passphrase function."""
    passphrase = "new_passphrase"
    key_store.set_passphrase(passphrase)
    assert key_store.passphrase == passphrase


def test_key_sign_verify(key_store):
    """Test Key.sign and Key.verify functions."""
    key = Key(key_store)
    signature = key.sign(DATA_TO_SIGN)
    assert key.verify(DATA_TO_SIGN, signature)
    assert not key.verify(b"Tampered message", signature)


def test_multi_key_sign_verify_same_key_store(key_store):
    """
    Test MultiKey.sign and MultiKey.verify functions
    using the same key store.
    """
    key1 = Key(key_store)
    key2 = Key(key_store)

    multi_key = MultiKey([key1, key2])
    key_signature_list = multi_key.sign(DATA_TO_SIGN)

    reliability_fraction = multi_key.verify(
        DATA_TO_SIGN,
        [(key.keystore.public_key, signature) for key, signature in key_signature_list],
    )
    assert reliability_fraction == "2/1"
    # Both keys should have successfully verified the data,
    # but there's only one actual key.


def test_multi_key_sign_verify_different_key_stores(key_store, key_store2):
    """
    Test MultiKey.sign and MultiKey.verify functions
    using different key stores.
    """
    key1 = Key(key_store)
    key2 = Key(key_store2)

    multi_key = MultiKey([key1, key2])
    key_signature_list = multi_key.sign(DATA_TO_SIGN)

    reliability_fraction = multi_key.verify(
        DATA_TO_SIGN,
        [(key.keystore.public_key, signature) for key, signature in key_signature_list],
    )
    assert (
        reliability_fraction == "2/2"
    )  # Both keys should have successfully verified the data


def test_multi_key_sign_verify_one_failure(key_store):
    """Test MultiKey.sign and MultiKey.verify functions with one mismatched signature."""
    key1 = Key(key_store)
    key2 = Key(key_store)

    multi_key = MultiKey([key1, key2])

    key_signature_list_correct = multi_key.sign(DATA_TO_SIGN)
    # Tamper with the first signature to make it mismatch the original data
    key_signature_list_tampered = [
        (key_signature_list_correct[0][0], b"Tampered signature"),
        key_signature_list_correct[1],
    ]
    reliability_fraction = multi_key.verify(
        DATA_TO_SIGN,
        [(key.keystore.public_key, signature) for key, signature in key_signature_list_tampered],
    )
    assert (
        reliability_fraction == "1/1"
    )  # Only one key should have successfully verified the data.


def test_multi_key_sign_verify_failure(key_store):
    """Test MultiKey.sign and MultiKey.verify functions with mismatched signatures."""
    key1 = Key(key_store)
    key2 = Key(key_store)
    multi_key = MultiKey([key1, key2])

    key_signature_list_correct = multi_key.sign(DATA_TO_SIGN)
    # Tamper with both signatures to make them mismatch the original data
    key_signature_list_tampered = [
        (key_signature_list_correct[0][0], b"Tampered signature 1"),
        (key_signature_list_correct[1][0], b"Tampered signature 2"),
    ]

    reliability_fraction = multi_key.verify(DATA_TO_SIGN, key_signature_list_tampered)
    assert (
        reliability_fraction == "0/1"
    )  # No keys should have successfully verified the tampered data.


# Additional edge case test cases
def test_empty_key_list():
    """Test MultiKey with an empty key list."""
    multi_key = MultiKey([])
    key_signature_list = multi_key.sign(DATA_TO_SIGN)
    assert key_signature_list == []
    reliability_fraction = multi_key.verify(DATA_TO_SIGN, key_signature_list)
    assert reliability_fraction == "0/0"


def test_key_store_with_invalid_encryption_algorithm(key_store):
    """Test KeyStore with an invalid encryption algorithm."""
    with pytest.raises(ValueError):
        KeyStore(
            encrypt_algo="invalid_algorithm",
            public_key=key_store.public_key,
            private_key=key_store.private_key,
            passphrase=PASSPHRASE,
        )


def test_key_sign_with_invalid_private_key(key_store):
    """Test Key.sign with an invalid private key."""
    key_store.private_key = b"Invalid private key"
    key = Key(key_store)
    with pytest.raises(Exception):
        key.sign(DATA_TO_SIGN)


def test_key_verify_with_invalid_public_key(key_store):
    """Test Key.verify with an invalid public key."""
    key_store.public_key = b"Invalid public key"
    key = Key(key_store)
    signature = b"Any signature"
    with pytest.raises(Exception):
        key.verify(DATA_TO_SIGN, signature)
