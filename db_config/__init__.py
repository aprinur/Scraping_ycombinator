from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


DB_URL = f'sqlite:///D:/Github/aprinur/scrape_ycombinator.com/ycombinator.db'
engine = create_engine(DB_URL, echo=False)
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()

