"""Coin transfer controller"""
from ucn.pay.data.transfer_data import TransferData, DestinationData
from ucn.pay.data.base_dataclass import BaseData, SignItem
from ucn.encoder.transfer_data import transfer_encode, transfer_decode
from ucn.pay.error import TranferVerifyError


class Transfer:
    """Coin tranfer"""

    def __init__(self, data: BaseData):
        self.data = data

    @property
    def tranfer_data(self) -> TransferData:
        """Get TranferData"""
        return transfer_decode(self.data.data)


def new_tranfer(
    coin_list: list[str], dest_list: list[tuple[str, int]], sign_func_map
) -> Transfer:
    """New tranfer"""
    transfer_data = TransferData(
        coin_list=coin_list,
        dest_list=[DestinationData(account=dest[0], num=dest[1]) for dest in dest_list],
    )
    transfer_bytes = transfer_encode(transfer_data)
    sign_list = [
        SignItem(account=account, sign=func(transfer_bytes))
        for account, func in sign_func_map
    ]
    return Transfer(data=BaseData(sign_list=sign_list, data=transfer_data))


def input_transfer(data: BaseData, verify_func_map) -> Transfer:
    """Init transfer by exist tranfer data"""
    for sign_item in data.sign_list:
        if not verify_func_map[sign_item.account](data.data, sign_item.sign):
            raise TranferVerifyError(data)
    return Transfer(data=data)
