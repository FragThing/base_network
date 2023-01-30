"""Define message type when node chat each other
It can save network and focus what need
"""
from enum import IntEnum

VERSION = 0


class BaseType(IntEnum):
    """Base network type, for Auto-Complete"""


class AccountType(BaseType):
    """Account type"""

    REGISTER = int(f"{VERSION}00")
    SEARCH = int(f"{VERSION}01")
    ABANDON = int(f"{VERSION}02")


class PayType(BaseType):
    """Pay type"""

    PULL = int(f"{VERSION}10")
    PUSH = int(f"{VERSION}11")


class LedgerType(BaseType):
    """Ledger type"""

    RELEASE = int(f"{VERSION}20")


TYPE_LIST = BaseType.__subclasses__()
