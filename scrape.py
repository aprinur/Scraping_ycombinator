import time
import traceback
from util import check_data, insert_to_db, save_as_file_confirm, user_input_and_save_db_as_file
from db_config import driver
from db_config.db_format import YCombinatorTable
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def scrape_company_info(url: str, sectors: str = None):
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                        r'.relative.isolate.z-0.border-retro-sectionBorder.sm\:pr-\[13px\].ycdcPlus\:pr-0.pt-2.sm\:pt-4.lg\:pt-6.pb-2.sm\:pb-4.lg\:pb-6')))

        table = driver.find_element(By.CLASS_NAME, 'space-y-3')
        name = table.find_element(By.TAG_NAME, 'h1').text
        batch = table.find_element(By.CLASS_NAME, 'flex').find_element(By.TAG_NAME, 'span').text
        elements = table.find_element(By.CSS_SELECTOR, 'div.align-center').find_elements(By.TAG_NAME, 'a')

        if sectors is None:
            sector = ', '.join(element.text for element in elements if 'industry' in element.get_attribute('href'))
        else:
            sector = sectors

        texts = driver.find_elements(By.CSS_SELECTOR,
                                     r'.relative.isolate.z-0.border-retro-sectionBorder.sm\:pr-\[13px\].ycdcPlus\:pr-0.pt-1.sm\:pt-2.lg\:pt-3.pb-1.sm\:pb-2.lg\:pb-3')
        company_desc = texts[0].text
        founding_date = driver.find_element(By.XPATH, "//span[text()='Founded:']/following-sibling::span").text
        location = driver.find_element(By.XPATH, "//span[text()='Location:']/following-sibling::span").text

        if driver.find_element(By.CSS_SELECTOR, r'.flex.flex-row.items-center.gap-x-3'):
            founders = '| '.join(i.find_element(By.CLASS_NAME, 'font-bold').text.strip() for i in
                                 driver.find_elements(By.CSS_SELECTOR, r'.flex.flex-row.items-center.gap-x-3'))
        elif driver.find_element(By.CSS_SELECTOR, r'.flex.flex-row.flex-col.items-start.gap-3.md\:flex-row'):
            founders = '| '.join(i.find_element(By.CLASS_NAME, 'font-bold').text for i in
                                 driver.find_elements(By.CSS_SELECTOR,
                                                      r'.flex.flex-row.flex-col.items-start.gap-3.md\:flex-row'))
        else:
            founders = None
        company_url = driver.find_element(By.CSS_SELECTOR, r'.mb-2.whitespace-nowrap.md\:mb-0').get_attribute('href')
        region = ' '.join(element.text for element in elements if 'location' in element.get_attribute('href'))
        source_url = driver.current_url
        incubator = driver.find_element(By.CSS_SELECTOR, r'.mt-8.text-base.md\:order-1.md\:mt-0').text.removeprefix(
            '© 2024 ')

        scraped_data = {
            "Name": name,
            "Batch": batch,
            "Sector": sector,
            "Region": region,
            "Company_Desc": company_desc,
            "Founding_Date": founding_date,
            "Founders": founders,
            "Incubator": incubator,
            "Location": location,
            "Source_Url": source_url,
            "Company_Url": company_url,
        }
        return scraped_data

    except TimeoutException:
        print('Timeout waiting for page to load')
        return False
    except NoSuchElementException as e:
        print(f'Scraping issue in {e}')
        return False


def scrape_with_count(url, table_class, scrape_count: int = None):
    issued_url = set()
    proceed_url = set()
    scraped_url = 0
    try:
        driver.get(url)
        actions = ActionChains(driver)

        while scraped_url < scrape_count:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, '_company_1pgsr_355')))
            elements = driver.find_elements(By.CLASS_NAME, '_company_1pgsr_355')

            for index, element in enumerate(elements):
                if scraped_url >= scrape_count:
                    return

                elements = driver.find_elements(By.CLASS_NAME, '_company_1pgsr_355')
                element = elements[index]

                url = element.get_attribute('href')
                sector = get_sector(element)

                if url in proceed_url:
                    continue

                proceed_url.add(url)

                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[-1])
                driver.get(url)

                data = scrape_company_info(url, sector)
                if not data:
                    issued_url.add(url)
                    continue

                if not check_data(data, table_class):
                    insert_to_db(data, table_class)
                    print(f'Data added to table: {data["Name"]}')
                    scraped_url += 1
                else:
                    print(f'Data {data["Name"]} already exist')
                    scraped_url += 1

                driver.close()
                driver.switch_to.window(driver.window_handles[0])

            try:
                if scraped_url >= scrape_count:
                    return
                last_element = elements[-1]
                actions.move_to_element(last_element).perform()
                time.sleep(1)
            except IndexError:
                if issued_url:
                    for url in issued_url:
                        if scraped_url >= scrape_count:
                            return
                        data = scrape_company_info(url)
                        if not check_data(data, table_class):
                            insert_to_db(data, table_class)
                            print(f'Data inserted to database: {data["Name"]}')
                            scraped_url += 1
                return

    except TimeoutException as e:
        print(e)
    except NoSuchElementException as e:
        print(e)
    except Exception as e:
        print(f'Error while scraping url {url}: {e}')
        traceback.print_exc()
        return []


def get_sector(element) -> object:
    """ Function to scrape sector """
    try:
        elements = element.find_elements(By.CSS_SELECTOR, '._tagLink_1pgsr_1040')
        sector = ", ".join([i.text for i in elements if 'industry' in i.get_attribute('href')])
        return sector
    except NoSuchElementException:
        return None


def scrape_without_count(url, table_class):
    issued_url = []
    proceed_url = set()
    retry_count = 0
    max_retries = 5

    try:
        driver.get(url)
        actions = ActionChains(driver)
        previous_count = 0

        while retry_count < max_retries:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, '_company_1pgsr_355')))
            elements = driver.find_elements(By.CSS_SELECTOR, '._company_1pgsr_355')

            for index, element in enumerate(elements):
                elements = driver.find_elements(By.CSS_SELECTOR, '._company_1pgsr_355')
                element = elements[index]

                url = element.get_attribute('href')
                sector = get_sector(element)

                if url in proceed_url:
                    continue

                proceed_url.add(url)

                driver.execute_script("window.open('');")
                driver.switch_to.window(driver.window_handles[-1])
                driver.get(url)

                data = scrape_company_info(url, sector)
                if data:
                    if not check_data(data, table_class):
                        insert_to_db(data, table_class)
                        print(f'Inserted to database: {data["Name"]}')
                    else:
                        print(f'Record already exist: {data["Name"]}')

                else:
                    issued_url.append(url)

                driver.close()
                driver.switch_to.window(driver.window_handles[0])

            current_count = len(elements)
            if current_count == previous_count:
                retry_count += 1
            else:
                retry_count = 0

            if retry_count == max_retries:
                print('No new elements')
                break

            previous_count = current_count

            try:
                last_element = elements[-1]
                actions.move_to_element(last_element).perform()
                time.sleep(3)
            except IndexError:
                if issued_url is not None:
                    for url in issued_url:
                        data = scrape_company_info(url)
                        if not data:
                            print(f'Scraping issue in {url}')
                            continue
                        if not check_data(data, table_class):
                            insert_to_db(data, table_class)

                print('Out of element')
                break

    except Exception as e:
        print(f'Error while scraping url {url}: {e}')
        return []
