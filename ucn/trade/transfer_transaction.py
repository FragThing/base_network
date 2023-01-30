"""Transaction of Transfer data header"""

from dataclasses import dataclass

@dataclass
class TransferTrasaction:
    """Transfer data header pay back transaction"""
    timestamp: int
    account: str
    gas_coin_num: str
