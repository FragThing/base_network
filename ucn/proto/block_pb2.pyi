from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class BasicBlock(_message.Message):
    __slots__ = ["data", "previous_block_hash", "protocol"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_BLOCK_HASH_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    previous_block_hash: str
    protocol: str
    def __init__(self, previous_block_hash: _Optional[str] = ..., protocol: _Optional[str] = ..., data: _Optional[bytes] = ...) -> None: ...
