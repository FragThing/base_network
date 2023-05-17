from abc import ABCMeta, abstractmethod

import hashlib
from google.protobuf import message

from ucn.proto.block_pb2 import BasicBlock


class BaseBlockStore(metaclass=ABCMeta):
    @abstractmethod
    def add_block(
        self, protocol: str, data: bytes, previous_block_hash: str
    ) -> BasicBlock:
        pass

    @abstractmethod
    def get_block(self, block_hash: str) -> BasicBlock or None:
        pass

    @staticmethod
    def get_hash(block: BasicBlock) -> str:
        # Ensure block is a protobuf message
        if not isinstance(block, message.Message):
            raise ValueError("block must be a protobuf message")

        # Get binary representation of block
        block_bin = block.SerializeToString()

        # Compute and return hash
        return f"sha256:{hashlib.sha256(block_bin).hexdigest()}"
