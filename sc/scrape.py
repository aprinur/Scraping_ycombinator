import time
import traceback

from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from db_config import driver
from sc.util import check_data, insert_to_db


def scrape_company_info(url: str, sectors: str = None):
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,
                                                                        r'flex.flex-col.gap-8.sm\:flex-row')))

        table = driver.find_element(By.CLASS_NAME, 'space-y-3')
        company_name = table.find_element(By.CLASS_NAME, 'text-3xl.font-bold').text
        batch = table.find_element(By.CLASS_NAME, r'flex.flex-row.items-center.gap-\[6px\]').find_element(By.TAG_NAME,
                                                                                                          'span').text
        elements = table.find_element(By.CSS_SELECTOR, 'div.align-center').find_elements(By.TAG_NAME, 'a')

        if sectors is None:
            sector = ', '.join(element.text for element in elements if 'industry' in element.get_attribute('href'))
        else:
            sector = sectors

        company_desc = driver.find_element(By.CLASS_NAME, 'prose.max-w-full.whitespace-pre-line').text
        company_card = driver.find_element(By.CSS_SELECTOR, r'div[class="ycdc-card-new space-y-1.5 sm:w-[300px]"]')

        founded_element = company_card.find_elements(By.XPATH, ".//div[.//span[text()='Founded:']]/span[2]")
        founded = founded_element[0].text if founded_element else None

        location = company_card.find_elements(By.XPATH, "//div[.//span[text()='Location:']]/span[2]")
        location = location[0].text if location else None

        founder_box = driver.find_element(By.CLASS_NAME, 'space-y-4')
        founders = []
        for content in founder_box.find_elements(By.CLASS_NAME, 'min-w-0.flex-1'):
            name = content.find_element(By.CLASS_NAME, 'text-xl.font-bold').text
            if content.find_element(By.CLASS_NAME, r'text-gray-600'):

                position = content.find_element(By.CLASS_NAME, r'text-gray-600').text
            else:
                position = content.find_element(By.CSS_SELECTOR, r'pt-1.text-gray-600').text
            founders.append(f"{name} ({position if position else ''})")
        founders = ' | '.join(founders)
        company_url = driver.find_element(By.CSS_SELECTOR, r'.mb-2.whitespace-nowrap.md\:mb-0').get_attribute('href')
        region = ' '.join(element.text for element in elements if 'location' in element.get_attribute('href'))
        source_url = driver.current_url
        incubator = driver.find_element(By.CSS_SELECTOR, r'.mt-8.text-base.md\:order-1.md\:mt-0').text.removeprefix(
            '© 2025 ')

        scraped_data = {
            "Company_Name": company_name,
            "Batch": batch,
            "Sector": sector,
            "Region": region,
            "Company_Desc": company_desc,
            "Founding_Date": founded,
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
        previous_count = 0

        while scraped_url < scrape_count:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, '_company_i9oky_355')))
            elements = driver.find_elements(By.CLASS_NAME, '_company_i9oky_355')

            for index, element in enumerate(elements):
                if scraped_url >= scrape_count:
                    return None

                elements = driver.find_elements(By.CLASS_NAME, '_company_i9oky_355')
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
                    scraped_url += 1
                else:
                    print(f'Data {data["Company_Name"]} already exist')
                    scraped_url += 1

                driver.close()
                driver.switch_to.window(driver.window_handles[0])

            try:
                if scraped_url >= scrape_count:
                    return True
                last_element = elements[-1]
                actions.move_to_element(last_element).perform()
                time.sleep(1)

                new_elements = driver.find_elements(By.CLASS_NAME, '_company_i9oky_355')
                if len(new_elements) == previous_count:
                    print('No new companies found, return to main menu.')
                    return False
                previous_count = len(new_elements)
            except IndexError:
                if issued_url:
                    for url in issued_url:
                        if scraped_url >= scrape_count:
                            return True
                        data = scrape_company_info(url)
                        if not check_data(data, table_class):
                            insert_to_db(data, table_class)
                            print(f'Data inserted to database: {data["Company_Name"]}')
                            scraped_url += 1
                return True
        return True

    except TimeoutException as e:
        print(e)
        return None
    except NoSuchElementException as e:
        print(e)
        return None
    except Exception as e:
        print(f'Error while scraping {url}: {e}')
        traceback.print_exc()
        return []


def get_sector(element) -> str | None:
    """ Function to scrape sector """
    main_url = 'https://www.ycombinator.com'
    try:
        elements = element.find_elements(By.CSS_SELECTOR, '._tagLink_i9oky_1040')
        sector = ", ".join([i.text for i in elements if 'industry' in i.get_attribute('href')])
        return f'{main_url}{sector}'
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
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, '_company_i9oky_355')))
            elements = driver.find_elements(By.CSS_SELECTOR, '._company_i9oky_355')

            for index, element in enumerate(elements):
                elements = driver.find_elements(By.CSS_SELECTOR, '._company_i9oky_355')
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
                        print(f'Inserted to database: {data["Company_Name"]}')
                    else:
                        print(f'Record already exist: {data["Company_Name"]}')

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

        return None

    except Exception as e:
        print(f'Error while scraping url {url}: {e}')
        return []
