from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AccountBlock(_message.Message):
    __slots__ = ["creation_time", "encode_algo", "public_keys"]
    CREATION_TIME_FIELD_NUMBER: _ClassVar[int]
    ENCODE_ALGO_FIELD_NUMBER: _ClassVar[int]
    PUBLIC_KEYS_FIELD_NUMBER: _ClassVar[int]
    creation_time: int
    encode_algo: int
    public_keys: _containers.RepeatedCompositeFieldContainer[PublicKey]
    def __init__(self, creation_time: _Optional[int] = ..., encode_algo: _Optional[int] = ..., public_keys: _Optional[_Iterable[_Union[PublicKey, _Mapping]]] = ...) -> None: ...

class AdditionalBlock(_message.Message):
    __slots__ = ["account_url", "data", "protocol"]
    ACCOUNT_URL_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    account_url: str
    data: bytes
    protocol: str
    def __init__(self, protocol: _Optional[str] = ..., account_url: _Optional[str] = ..., data: _Optional[bytes] = ...) -> None: ...

class PublicKey(_message.Message):
    __slots__ = ["algorithm", "key"]
    ALGORITHM_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    algorithm: str
    key: bytes
    def __init__(self, algorithm: _Optional[str] = ..., key: _Optional[bytes] = ...) -> None: ...
