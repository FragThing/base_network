"""Utils"""
from json import dumps
from time import time
from base64 import b85encode, b85decode


def json_dumps(obj) -> str:
    """Dumps Json without whitespaces"""
    return dumps(obj, separators=(",", ":"))


def get_timestamp():
    """Get timestamp"""
    return time()


def data_bytes_to_string(data: bytes) -> str:
    """Encode bytes to string by base85"""
    return b85encode(data).decode("utf8")


def data_string_to_bytes(string: str) -> bytes:
    """Decode string to bytes by base85"""
    return b85decode(string.encode("utf8"))


def data_bytes_list_to_string(data_list: list[bytes]) -> str:
    """Encode bytes list to string by base85"""
    return "\n".join([b85encode(data).decode("utf8") for data in data_list])


def data_string_to_bytes_list(string: str) -> list[bytes]:
    """Decode string to bytes list by base85"""
    return [b85decode(s.encode("utf8")) for s in string.split("\n")]
