from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys 
import time
import os
import re

def open_site(driver):

    # max retries and timeout pages
    max_retries = 3 
    timeout_page = os.getenv('TIMEOUT_PAGE')

    # try open the application three times
    for attempt in range(max_retries):

        try:
            driver.get(os.getenv('MAIN_URL'))
            search_bar = WebDriverWait(driver, timeout_page).until(EC.visibility_of_element_located((By.XPATH, '//input[contains(@class,"search")]')))
            
            if search_bar:
                print('Page is load.')
                break

        except Exception as e:

            if attempt < max_retries - 1:
                print(f'Attempt: {attempt} of {max_retries}. Trying again...')
                time.sleep(5)

            else:
                print(f'All atempts already try.')
                driver.close()


def search_dateset(driver, dataset_name):

    timeout_page = os.getenv('TIMEOUT_PAGE')


    # try search dataset 
    try: 

        if dataset_name == 'Obesity in California, 2012 and 2013':
            driver.get(os.getenv('CA_GOV_URL'))

        search_bar = WebDriverWait(driver, timeout_page).until(EC.visibility_of_element_located((By.XPATH, '//input[@placeholder="Search datasets..."]')))
        if search_bar:
            # clear the input field and set new information
            search_bar.clear()
            search_bar.send_keys(dataset_name)
            search_bar.send_keys(Keys.ENTER)

    except Exception as e:
        print(f'Element not found. Error {str(e)}')

def download_dataset(driver, download_dir ,dataset_name):
    # download dataset to the destination repository
    timeout_page = os.getenv('TIMEOUT_PAGE')

    try:

        if dataset_name == 'National Obesity By State':
            set_local_gov = WebDriverWait(driver, timeout_page).until(EC.visibility_of_element_located((By.XPATH, '//span[contains(.,"Local Government")]')))
            if set_local_gov:
                set_local_gov.click()

        dataset_group = WebDriverWait(driver, timeout_page).until(EC.visibility_of_element_located((By.XPATH, '//ul[contains(@class,"dataset-list unstyled")]')))
        if dataset_group:
            print(f'Element found: {dataset_group}')

        dataset_cards = dataset_group.find_elements(By.CSS_SELECTOR, ".dataset-item.has-organization")

        # iterate through each card information and check the dataset names
        for index, card in enumerate(dataset_cards):
            title_dataset = card.find_element(By.CLASS_NAME, 'dataset-heading')
            print(f'Current card title {title_dataset.text} and {dataset_name}')

            pattern = re.compile(re.escape(dataset_name), re.IGNORECASE)
            match = pattern.search(title_dataset.text)

            # search dataset name with regex
            if match:
                link_dataset = title_dataset.find_element(By.TAG_NAME, 'a')
                driver.get(link_dataset.get_attribute('href'))
                break
                
        csv_format_button = WebDriverWait(driver, timeout_page).until(EC.visibility_of_element_located((By.XPATH, '//a[contains(@data-format,"csv")]')))
        csv_format_url = csv_format_button.get_attribute('href')

        try: 

            # try to download file
            driver.get(csv_format_url)
            time.sleep(5)

            files = [f for f in os.listdir(download_dir) if f.endswith('.csv')]

            if len(files) == 1:
                print(f'First file found.')
                driver.back()

            if len(files) == 2:
                if files[0] != files[1]:
                    print(f'Exists two different files in path.')  

                else:
                    print(f'Exists two equal files.')
                    raise FileExistsError('Exists two files equals.')

        except WebDriverException as wd:
            print(f'Error to access url. Error: {wd}')

        except FileExistsError as fee:
            print(fee)

    except Exception as e:
        print(f'Element not found. Error {str(e)}')

