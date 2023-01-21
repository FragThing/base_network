"""Generate and Verify transfer key header
"""

from fractions import Fraction
from ucn.encrypt.key import MultiKey, Key, KeyStore
from ucn.encrypt.url_parse import url_parse


def generate_transfer_key_header(
    encode_algo: str, multikey: MultiKey, data: bytes
) -> bytes:
    """Generate transfer key header"""
    transfer_header = b""
    key_url = url_parse.generate(encode_algo, multikey.decoder)
    transfer_header += b"%b\n" % key_url
    key_decodable = url_parse.decodable(encode_algo)
    for public_key, signature in multikey.sign(data):
        if not key_decodable:
            transfer_header += b"%b\n" % public_key
        transfer_header += b"%b\n" % signature
    return transfer_header


def verify_transfer_key_header_and_get_data(data: bytes) -> bytes or None:
    """Verify transfer key header by signature
    And practice data
    Or drop if reliability < 1"""
    key_url_bytes, data = data.split(b"\n", maxsplit=1)
    key_url = key_url_bytes.decode("utf-8")
    encode_algo, key_list = url_parse.parse(key_url)
    key_decodable = url_parse.decodable(encode_algo)
    if key_decodable:
        multikey = MultiKey(key_list)
    key_signature_list = []
    for _ in key_list:
        if key_decodable:
            signature, data = data.split(b"\n", maxsplit=1)
        else:
            public_key, signature, data = data.split(b"\n", maxsplit=2)
        key_signature_list.append((public_key, signature))
    if not key_decodable:
        multikey = MultiKey(
            [
                Key(KeyStore(encrypt_algo, public_key))
                for encrypt_algo, public_key, _ in zip(key_list, key_signature_list)
            ]
        )
        if url_parse.generate(encode_algo, multikey.key_list).decode("utf-8") != key_url:
            return None
    reliability = multikey.verify(data, key_signature_list)
    if int(Fraction(reliability)):
        # if reliability == 1
        return data
    return None
