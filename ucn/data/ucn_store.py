"""Data store saver"""

from urllib.parse import urlparse
from ucn.data.base_local_store import base_local_store
from ucn.url_parse import url_parse

from ucn.network.network_wrap import send
from ucn.network.net_type import DataStoreType


class UCNDataStore:
    """UCN Data store controller"""

    def read(self, url) -> bytes or None:
        """Read bytes content by URL string
        If URL check fail return None
        """
        content = self.__read_local(url)
        if not content:
            content = self.__read_net(url)
        encode_algo = urlparse(url).scheme
        if url_parse.encode(content, encode_algo) == url:
            return content
        return None

    def save(self, content: bytes) -> str:
        """Save bytes content and return URL string"""
        url = url_parse.encode(content, force_hash=True)
        self.__save_local(url, content)
        self.__save_net(url, content)
        return url

    def __read_local(self, url: str) -> bytes or None:
        """Read data in local"""
        try:
            return base_local_store.read(base_local_store.FILE_STORE, url)
        except FileNotFoundError:
            return None

    def __read_net(self, url: str) -> bytes or None:
        """Request data in ucn network"""
        return send(DataStoreType.READ, url.encode("utf-8"))

    def __save_local(self, url: str, data) -> bytes or None:
        """Save data in local"""
        try:
            return base_local_store.save(data, base_local_store.FILE_STORE, url)
        except FileNotFoundError:
            return None

    def __save_net(self, url: str, data) -> bytes or None:
        """Push data in ucn network"""
        return send(DataStoreType.SAVE, url.encode("utf-8") + "\n" + data)


ucn_store = UCNDataStore()
