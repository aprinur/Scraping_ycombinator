import pandas, datetime
from db_config import session, engine
from db_config.db_format import Format_SQL
from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font


def db_to_file(db_table: str = 'Company_in_ycombinator', filename: str = 'ycombinator company scraping result', sheet_title: str = 'Scraping result', sheet_desc: str = None ):
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



def insert_to_db(scrape_result: Format_SQL):
    """ This method used to insert data into database."""
    session.add(scrape_result)
    session.commit()


def check_data(data):
    """ Check is scraped data already in database """
    exists =  session.query(Format_SQL).filter_by(Name=data.Name).first()
    return exists is not None



def user_input():

    while True:
        user_option = input("""
1. Scrape company
2. Export database into xlsx and csv
3. Quit

Choose Option (1/2/3) : """)

        if not user_option.isdigit():
            print('Input only number')
            continue

        if user_option == '1':
            while True:
                count = input('Input total page to scrape (empty = all pages): ')
                if count and not count.isdigit():
                    print('Input must be a number')
                    continue
                count = int(count) if count else None
                url = input('Input Url after filtering company: ')
                if not url.strip():
                    print(" Url cannot be empty")
                    continue
                return count, url

        elif user_option == '2':
            while True:
                filename = input('Input filename (optional): ') or None
                sheet_title = input('Input sheet title (optional): ') or None
                sheet_desc = input('Input sheet description (optional) : ') or None

                args = {}
                if filename:
                    args["filename"] = filename
                if sheet_title:
                    args['sheet_title'] = sheet_title
                if sheet_desc:
                    args['sheet_desc'] = sheet_desc

                try:
                    db_to_file(**args)
                    return False
                except Exception as e:
                    print(e)
        elif user_option == '3':
            return False
        else:
            print('Out of option')