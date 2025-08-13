import os
import tempfile
from pathlib import Path

from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

Base = declarative_base()


class YCombinatorTable(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    Company_Name = Column(String, unique=True)
    Batch = Column(String,)
    Sector = Column(String,)
    Location = Column(String,)
    Company_Desc = Column(String,)
    Founding_Date = Column(Integer,)
    Founders = Column(String,)
    Incubator = Column(String,)
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


def get_db_path():
    try:
        current_dir = os.path.abspath(os.getcwd())
        db_path = os.path.join(current_dir, 'ycombinator.db')
        Path(db_path).touch()
        print(f'Database will be saved in: {db_path}')
        return f'sqlite:///{db_path}'
    except Exception:
        try:
            home_dir = str(Path.home())
            print(home_dir)
            db_path = os.path.join(home_dir, "ycombinator.db")
            Path(db_path).touch()
            print(f'Database will be saved in: {db_path}')
            return f"sqlite:///{db_path}"
        except Exception:
            temp_dir = tempfile.gettempdir()
            print(temp_dir)
            db_path = os.path.join(temp_dir, 'ycombinator.db')
            print(f'Database will be saved in: {db_path}')
            return f'sqlite:///{db_path}'


DB_URL = get_db_path()
engine = create_engine(DB_URL, echo=False)

Session = scoped_session(sessionmaker(bind=engine))
