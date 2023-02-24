"""Coin checker"""
from ucn.pay.transfer import Transfer
from ucn.ledger.ledger import ledger


class Coin:
    """Check Coin data and num"""

    def __init__(self, transfer: Transfer, account: str):
        self.transfer = transfer
        self.account = account

    def verify(self) -> int:
        """Verify coin is belong to account and return coin quantity"""
