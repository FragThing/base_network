"""
Tests for the ucn.encrypt.encrypt module.

This test suite contains test cases for the following classes and functions:
- Ed25519KeyEncrypt class
- save_key_to_file function
- KeyEncrypt class and its subclasses
- KEY_ENCRYPT_MAP

The test cases cover the following functionalities:
- Ensuring the correct encryption algorithm is in KEY_ENCRYPT_MAP
- Saving a key to a file
- Generating private and public keys
- Getting the hash content from a public key
- Signing and verifying data using private and public keys

Usage:
    Run the tests with the command: pytest tests/test_encrypt.py
"""

from collections import Counter
import os
from ucn.encrypt.encrypt import (
    save_key_to_file,
    KeyEncrypt,
    KEY_ENCRYPT_MAP,
)

PASSPHRASE = "test_passphrase"
DATA_TO_SIGN = b"Hello, this is a test message."


def test_key_encrypt_map_contains_correct_algorithms():
    """Test if KEY_ENCRYPT_MAP contains the correct encryption algorithm."""
    assert Counter(["Ed25519"]) == Counter(KEY_ENCRYPT_MAP.keys())
    for name, encryption in KEY_ENCRYPT_MAP.items():
        assert isinstance(encryption, KeyEncrypt)
        assert name == encryption.get_name()


def test_save_key_to_file(tmpdir):
    """Test save_key_to_file function."""
    test_file = tmpdir.join("test_key_file.pem")
    save_key_to_file(test_file, "test_key")
    assert os.path.exists(test_file)
    assert test_file.read() == "test_key"


def test_generate_private_key(key_encrypt_obj):
    """Test generate_private_key function."""
    private_key = key_encrypt_obj.generate_private_key(PASSPHRASE)
    assert isinstance(private_key, bytes)
    assert len(private_key)


def test_generate_public_key(key_encrypt_obj):
    """Test generate_public_key function."""
    private_key = key_encrypt_obj.generate_private_key(PASSPHRASE)
    public_key = key_encrypt_obj.generate_public_key(private_key, PASSPHRASE)
    assert isinstance(public_key, bytes)
    assert len(public_key)


def test_get_hash_content(key_encrypt_obj):
    """Test get_hash_content function."""
    private_key = key_encrypt_obj.generate_private_key(PASSPHRASE)
    public_key = key_encrypt_obj.generate_public_key(private_key, PASSPHRASE)
    hash_content = key_encrypt_obj.get_hash_content(public_key)
    assert hash_content == public_key


def test_sign_and_verify(key_encrypt_obj):
    """Test sign and verify functions."""
    private_key = key_encrypt_obj.generate_private_key(PASSPHRASE)
    public_key = key_encrypt_obj.generate_public_key(private_key, PASSPHRASE)
    signature = key_encrypt_obj.sign(private_key, PASSPHRASE, DATA_TO_SIGN)

    assert key_encrypt_obj.verify(public_key, signature, DATA_TO_SIGN)
    assert not key_encrypt_obj.verify(public_key, signature, b"Tampered message")
