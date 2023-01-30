"""Data store getter
which proxy UCN request to other request or pure data
"""

from ucn.data.base_store import BaseStore
from ucn.data.local_store import local_store


class StoreProxy(BaseStore):
    """Data store proxy getter"""

    def read(self, file_dir: str, file_name: str) -> bytes:
        pass

    def save(self, file_dir: str, file_name: str, content: bytes):
        pass


store_proxy = StoreProxy()
