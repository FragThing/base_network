"""Data store saver"""

from urllib.parse import urlparse
from ucn.data.store_proxy import store_proxy
from ucn.url_parse import url_parse


class DataStore:
    """Data store controller"""

    def read(self, url) -> bytes or None:
        """Read bytes content by URL string
        If URL check fail return None
        """
        url_save = urlparse(url)
        encode_algo = url_save.scheme
        content = store_proxy.read(encode_algo, url_save.netloc)
        if url_parse.encode(content, encode_algo) == url:
            return content
        return None

    def save(self, content: bytes) -> str:
        """Save bytes content and return URL string"""
        url = url_parse.encode(content)
        url_save = urlparse(url)
        store_proxy.save(url_save.scheme, url_save.netloc, content)
        return url
