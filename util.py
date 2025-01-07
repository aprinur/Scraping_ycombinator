import pandas, datetime
from db_config import Session, engine, Base
from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font
from sqlalchemy import inspect
import traceback


def db_to_file( db_table, sheet_desc: str, sheet_title: str = "YCombinator Scraping Result", filename: str = 'ycombinator company scraping result' ):
    ''' Method to save db into excel and csv file '''
    date = datetime.datetime.now().strftime('%d_%B_%Y')
    query = f"SELECT * FROM {db_table}"
    df = pandas.read_sql_query(query, engine)

    with pandas.ExcelWriter(f'{filename}_{date}.xlsx', engine='openpyxl') as writer:
        df.to_excel(writer, index=False, startrow=3, sheet_name='Sheet_1')
        worksheet = writer.sheets['Sheet_1']

        worksheet.merge_cells('A1:E1')
        worksheet.merge_cells('A2:E2')
        worksheet['A1'] = sheet_title
        worksheet['A2'] = sheet_desc

        worksheet['A1'].font = Font(name='Times New Roman', size=16, bold=True)
        worksheet['A1'].alignment = Alignment(horizontal='center', vertical='center')
        worksheet['A2'].alignment = Alignment(horizontal='left', vertical='center')
        print(f'Saved to file as: {filename}')

    df.to_csv(fr'D:\Github\aprinur\scrape_ycombinator.com\{filename}_{date}.csv', index=False)



def insert_to_db(scrape_result, table_class):
    """ This method used to insert data into database."""
    with Session() as session:
        table_instance = table_class(**scrape_result)
        session.add(table_instance)
        session.commit()


def check_data(data, table_class):
    """ Check if scraped data already in database """
    with Session() as session:
        exists =  session.query(table_class).filter_by(Name=data["Name"]).first()
        return exists is not None



def user_input():
    """ Function to handling what to do """
    while True:
        user_option = input("""
1. Scrape company
2. Export database into xlsx and csv file
3. Quit

Choose Option (1/2/3) : """)

        if not user_option.isdigit():
            print('Input only number')
            continue

        if user_option == '1':
            while True:
                url = input('Url: ')
                if not url.strip():
                    print(" Url cannot be empty")
                    continue
                break

            while True:
                count = input('Total Company (empty = all company): ')
                if count and not count.isdigit():
                    print('Input must be a number')
                    continue
                count = int(count) if count else None
                return count, url

        elif user_option == '2':
            while True:
                while True:
                    tablename = input('Input table name: ')
                    if not tablename.strip():
                        print('Table name cannot be empty')
                        continue
                    if not check_table_exists(tablename, engine):
                        print("Table not found! Enter existing table from database ")
                        continue
                    break
                filename = input('Input filename (optional): ').strip() or None
                sheet_title = input('Input sheet title (optional): ').strip() or None
                sheet_desc = input('Input sheet description (optional) : ').strip() or (f'This file saved from table '
                                                                                        f'{tablename} in ycombinator '
                                                                                        f'database')

                args = {}
                if filename:
                    args["filename"] = filename
                if sheet_title:
                    args['sheet_title'] = sheet_title
                if sheet_desc:
                    args['sheet_desc'] = sheet_desc
                args['db_table'] = tablename

                try:
                    db_to_file(**args)
                    return False
                except Exception as e:
                    print(f'Cannot save table to file: {e}')
                    traceback.print_exc()
        elif user_option == '3':
            return False
        else:
            print('Out of option')


def check_table_exists(tablename: str, engine=engine):
        inspector = inspect(engine)
        return tablename in inspector.get_table_names()


