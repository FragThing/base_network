"""Define message type when node chat each other
It can save network and focus what need
"""
from enum import IntEnum

VERSION = 0


class BaseType(IntEnum):
    """Base network type, for Auto-Complete"""


class AccountType(BaseType):
    """Account"""

    REGISTER = int(f"{VERSION}00")
    SEARCH = int(f"{VERSION}01")
    ABANDON = int(f"{VERSION}02")


class PayType(BaseType):
    """Pay"""

    PULL = int(f"{VERSION}10")
    PUSH = int(f"{VERSION}11")


class LedgerType(BaseType):
    """Ledger"""

    RELEASE = int(f"{VERSION}20")


class DataStoreType(BaseType):
    """Data store"""

    SAVE = int(f"{VERSION}30")
    READ = int(f"{VERSION}31")


TYPE_LIST = BaseType.__subclasses__()
