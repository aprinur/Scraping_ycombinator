from util import insert_to_db, db_to_file, check_data, user_input, check_table_exists, get_existing_table_class
from db_config.db_format import create_db_table
from scrape import scrape_company_info, scrape_company_url


def main():
    tablename = None
    try:
        choice = user_input()
        if choice is False:
            print('Exiting the program')
            return

        count, url = choice
        table_class = None
        table_ready = False
        while not table_ready:
            tablename = input('Input table name for database: ')
            if not tablename.strip():
                print('Table name cannot be empty!')
                continue

            if not tablename.isidentifier():
                raise ValueError('Table name must be a valid identifier')

            if check_table_exists(tablename):
                while True:
                    append = input('Table already exist, do you want to append data to the existing table (y/n): ').lower()
                    if append not in ['y', 'n']:
                        print("Choose only y or n")
                        continue

                    if append == 'y':
                        try:
                            table_class = get_existing_table_class(tablename)
                            print(f'Appending data to the existing table: {tablename}.')
                            table_ready = True
                            break
                        except ValueError as e:
                            print(e)
                            return
                    else:
                        print('Please input the new table name')
                        break
            else:
                try:
                    table_class = create_db_table(tablename)
                    print(f'New table created: {tablename}')
                    table_ready = True
                    break

                except ValueError as e:
                    print(f'Invalid table name: {e}')
                    continue

        company_urls = scrape_company_url(url, scrape_count=count)
        for company_url in company_urls:
            info = scrape_company_info(company_url, table_class)
            if not check_data(info, table_class):
                insert_to_db(info, table_class)
                print(f'Company inserted to database: {info['Name']}')
            else:
                print(f'Record already exist: {info['Name']}')
        return tablename
    except Exception as e:
        print(e)


def save_as_file(tablename):
    save_file = input("Do You want to save the result as a file? (y/n): ").lower()

    if save_file == 'y':
        args = {}
        filename = input('Input filename (optional): ') or None
        sheet_title = input('Input sheet title (optional): ') or 'Scraping result'
        sheet_desc = input('Input sheet description (optional): ') or None
        if filename:
            args['filename'] = filename
        if sheet_title:
            args['sheet_title'] = sheet_title
        if sheet_desc:
            args['sheet_desc'] = sheet_desc
        args['db_table'] = tablename

        db_to_file(**args)

    else:
        print('Program closed')


if __name__ == "__main__":
    table_name = main()
    save_as_file(table_name)

