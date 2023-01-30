"""Data store template"""
from abc import ABCMeta, abstractmethod


class BaseStore(metaclass=ABCMeta):
    """Data store base template"""

    @abstractmethod
    def read(self, *path: str) -> bytes:
        """Read data from file"""

    @abstractmethod
    def save(self, content: bytes, *path: str):
        """Save data from file"""
