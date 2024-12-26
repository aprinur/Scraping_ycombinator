import time
from util import insert_to_db, db_to_file, check_data, user_input
from db_config import session
from selenium import webdriver
from db_config.db_format import Format_SQL
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
driver = webdriver.Chrome()


def scrape_company_info(url: str):
    driver.get(url)
    table = driver.find_element(By.CLASS_NAME, 'space-y-3')
    name = table.find_element(By.TAG_NAME, 'h1').text
    batch = table.find_element(By.CLASS_NAME, 'flex').find_element(By.TAG_NAME, 'span').text
    elements = table.find_element(By.CSS_SELECTOR, 'div.align-center').find_elements(By.TAG_NAME, 'a')
    sector = ', '.join(element.text for element in elements if 'industry' in element.get_attribute('href'))
    texts = driver.find_elements(By.CSS_SELECTOR, r'.relative.isolate.z-0.border-retro-sectionBorder.sm\:pr-\[13px\].ycdcPlus\:pr-0.pt-1.sm\:pt-2.lg\:pt-3.pb-1.sm\:pb-2.lg\:pb-3')
    company_desc = texts[0].text
    founding_date = driver.find_element(By.XPATH, "//span[text()='Founded:']/following-sibling::span").text
    location = driver.find_element(By.XPATH, "//span[text()='Location:']/following-sibling::span").text

    if driver.find_element(By.CSS_SELECTOR, r'.flex.flex-row.items-center.gap-x-3'):
        founders = '| '.join(i.find_element(By.CLASS_NAME, 'font-bold').text.strip() for i in
                             driver.find_elements(By.CLASS_NAME, 'flex flex-row items-center gap-x-3'))
        print(founders)
    elif driver.find_element(By.CSS_SELECTOR, r'.flex.flex-row.flex-col.items-start.gap-3.md\:flex-row'):
        founders = '| '.join(i.find_element(By.CLASS_NAME, 'font-bold').text for i in driver.find_elements(By.CLASS_NAME, 'flex flex-row flex-col items-start gap-3 md:flex-row'))
        print(founders)
    else:
        founders = None
    company_url = driver.find_element(By.CSS_SELECTOR, r'.mb-2.whitespace-nowrap.md\:mb-0').get_attribute('href')
    region = ' '.join(element.text for element in elements if 'location' in element.get_attribute('href'))
    source_url = driver.current_url
    incubator = driver.find_element(By.CSS_SELECTOR, r'.mt-8.text-base.md\:order-1.md\:mt-0').text.removeprefix(
        '© 2024 ')

    return Format_SQL(
        Name=name,
        Batch=batch,
        Sector=sector,
        Region=region,
        Company_Desc=company_desc,
        Founding_Date=founding_date,
        Founders=founders,
        Incubator=incubator,
        Location=location,
        Source_Url=source_url,
        Company_Url=company_url

    )


def scrape_company_url(url, scrape_count: int = None) -> list:
    driver.get(url)
    actions = ActionChains(driver)
    company_urls = []
    previous_count = 0
    while True:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, '_company_1pgsr_355')))
        elements = driver.find_elements(By.CLASS_NAME, '_company_1pgsr_355')
        for element in elements:
            if scrape_count is None or len(company_urls) < scrape_count:
                url = element.get_attribute('href')
                if url not in company_urls:
                    company_urls.append(url)

            if scrape_count is not None and len(company_urls) == scrape_count:
                return company_urls

        current_count = len(elements)
        if current_count == previous_count:
            break
        previous_count = current_count

        try:
            last_element = elements[-1]
            actions.move_to_element(last_element).perform()
            time.sleep(3)
        except IndexError:
            print('Out of element')
            break

    return company_urls


def main():
    to_db = []
    choice = user_input()
    if choice is False:
        print('Exiting the program')
        return

    count, url = choice
    try:
        company_urls = scrape_company_url(url, scrape_count=count)
        for company_url in company_urls:
            info = scrape_company_info(company_url)
            to_db.append(info)
            if not check_data(info):
                insert_to_db(info)
                print(f'Company inserted to database: {info.Name}')
            else:
                print(f'Record already exist: {info.Name}')

        save_file = input(" Do You want to save the result as a fiel? (y/n): ").lower()
        if save_file == 'y':
            args = {}
            filename = input('Input filename (optional): ') or None
            sheet_title = input('Input sheet title (optional): ') or None
            sheet_desc = input('Input sheet description (optional): ') or None
            if filename:
                args['filename'] = filename
            if sheet_title:
                args['sheet_title'] = sheet_title
            if sheet_desc:
                args['sheet_desc'] = sheet_desc

            db_to_file(**args)

        else:
            print('Program closed')

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
    # scrape_company_info('https://www.ycombinator.com/companies')
# sample url: 'https://www.ycombinator.com/companies?batch=F24&batch=S24&batch=W24&batch=S23&batch=W23'

"""
Next feature:
1. add multiple table so user can choose which table to save as external file
2.  
"""
