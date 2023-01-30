"""Cloud store proxy
Such as: ipfs, gnunet
"""
from ucn.data.base_store import BaseStore


class CloudStore(BaseStore):
    """Cloud store proxy"""

    def read(self, file_dir: str, file_name: str) -> bytes:
        pass

    def save(self, file_dir: str, file_name: str, content: bytes):
        pass
