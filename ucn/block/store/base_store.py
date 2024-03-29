from abc import ABCMeta, abstractmethod

import hashlib
from google.protobuf import message

from ucn.block.data.basic_block import BasicBlock


class BaseBlockStore(metaclass=ABCMeta):
    @abstractmethod
    def add_block(
        self, protocol: str, data: bytes, previous_block_hash: str
    ) -> BasicBlock:
        pass

    @abstractmethod
    def get_block(self, block_hash: str) -> BasicBlock or None:
        pass

    @abstractmethod
    def get_block_by_index(self, block_index: int) -> BasicBlock or None:
        pass

    @abstractmethod
    def get_block_count(self) -> int:
        return 0

    @abstractmethod
    def remove_block(self, block_hash: str) -> list[BasicBlock]:
        pass

    @abstractmethod
    def remove_block_by_index(self, block_index: int) -> list[BasicBlock]:
        pass

    @staticmethod
    def get_hash(block: BasicBlock) -> str:

        # Get binary representation of block
        block_bin = block.serialize()

        # Compute and return hash
        return f"sha256:{hashlib.sha256(block_bin).hexdigest()}"
