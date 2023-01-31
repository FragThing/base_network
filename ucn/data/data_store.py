"""Data store wrapper"""

from ucn.url_parse import url_parse
from ucn.data.store_type import StoreType
from ucn.data.ucn_store import ucn_store
from ucn.network.net_type import BaseType


class DataStore:
    """Data store wrapper"""

    def read(self, url: str, net_type: BaseType = None) -> bytes or None:
        """Read data"""
        scheme_list = url_parse.get_scheme(url)
        store_type = StoreType(scheme_list.pop())
        re_url = url_parse.reset_scheme(url, scheme_list)
        if store_type is StoreType.UCN:
            return ucn_store.read(net_type, re_url)
        return None

    def save(self, store_type: StoreType, content: bytes, net_type: BaseType = None) -> str:
        """Save data from file"""
        if store_type is StoreType.UCN:
            url = ucn_store.save(net_type, content)
        scheme_list = url_parse.get_scheme(url)
        scheme_list.insert(0, store_type.value)
        return url_parse.reset_scheme(url, scheme_list)
