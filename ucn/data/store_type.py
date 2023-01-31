"""The way of data store"""

from enum import Enum


class StoreType(Enum):
    """Data storeroom type"""

    UCN = "ucn"
    IPFS = "ipfs"
    GNUNET = "gnunet"
    HTTP = "http"
