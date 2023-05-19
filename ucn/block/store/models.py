from sqlalchemy import Engine, Column, Integer, String, LargeBinary
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BasicBlockModel(Base):
    __abstract__ = True
    protocol = Column(String)
    data = Column(LargeBinary)
    block_hash = Column(String, index=True, unique=True)
    previous_block_hash = Column(String, nullable=True)
    block_index = Column(Integer, primary_key=True)


class BlockModel(BasicBlockModel):
    __tablename__ = "blocks"


BLOCK_MODEL_MAP = {cls.__tablename__: cls for cls in BasicBlockModel.__subclasses__()}


def init_database(engine: Engine):
    Base.metadata.create_all(engine)


def get_block_model(tablename: str = "blocks"):
    return BLOCK_MODEL_MAP[tablename]
