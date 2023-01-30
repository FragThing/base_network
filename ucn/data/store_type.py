"""The way of data store"""

from enum import Enum


class StoreType(Enum):
    """Data storeroom type"""

    RAW = "raw"
    IPFS = "ipfs"
    GNUNET = "gnunet"
    HTTP = "http"
