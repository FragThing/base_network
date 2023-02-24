"""Coin data with signature in bill"""

from dataclasses import dataclass
from ucn.pay.data.transfer_data import TransferData

@dataclass
class CoinPay:
    """Coin data for pay which mark by account"""
    tranfer: TransferData
    account: str
