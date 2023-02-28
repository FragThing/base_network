"""Transfer item data"""
from dataclasses import dataclass
from ucn.pay.data.coin_data import CoinData


@dataclass
class DestinationData:
    """Transfer destination"""

    account: str
    num: int


@dataclass
class TransferData:
    """Coin tranfer"""

    coin_list: list[CoinData]
    dest_list: list[DestinationData]
