"""Coin transfer encoder"""
from enum import Enum, auto

from ucn.proto.coin_transfer_pb2 import (
    Destination,
    Coin,
    Transfer,
    Bill,
    Sign,
    SignData,
)
from ucn.pay.data.base_dataclass import SignItem, BaseData
from ucn.pay.data.coin_data import CoinData
from ucn.pay.data.transfer_data import DestinationData, TransferData
from ucn.pay.data.bill_data import BillData


class DataType(Enum):
    """Data type of protobuf"""

    BILL = auto()


def sign_encode(data: SignItem) -> Sign:
    """Encode SignItem to Sign protobuf"""
    return Sign(account=data.account, sign=data.sign)


def sign_decode(data: Sign) -> SignItem:
    """Decode Sign protobuf to SignItem"""
    return SignData(account=data.account, sign=data.sign)


def destination_encode(data: DestinationData) -> Destination:
    """Encode DestinationData to Destination protobuf"""
    return Destination(account=data.account, num=data.num)


def destination_decode(data: Destination) -> DestinationData:
    """Decode Destination protobuf to DestinationData"""
    return DestinationData(account=data.account, num=data.num)


def coin_encode(data: CoinData) -> Coin:
    """Encode CoinData to Coin protobuf"""
    return Coin(bill_url=data.bill_url, account=data.account)


def coin_decode(data: Coin) -> CoinData:
    """Decode Coin protobuf to CoinData"""
    return CoinData(bill_url=data.bill_url, account=data.account)


def transfer_encode(data: TransferData) -> Transfer:
    """Encode TransferData to Transfer protobuf"""
    return Transfer(
        coin_list=[coin_encode(coin) for coin in data.coin_list],
        dest_list=[destination_encode(dest) for dest in data.dest_list],
    )


def transfer_decode(data: Transfer) -> TransferData:
    """Decode Transfer protobuf to TransferData"""

    return TransferData(
        coin_list=[coin_decode(coin) for coin in data.coin_list],
        dest_list=[destination_decode(dest) for dest in data.dest_list],
    )


def bill_encode(data: BillData) -> Bill:
    """Encode Bill protobuf to BillData"""

    return Bill(
        version=data.version,
        root=data.root_bill_url,
        timestamp=data.timestamp,
        transfer=transfer_encode(data.transfer),
    )


def bill_decode(data: Bill) -> BillData:
    """Decode Bill protobuf to BillData"""

    return BillData(
        version=data.version,
        root_bill_url=data.root,
        timestamp=data.timestamp,
        transfer=transfer_decode(data.transfer),
    )


def data_encode(data: BaseData, data_type: DataType) -> SignData:
    """Encode BaseData to SignData protobuf"""
    if data_type is DataType.BILL:
        str_data = bill_encode(data.data).SerializeToString()
    return SignData(
        sign_list=[sign_encode(sign) for sign in data.sign_list],
        data=str_data,
    )


def data_decode(data: SignData, data_type: DataType) -> BaseData:
    """Decode SignData protobuf to BaseData"""
    if data_type is DataType.BILL:
        data_class_obj = Bill.ParseFromString(transfer_decode(data.data))
    return BaseData(
        sign_list=[sign_decode(sign) for sign in data.sign_list],
        data=data_class_obj,
    )
