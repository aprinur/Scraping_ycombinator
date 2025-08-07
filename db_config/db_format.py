from sqlalchemy import Column, Integer, String
from db_config import Base, engine
from sqlalchemy import inspect


class YCombinatorTable(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    Company_Name = Column(String, unique=True)
    Batch = Column(String,)
    Sector = Column(String,)
    Region = Column(String,)
    Company_Desc = Column(String,)
    Founding_Date = Column(Integer,)
    Founders = Column(String,)
    Incubator = Column(String,)
    Location = Column(String,)
    Source_Url = Column(String, unique=True)
    Company_Url = Column(String,)


def get_existing_table_class(tablename):
    """ Get an existing table with YCombinatorTable class structure"""
    inspector = inspect(engine)

    if not inspector.has_table(tablename):
        raise ValueError(f'Table {tablename} does not exist in the database')

    class ExistingTable(YCombinatorTable):
        __tablename__ = tablename
        __table_args__ = {'extend_existing': True}

    return ExistingTable


def create_db_table(tablename: str):
    """ Create new table based on YCombinatorTable class structure"""

    class DynamicTable(YCombinatorTable):
        __tablename__ = tablename
        __table_args__ = {'extend_existing': True}

    Base.metadata.create_all(engine)
    return DynamicTable
