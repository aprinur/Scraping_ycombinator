import traceback

from sc import user_input_scraping, scrape_with_count, save_as_file_confirm, user_input_and_save_db_as_file, \
    scrape_without_count


def execution():
    try:
        parameter = user_input_scraping()
        if not parameter:
            quit()
        count = parameter['count']
        url = parameter['url']
        table_class = parameter['new_table_class'] if 'new_table_class' in parameter.keys() else (
            parameter)['table_class']
        tablename = parameter['table_name']

        if count is not None:
            if not scrape_with_count(url, table_class=table_class, scrape_count=count):
                return
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
        quit()


def main_menu():
    while True:

        user_option = input(
            """
1. Get companies information
2. Export database into xlsx and csv file
3. Quit


Enter Option (1/2/3) : """)
        if user_option and user_option.lower() == 'quit':
            quit()

        if not user_option.isdigit():
            print('Input only number')
            continue

        if user_option == '1':
            execution()

        elif user_option == '2':
            user_input_and_save_db_as_file()

        elif user_option == '3':
            print('Closing program')
            return

        else:
            print('Out of option')


if __name__ == "__main__":
    main_menu()
