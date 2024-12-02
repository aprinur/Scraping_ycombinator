import pandas, datetime
from db_config import session, engine
from db_config.db_format import Format_SQL
from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font


def db_to_file(db_table: str, filename: str, sheet_title: str = 'Scraping result', sheet_desc: str = None ):
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
        print(f'Saving to file as: {filename}')

    df.to_csv(fr'D:\Github\aprinur\scrape_ycombinator.com\{filename}_{date}.csv', index=False)



def insert_to_db(scrape_result: Format_SQL):
    """ This method used to insert data into database."""
    session.add(scrape_result)
    session.commit()


def check_data(data):
    exists =  session.query(Format_SQL).filter_by(Name=data.Name).first()
    return exists is not None

