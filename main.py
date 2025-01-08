import traceback
import keyword
from util import insert_to_db, check_data, user_input_scraping, user_input_and_save_db_as_file
from scrape import scrape_company_info, scrape_company_url


def scrape():
    try:
        count, url, table_class = user_input_scraping()
        company_urls = scrape_company_url(url, scrape_count=count)

        for company_url in company_urls:
            result = scrape_company_info(company_url)
            if not result:
                print(f'Scraping issue in {company_url}')
                continue
            if not check_data(result, table_class):
                insert_to_db(result, table_class)
                print(f'Company inserted to database: {result["Name"]}')
            else:
                print(f'Record already exist: {result["Name"]}')

        save_file = input("Do You want to save the result as a file? (y/n): ").lower()
        if save_file == 'y':
            user_input_to_save_db_as_file(tablename)
        else:
            print('Program closed')
            return
    except Exception as e:
        print(e)
        traceback.print_exc()
        return


def main_menu():
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
            scrape()

        elif user_option == '2':
            user_input_and_save_db_as_file()

        elif user_option == '3':
            print('Closing program')
            return

        else:
            print('Out of option')


if __name__ == "__main__":
    main_menu()
