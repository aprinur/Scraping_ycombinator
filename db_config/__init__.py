from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from selenium import webdriver


DB_URL = f'sqlite:///D:/Github/aprinur/scrape_ycombinator.com/ycombinator.db'
engine = create_engine(DB_URL, echo=False)
Base = declarative_base()

Session = scoped_session(sessionmaker(bind=engine))

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)