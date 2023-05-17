from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import Session
from ucn.proto.block_pb2 import BasicBlock
from .models import init_database, get_block_model
from .base_store import BaseBlockStore


class LocalBlockStore(BaseBlockStore):
    def __init__(self, engine: Engine):
        self.engine = engine
        init_database(self.engine)

    def add_block(
        self, protocol: str, data: bytes, previous_block_hash: str
    ) -> BasicBlock:
        block = BasicBlock(
            protocol=protocol,
            previous_block_hash=previous_block_hash,
            data=data,
        )

        block_model = get_block_model()(
            protocol=block.protocol,
            previous_block_hash=block.previous_block_hash,
            data=block.data,
        )
        with Session(self.engine) as session:
            session.add(block_model)
            session.commit()
        return block

    def get_block(self, block_hash: str) -> BasicBlock or None:
        with Session(self.engine) as session:
            block_query = session.query(get_block_model()).yield_per(100)
            for block_model in block_query:
                block = BasicBlock(
                    protocol=block_model.protocol,
                    previous_block_hash=block_model.previous_block_hash,
                    data=block_model.data,
                )
                if self.get_hash(block) == block_hash:
                    return block
        return None


# Create an engine
engine = create_engine("sqlite:///:memory:")

# Create a new instance of the LocalBlockStore class
local_block_store = LocalBlockStore(engine)
