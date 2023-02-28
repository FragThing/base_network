from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Bill(_message.Message):
    __slots__ = ["root", "timestamp", "transfer", "version"]
    ROOT_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    TRANSFER_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    root: str
    timestamp: int
    transfer: Transfer
    version: int
    def __init__(self, version: _Optional[int] = ..., root: _Optional[str] = ..., timestamp: _Optional[int] = ..., transfer: _Optional[_Union[Transfer, _Mapping]] = ...) -> None: ...

class Coin(_message.Message):
    __slots__ = ["account", "bill_url"]
    ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    BILL_URL_FIELD_NUMBER: _ClassVar[int]
    account: str
    bill_url: str
    def __init__(self, bill_url: _Optional[str] = ..., account: _Optional[str] = ...) -> None: ...

class Destination(_message.Message):
    __slots__ = ["account", "num"]
    ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    NUM_FIELD_NUMBER: _ClassVar[int]
    account: str
    num: int
    def __init__(self, account: _Optional[str] = ..., num: _Optional[int] = ...) -> None: ...

class Sign(_message.Message):
    __slots__ = ["account", "sign"]
    ACCOUNT_FIELD_NUMBER: _ClassVar[int]
    SIGN_FIELD_NUMBER: _ClassVar[int]
    account: str
    sign: bytes
    def __init__(self, account: _Optional[str] = ..., sign: _Optional[bytes] = ...) -> None: ...

class SignData(_message.Message):
    __slots__ = ["data", "sign_list"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    SIGN_LIST_FIELD_NUMBER: _ClassVar[int]
    data: str
    sign_list: _containers.RepeatedCompositeFieldContainer[Sign]
    def __init__(self, sign_list: _Optional[_Iterable[_Union[Sign, _Mapping]]] = ..., data: _Optional[str] = ...) -> None: ...

class Transfer(_message.Message):
    __slots__ = ["coin_list", "dest_list"]
    COIN_LIST_FIELD_NUMBER: _ClassVar[int]
    DEST_LIST_FIELD_NUMBER: _ClassVar[int]
    coin_list: _containers.RepeatedCompositeFieldContainer[Coin]
    dest_list: _containers.RepeatedCompositeFieldContainer[Destination]
    def __init__(self, coin_list: _Optional[_Iterable[_Union[Coin, _Mapping]]] = ..., dest_list: _Optional[_Iterable[_Union[Destination, _Mapping]]] = ...) -> None: ...
