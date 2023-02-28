"""Bill data for one bill"""
from dataclasses import dataclass

from ucn.pay.data.transfer_data import TransferData


@dataclass
class BillData:
    """Bill data class translate from/to raw network data"""

    # The root bill data of the chain
    # which as chain id
    root_bill_url: str
    # Timestamp of bill release time
    timestamp: float
    # transfer data
    transfer: TransferData

    # structure version
    version: int = 0
