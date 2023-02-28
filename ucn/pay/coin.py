"""Coin checker"""
from ucn.pay.data.bill_data import BillData
from ucn.ledger.ledger import ledger


class Coin:
    """Check Coin data and num"""

    def __init__(self, bill: BillData, account: str):
        self.bill = bill
        self.account = account

    def verify(self) -> int:
        """Verify coin is belong to account and return coin quantity"""
