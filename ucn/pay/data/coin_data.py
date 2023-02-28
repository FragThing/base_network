"""Coin data with signature in bill"""

from dataclasses import dataclass


@dataclass
class CoinData:
    """Coin data for pay which mark by account"""

    bill_url: str
    account: str
