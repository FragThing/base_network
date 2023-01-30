""" UCN base network send and receive
with function callback
"""
from hashlib import shake_256
from ucn.network import net_type
from ucn.network import ipfs
from ucn.config import IPFS_API_URL


callback_map = {}


def send(network_type: net_type.BaseType, data: bytes, callback):
    """Send data and callback"""
    data_header = shake_256(data).hexdigest(64)
    callback_key = f"{network_type} {data_header}"
    callback_map[callback_key] = callback
    re_data = data_header.encode("utf-8") + "\n" + data
    ipfs.send(re_data, str(network_type.value), IPFS_API_URL)


def __handle_recv(network_type: net_type.BaseType):
    """Receive data and try match callback"""
    for data in ipfs.recv(str(network_type.value), IPFS_API_URL):
        try:
            data_header, data = data.split("\n", maxsplit=1)
            callback_key = f"{network_type} {data_header}"
            callback_map.pop(callback_key)(data)
        except KeyError:
            pass
        except ValueError:
            print("wrong data format")


def get_recv_handler_list():
    """Generate handle_recv by network type list"""
    return [
        lambda ntype=network_type: __handle_recv(ntype)
        for network_type in net_type.TYPE_LIST
    ]
