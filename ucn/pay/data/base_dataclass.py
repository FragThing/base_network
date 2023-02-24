"""Base class of pay"""
from dataclasses import dataclass


@dataclass
class SignItem:
    """Sign item data"""

    account: str
    sign: str


@dataclass
class BaseData:
    """Base tranfer data"""

    sign_list: list[SignItem]
    data: object
