"""Coin transfer controller"""
from ucn.utils import get_timestamp
from ucn.pay.data.transfer_data import TransferData, DestinationData
from ucn.pay.data.bill_data import BillData
from ucn.pay.data.coin_data import CoinData
from ucn.pay.data.base_dataclass import BaseData, SignItem
from ucn.pay.error import TranferVerifyError, CoinBillRootError, CoinDataVerifyError
from ucn.encoder.bytes_encoder import bill_encode_bytes
from ucn.ledger.ledger import ledger
from ucn.account.wallet_getter import get_account


class Bill:
    """Coin tranfer"""

    def __init__(self, data: BaseData):
        self.data = data

    @property
    def bill_data(self) -> BillData:
        """Get TranferData"""
        return self.data.data

    def sign(self, sign_func):
        bill_bytes = bill_encode_bytes(self.data.data)


def new_bill(coin_list: list[CoinData], dest_list: list[DestinationData]):
    """New bill"""
    check_coin_data(coin_list, dest_list)
    transfer_data = TransferData(
        coin_list=coin_list,
        dest_list=[DestinationData(account=dest[0], num=dest[1]) for dest in dest_list],
    )
    root_bill_url = get_root_bill_url(coin_list)
    bill_data = BillData(
        root_bill_url=root_bill_url,
        timestamp=get_timestamp(),
        transfer=transfer_data,
    )
    sign_list = new_sign_list(bill_data)
    return Bill(BaseData(sign_list=sign_list, data=bill_data))


def get_bill(bill_url: str) -> BillData:
    """Get BillData from ledger"""
    return ledger.get(bill_url)


def new_sign_list(bill_data: BillData) -> list[SignItem]:
    """New sign_list for BillData"""
    bill_bytes = bill_encode_bytes(bill_data)
    sign_list = []
    for coin in bill_data.transfer.coin_list:
        account = get_account(coin.account)
        sign = account.key.sign(bill_bytes)
        sign_list.append(SignItem(account=account, sign=sign))
    return sign_list


def check_coin_data(coin_list: list[CoinData], dest_list: list[DestinationData]):
    """Check CoinData is coincide with bill"""
    coin_num = 0
    for coin in coin_list:
        bill = get_bill(coin.bill_url)
        for dest in bill.transfer.dest_list:
            if dest.account == coin.account:
                coin_num += dest.num
            else:
                raise CoinDataVerifyError(coin_list)
    total_num = 0
    for dest in dest_list:
        total_num += dest.num
    if coin_num != total_num:
        raise CoinDataVerifyError(coin_list)


def get_root_bill_url(coin_list: list[CoinData]) -> str:
    """Get bill root from coins"""
    root_url = coin_list[0].bill.root_bill_url
    for i in range(1, len(coin_list)):
        if coin_list[i] == root_url:
            continue
        raise CoinBillRootError(coin_list)
    return root_url
