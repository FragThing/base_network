"""Base Network templeate for all networks to be used in the project
"""

from abc import ABCMeta, abstractmethod
from multiprocessing import Queue
from typing import Iterator, Mapping


class BasicNetworkModel(metaclass=ABCMeta):
    def __init__(self, timeout: float = 5):
        self.recv_queue_map: Mapping[str, Queue] = {}
        self.timeout = timeout

    @abstractmethod
    def send(self, data: bytes, net_type: str, timeout: float) -> bool:
        """Send bytes data to the network"""

    @abstractmethod
    def recv(self, net_type: str, timeout: float) -> Iterator[bytes]:
        """Receive bytes data from the network"""
