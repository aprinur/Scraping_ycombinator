import os
import tempfile
from pathlib import Path

from selenium import webdriver
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

from .db_format import create_db_table, get_existing_table_class


def get_db_path():
    try:
        current_dir = os.path.abspath(os.getcwd())
        db_path = os.path.join(current_dir, 'ycombinator.db')
        Path(db_path).touch()
        print(f'Database will be saved in: {db_path}')
        return f'sqlite:///{db_path}'
    except:
        try:
            home_dir = str(Path.home())
            print(home_dir)
            db_path = os.path.join(home_dir, "ycombinator.db")
            Path(db_path).touch()
            print(f'Database will be saved in: {db_path}')
            return f"slite:///{db_path}"
        except:
            temp_dir = tempfile.gettempdir()
            print(temp_dir)
            db_path = os.path.join(temp_dir, 'ycombinator.db')
            print(f'Database will be saved in: {db_path}')
            return f'sqlite:///{db_path}'


DB_URL = get_db_path()
engine = create_engine(DB_URL, echo=False)
Base = declarative_base()

Session = scoped_session(sessionmaker(bind=engine))

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

sql_reserved_keyword = {
    "select", "insert", "update", "delete", "from", "where", "join",
    "group", "by", "order", "limit", "table", "create", "drop",
    "alter", "index", "and", "or", "not", "null", "into", "values", "all"
}
