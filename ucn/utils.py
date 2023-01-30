"""Utils"""
from json import dumps
from time import time


def json_dumps(obj) -> str:
    """Dumps Json without whitespaces"""
    return dumps(obj, separators=(",", ":"))


def get_timestamp():
    """Get timestamp"""
    return time()
