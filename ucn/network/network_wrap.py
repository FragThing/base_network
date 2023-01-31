"""UCN network callback to blocking wrapper"""
from ucn.network.network import send_callback, regist_callback
from ucn.network.net_type import BaseType
from ucn.thread_utils import get_wait_result, get_queue


def send(network_type: BaseType, data: bytes) -> bytes:
    """Send data and return data"""
    result = get_wait_result()
    send_callback(network_type, data, lambda data: result.set(result))
    return result.get()


def recv(network_type: BaseType) -> bytes:
    """Receive data and yield return data"""
    queue = get_queue()
    regist_callback(network_type, lambda data: queue.put(data))
    for data in queue:
        yield data
