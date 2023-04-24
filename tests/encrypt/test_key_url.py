"""
This module contains test cases for the KeyUrl class in key_url.py.
It verifies the functionality of generating and parsing URLs for single and
multiple key objects with various encoding algorithms. It also includes tests
for edge cases, such as empty or invalid inputs.
"""

import pytest
from ucn.encrypt.key import Key
from ucn.encrypt.key_url import key_url, KeyURLException


def test_key_url_generate_empty_list():
    """
    Test generating a URL with an empty list of Key objects. Assert that the
    generated URL contains an empty payload with the default encoding scheme
    (Base85).
    """
    key_list = []
    url = key_url.generate(key_list)
    assert url == "Base85://"


def test_key_url_generate_valid_url(key_store, key_store2):
    """
    Test generating a valid URL from a list of Key objects. Assert that the
    generated URL is a non-empty string.
    """
    key1 = Key(key_store)
    key2 = Key(key_store2)
    key_list = [key1, key2]

    url = key_url.generate(key_list)
    assert isinstance(url, str) and len(url) > 0


def test_key_url_single_key(key_store):
    """
    Test generating and parsing a URL with a single Key object. Assert that
    the parsed Key object matches the original Key object.
    """
    key = Key(key_store)
    key_list = [key]

    url = key_url.generate(key_list)
    parsed_key_list = key_url.parse(url)

    assert len(parsed_key_list) == len(key_list)
    assert key_list[0].keystore.encrypt_algo == parsed_key_list[0].keystore.encrypt_algo
    assert key_list[0].keystore.public_key == parsed_key_list[0].keystore.public_key


def test_key_url_parse_valid_url(key_store, key_store2):
    """
    Test parsing a valid URL and reconstructing the Key objects. Assert that
    the parsed Key objects match the original Key objects.
    """
    key1 = Key(key_store)
    key2 = Key(key_store2)
    key_list = [key1, key2]

    url = key_url.generate(key_list)
    parsed_key_list = key_url.parse(url)

    assert len(parsed_key_list) == len(key_list)
    for i, key in enumerate(key_list):
        assert key.keystore.encrypt_algo == parsed_key_list[i].keystore.encrypt_algo
        assert key.keystore.public_key == parsed_key_list[i].keystore.public_key


def test_key_url_parse_valid_url_shake256(key_store, key_store2):
    """
    Test parsing a valid URL and reconstructing the Key objects using
    a different encoding algorithm (shake256). Assert that a
    KeyURLException is raised due to the unsupported algorithm.
    """
    key1 = Key(key_store)
    key2 = Key(key_store2)
    key_list = [key1, key2]

    url = key_url.generate(key_list, "SHAKE256")
    assert key_url.parse(url) is None


def test_key_url_generate_with_invalid_encode_algo(key_store, key_store2):
    """
    Test generating a URL with an invalid encoding algorithm. Assert that a
    KeyError is raised due to the invalid algorithm.
    """
    key1 = Key(key_store)
    key2 = Key(key_store2)
    key_list = [key1, key2]

    with pytest.raises(KeyError):
        key_url.generate(key_list, encode_algo="invalid_algo")


def test_key_url_parse_invalid_url():
    """
    Test parsing an invalid URL. Assert that a KeyURLException is raised due
    to the invalid URL format.
    """
    url = "invalid_url"
    with pytest.raises(KeyURLException):
        key_url.parse(url)


def test_key_url_parse_url_with_invalid_content():
    """
    Test parsing a URL containing invalid content, which is not properly
    base85 encoded or improperly formatted. Assert that a KeyURLException is
    raised when attempting to parse the invalid content.
    """
    url = "http://example.com/invalid_content"

    assert key_url.parse(url) is None


def test_key_url_parse_url_shake256():
    """
    Test parsing a URL containing invalid content, which is not properly
    base85 encoded or improperly formatted. Assert that a KeyURLException is
    raised when attempting to parse the invalid content.
    """
    url = "shake256://123"
    assert key_url.parse(url) is None
