import time
from util import insert_to_db, db_to_file, check_data, session
from selenium import webdriver
from db_config.db_format import Format_SQL
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()


def scrape_company_info(url: str):
    driver.get(url)
    table = driver.find_element(By.CLASS_NAME, 'space-y-3')
    name = table.find_element(By.TAG_NAME, 'h1').text
    batch = table.find_element(By.CLASS_NAME, 'flex').find_element(By.TAG_NAME, 'span').text
    elements = table.find_element(By.CSS_SELECTOR, 'div.align-center').find_elements(By.TAG_NAME, 'a')
    sector = ', '.join(element.text for element in elements if 'industry' in element.get_attribute('href'))
    texts = driver.find_elements(By.CSS_SELECTOR,
                                 r'.relative.isolate.z-0.border-retro-sectionBorder.sm\:pr-\[13px\].ycdcPlus\:pr-0.pt-1.sm\:pt-2.lg\:pt-3.pb-1.sm\:pb-2.lg\:pb-3')
    company_desc = texts[0].text
    founding_date = driver.find_element(By.XPATH, "//span[text()='Founded:']/following-sibling::span").text
    location = driver.find_element(By.XPATH, "//span[text()='Location:']/following-sibling::span").text
    founders = '| '.join(i.text.strip().replace('\n', ' ') for i in
                         driver.find_element(By.CLASS_NAME, 'space-y-5').find_elements(By.CSS_SELECTOR, '.flex-grow'))
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
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, '_company_86jzd_338')))
        elements = driver.find_elements(By.CLASS_NAME, '_company_86jzd_338')
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


def main(url):
    to_db = []
    to_file = []
    while True:
        count = input('How much companies you want to scrape ? [ empty = all]: ')
        if count == '':
            count = None
            break
        elif count.isdigit():
            count = int(count)
            break
        else:
            print('Input only numbers')
    while True:
        file = input('Save to xlsx and csv? y/n: ')
        if file.lower() in ['y', 'n']:
            break
        else:
            print('Choose only y/n')
    company_urls = scrape_company_url(url, scrape_count=count)
    print(len(company_urls))
    for company_url in company_urls:
        info = scrape_company_info(company_url)
        to_db.append(info)
        to_file.append(info)
        if not check_data(info):
            insert_to_db(info)
            print(f'Company inserted to database: {info.Name}')
        else:
            print(f'Record already exist: {info.Name}')

    if file == 'y':
        filename = input('Input filename: ')
        db_to_file(to_file, filename)
        print(f'Result saved as {filename}')
    else:
        print('Result saved to database')


if __name__ == "__main__":
    # main('https://www.ycombinator.com/companies?batch=F24&batch=S24&batch=W24&batch=S23&batch=W23')
    # scrape_company_info('https://www.ycombinator.com/companies/archilabs')
    db_to_file(db_table='Company_in_ycombinator', filename='ycombinator company scraping result',
               sheet_title='Scraping ycombinator',
               sheet_desc='This file contain 200 companies from batch W23, S23, S24, F24, W24 in ycombinator.com')
