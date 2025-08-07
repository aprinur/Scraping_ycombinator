
from selenium import webdriver

from .db_format import create_db_table, get_existing_table_class, Session, engine


options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

sql_reserved_keyword = {
    "select", "insert", "update", "delete", "from", "where", "join",
    "group", "by", "order", "limit", "table", "create", "drop",
    "alter", "index", "and", "or", "not", "null", "into", "values", "all"
}
