"""Generate and Verify transfer key header
"""

from fractions import Fraction
from ucn.utils import data_bytes_list_to_string, data_string_to_bytes_list
from ucn.encrypt.key import MultiKey, Key, KeyStore
from ucn.encrypt.key_url import key_url, url_parse


def generate_transfer_key_header(
    multikey: MultiKey, encode_algo: str, data: bytes
) -> bytes:
    """Generate transfer key header"""
    header_list = []
    key_url_str = key_url.generate(multikey.key_list, encode_algo)
    header_list.append(key_url_str.encode("utf8"))
    key_decodable = url_parse.decodable_algo(encode_algo)
    for key, signature in multikey.sign(data):
        keystore = key.keystore
        if not key_decodable:
            header_list.append(keystore.encrypt_algo.encode("utf8"))
            header_list.append(keystore.public_key)
        header_list.append(signature)
    header_data = data_bytes_list_to_string(header_list).encode("utf8")
    header_size = str(len(header_data)).encode("utf8")
    return header_size + b"\n" + header_data


def verify_transfer_key_header_and_get_data(data: bytes) -> bytes or None:
    """Verify transfer key header by signature
    And practice data
    Or drop if reliability < 1"""
    header_size_bytes, data = data.split(b"\n", maxsplit=1)
    header_size = int(header_size_bytes.decode("utf8"))
    header, data = (data[:header_size], data[header_size:])
    header_list = data_string_to_bytes_list(header.decode("utf8"))
    key_url_bytes = header_list.pop(0)
    key_url_str = key_url_bytes.decode("utf-8")
    key_list = key_url.parse(key_url_str)
    key_signature_list = []
    i = 0
    if key_list is None:
        key_list_complete = []
    else:
        key_list_complete = key_list
    while header_list:
        if key_list is None:
            encrypt_algo = header_list.pop(0).decode("utf8")
            public_key = header_list.pop(0)
            key = Key(KeyStore(encrypt_algo=encrypt_algo, public_key=public_key))
            key_list_complete.append(key)
        else:
            key = key_list[i]
            i += 1
        signature = header_list.pop(0)
        key_signature_list.append((key.keystore.public_key, signature))
    if key_list is None:
        multikey = MultiKey(key_list_complete)
    else:
        multikey = MultiKey(key_list)
    encode_algo = key_url_str.split("://", maxsplit=1)[0]
    if key_url.generate(multikey.key_list, encode_algo) != key_url_str:
        return None
    reliability = multikey.verify(data, key_signature_list)
    if int(Fraction(reliability)):
        return data
    return None
