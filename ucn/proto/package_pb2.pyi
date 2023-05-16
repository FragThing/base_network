from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class TransferHeader(_message.Message):
    __slots__ = ["checksum", "length", "protocol", "source"]
    CHECKSUM_FIELD_NUMBER: _ClassVar[int]
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    checksum: int
    length: int
    protocol: str
    source: str
    def __init__(self, source: _Optional[str] = ..., protocol: _Optional[str] = ..., length: _Optional[int] = ..., checksum: _Optional[int] = ...) -> None: ...
