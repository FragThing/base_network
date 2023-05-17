from ucn.proto.block_pb2 import BasicBlock
from .store.base_store import BaseBlockStore
from .store.local_store import local_block_store


class BlockStore(BaseBlockStore):
    def add_block(self, protocol, data, previous_block_hash=None) -> BasicBlock:
        return local_block_store.add_block(protocol, data, previous_block_hash)

    def get_block(self, block_hash: str) -> BasicBlock or None:
        return local_block_store.get_block(block_hash)
