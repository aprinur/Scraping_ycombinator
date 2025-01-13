import traceback
import keyword
from db_config import driver
from util import user_input_scraping, user_input_and_save_db_as_file, save_as_file_confirm
from scrape import scrape_with_count, scrape_without_count


def scrape():
    try:
        count, url, table_class, tablename = user_input_scraping()
        if count is not None:
            scrape_with_count(url, table_class=table_class, scrape_count=count)
            if save_as_file_confirm():
                user_input_and_save_db_as_file(tablename)
                return
        else:
            scrape_without_count(url, table_class)
            if save_as_file_confirm():
                user_input_and_save_db_as_file(tablename)
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
