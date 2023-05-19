from sqlalchemy import create_engine, Engine, select
from sqlalchemy.orm import Session
from ucn.proto.block_pb2 import BasicBlock
from ..error import InvalidPreviousBlockHashError, MissingGenesisBlockError
from .models import init_database, get_block_model
from .base_store import BaseBlockStore


class LocalBlockStore(BaseBlockStore):
    def __init__(self, engine: Engine, chain_name: str = "blocks"):
        self.engine = engine
        self.BLOCK_MODEL = get_block_model(chain_name)
        init_database(self.engine)

    def add_block(
        self, protocol: str, data: bytes, previous_block_hash: str
    ) -> str:  # Return type has been changed from BasicBlock to str.
        block = BasicBlock(
            protocol=protocol,
            previous_block_hash=previous_block_hash,
            data=data,
        )

        block_hash = self.get_hash(block)

        with Session(self.engine) as session:
            # Retrieve the latest block in the database
            latest_block = (
                session.query(self.BLOCK_MODEL)
                .order_by(self.BLOCK_MODEL.block_index.desc())
                .first()
            )
            if latest_block:
                # If the previous_block_hash does not match the hash of the latest block, raise an error
                if latest_block.block_hash != previous_block_hash:
                    raise InvalidPreviousBlockHashError(
                        "Invalid previous block hash: The given previous block hash does not match the hash of the latest block in the database."
                    )
            elif previous_block_hash:
                # If the genesis block does not exist in the database yet, raise an error
                raise MissingGenesisBlockError(
                    "Missing genesis block: The database does not contain a genesis block yet."
                )

            # Compute the index for the new block
            new_block_index = latest_block.block_index + 1 if latest_block else 0

            # Create a new block model and add it to the database
            block_model = self.BLOCK_MODEL(
                protocol=block.protocol,
                data=block.data,
                previous_block_hash=block.previous_block_hash,
                block_hash=block_hash,
                block_index=new_block_index,
            )
            session.add(block_model)
            session.commit()

        # Return the hash of the new block
        return block_hash

    def get_block(self, block_hash: str) -> BasicBlock or None:
        with Session(self.engine) as session:
            # Retrieve the block model with the specified block hash
            block_model = session.scalar(
                select(self.BLOCK_MODEL).where(
                    self.BLOCK_MODEL.block_hash == block_hash
                )
            )
            if block_model:
                # Convert the block model to a BasicBlock object and return it
                block = BasicBlock(
                    protocol=block_model.protocol,
                    previous_block_hash=block_model.previous_block_hash,
                    data=block_model.data,
                )
                return block
        return None

    def get_block_by_index(self, block_index: int) -> BasicBlock or None:
        with Session(self.engine) as session:
            # If block_index is -1, retrieve the latest block
            if block_index == -1:
                block_model = (
                    session.query(self.BLOCK_MODEL)
                    .order_by(self.BLOCK_MODEL.block_index.desc())
                    .first()
                )
            else:
                # Otherwise, retrieve the block model with the specified block index
                block_model = session.scalar(
                    select(self.BLOCK_MODEL).where(
                        self.BLOCK_MODEL.block_index == block_index
                    )
                )

            if block_model:
                # Convert the block model to a BasicBlock object and return it
                return BasicBlock(
                    protocol=block_model.protocol,
                    previous_block_hash=block_model.previous_block_hash,
                    data=block_model.data,
                )
        return None

    def get_block_count(self) -> int:
        with Session(self.engine) as session:
            # Return the total count of blocks in the database
            return session.query(self.BLOCK_MODEL).count()


# Create an engine
engine = create_engine("sqlite:///:memory:")

# Create a new instance of the LocalBlockStore class
local_block_store = LocalBlockStore(engine)
