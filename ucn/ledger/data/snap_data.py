"""Snap blockchain item data"""

from dataclasses import dataclass
from ucn.ledger.data.bill_data import BillData


@dataclass
class LegerSnap:
    """Ledger snap data"""

    prev_snap_url: str
    block_hight: int
    bill_list: list[BillData]
