from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from db_config import driver


def scrape_company_info(url: str, sectors: str = None):
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, r'flex.flex-col.gap-8.sm\:flex-row')))

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

        location = company_card.find_element(By.XPATH, "//div[.//span[text()='Location:']]/span[2]")

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


scrape_company_info('https://www.ycombinator.com/companies/matterport')
# scrape_company_info('https://www.ycombinator.com/companies/doordash')
