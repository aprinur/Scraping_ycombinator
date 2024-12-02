from sqlalchemy import Column, Integer, String
from db_config import Base, engine


class Format_SQL(Base):
    __tablename__ = 'Company_in_ycombinator'

    id = Column(Integer, primary_key=True)
    Name = Column(String, unique=True)
    Batch = Column(String, nullable=False)
    Sector = Column(String, nullable=False)
    Region = Column(String, nullable=False)
    Company_Desc = Column(String, nullable=False)
    Founding_Date = Column(Integer, nullable=False)
    Founders = Column(String, nullable=False)
    Incubator = Column(String, nullable=False)
    Location = Column(String, nullable=False)
    Source_Url = Column(String, nullable=False)
    Company_Url = Column(String, nullable=False)


Base.metadata.create_all(engine)
