from sqlalchemy import Engine, Column, Integer, String, LargeBinary
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class BasicBlockModel(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True)
    protocol = Column(String)
    data = Column(LargeBinary)
    previous_block_hash = Column(String)


class BlockModel(BasicBlockModel):
    __tablename__ = "blocks"


MODEL_MAP = {cls.__tablename__: cls for cls in BasicBlockModel.__subclasses__()}


def init_database(engine: Engine):
    Base.metadata.create_all(engine)


def get_block_model(tablename: str = "blocks"):
    return MODEL_MAP[tablename]
