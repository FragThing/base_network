"""Coin transfer encoder"""
from ucn.proto.coin_transfer_pb2 import Destination, Transfer, Sign, SignData
from ucn.pay.data.base_dataclass import SignItem, BaseData
from ucn.pay.data.transfer_data import DestinationData, TransferData


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


def transfer_encode(data: TransferData) -> Transfer:
    """Encode TransferData to Transfer protobuf"""
    return Transfer(
        coin_list=data.coin_list,
        dest_list=[destination_encode(dest) for dest in data.dest_list],
    )


def transfer_decode(data: Transfer) -> TransferData:
    """Decode Transfer protobuf to TransferData"""

    return TransferData(
        coin_list=data.coin_list,
        dest_list=[destination_decode(dest) for dest in data.dest_list],
    )


def data_encode(data: BaseData) -> SignData:
    """Encode BaseData to SignData protobuf"""
    return SignData(
        sign_list=[sign_encode(sign) for sign in data.sign_list],
        data=transfer_encode(data.data),
    )


def data_decode(data: SignData) -> BaseData:
    """Decode SignData protobuf to BaseData"""
    return BaseData(
        sign_list=[sign_decode(sign) for sign in data.sign_list],
        data=transfer_decode(data.data),
    )
