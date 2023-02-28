"""Encode class to bytes"""
from ucn.pay.data.bill_data import BillData
from ucn.encoder.transfer_data import bill_encode


def bill_encode_bytes(bill: BillData) -> bytes:
    """Encode BillData to bytes"""
    return bill_encode(bill).SerializeToString().decode("utf-8")
