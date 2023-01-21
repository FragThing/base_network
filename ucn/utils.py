"""Utils"""
from json import dumps


def json_dumps(obj) -> str:
    """Dumps Json without whitespaces"""
    return dumps(obj, separators=(',', ':'))
