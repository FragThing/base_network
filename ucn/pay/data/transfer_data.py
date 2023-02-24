"""Transfer item data"""
from dataclasses import dataclass


@dataclass
class DestinationData:
    """Transfer destination"""

    account: str
    num: int


@dataclass
class TransferData:
    """Coin tranfer"""

    coin_list: list[str]
    dest_list: list[DestinationData]
