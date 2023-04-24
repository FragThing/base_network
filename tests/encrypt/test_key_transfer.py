"""
This module contains test cases for testing key transfer related functions
in the ucn.encrypt package.
"""

import pytest
from ucn.utils import data_bytes_list_to_string, data_string_to_bytes_list
from ucn.encrypt.key import MultiKey, Key
from ucn.encrypt.key_transfer import (
    generate_transfer_key_header,
    verify_transfer_key_header_and_get_data,
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


@pytest.fixture
def data():
    """Fixture for sample data used in testing."""
    return b"Sample data for testing"


@pytest.fixture(params=["Base85", "SHAKE256"])
def encode_algo(request):
    """Fixture for parameterized encoding algorithm."""
    return request.param


def test_generate_transfer_key_header(multikey, encode_algo, data):
    """
    Test generating a transfer key header with a valid MultiKey object
    and data. Assert that the header is a non-empty bytes object.
    """
    header = generate_transfer_key_header(multikey, encode_algo, data)
    assert isinstance(header, bytes) and len(header) > 0


def test_verify_transfer_key_header_and_get_data(multikey, encode_algo, data):
    """
    Test verifying a transfer key header and retrieving the data.
    Assert that the retrieved data matches the original data after successful
    verification.
    """
    header = generate_transfer_key_header(multikey, encode_algo, data)
    combined_data = header + data
    retrieved_data = verify_transfer_key_header_and_get_data(combined_data)
    assert retrieved_data == data


def test_verify_transfer_key_header_with_invalid_key(multikey, encode_algo, data):
    """
    Test verifying a transfer key header with an invalid key.
    Assert that None is returned due to the failed verification.
    """
    header = generate_transfer_key_header(multikey, encode_algo, data)
    header_data = data_string_to_bytes_list(
        header.split(b"\n", maxsplit=1)[1].decode("utf8")
    )
    combined_url = b"Invalid://" + header_data.pop(0).split(b"://", maxsplit=1)[1]
    combined_header = data_bytes_list_to_string([combined_url] + header_data).encode(
        "utf8"
    )
    combined_data = (
        str(len(combined_header)).encode("utf8") + b"\n" + combined_header + data
    )
    with pytest.raises(Exception):
        verify_transfer_key_header_and_get_data(combined_data)


def test_verify_transfer_key_header_with_invalid_signature(multikey, encode_algo, data):
    """
    Test verifying a transfer key header with an invalid signature.
    Assert that None is returned due to the failed verification.
    """
    header = generate_transfer_key_header(multikey, encode_algo, data)
    header_data = data_string_to_bytes_list(
        header.split(b"\n", maxsplit=1)[1].decode("utf8")
    )
    header_data[-1] = b"INVALID_SIGNATURE"
    combined_header = data_bytes_list_to_string(header_data).encode("utf8")
    combined_data = (
        str(len(combined_header)).encode("utf8") + b"\n" + combined_header + data
    )
    retrieved_data = verify_transfer_key_header_and_get_data(combined_data)
    assert retrieved_data is None
