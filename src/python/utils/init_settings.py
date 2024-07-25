# import libs
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import os
import shutil
import logging
from dotenv import load_dotenv

def load_environ():

    # load environment variables
    try: 
        dotenv_path = os.path.join(os.getcwd(), '.env')
        if os.path.exists(dotenv_path):
            print(f'File exists.')
        load_dotenv(dotenv_path)

    except FileNotFoundError as not_file:
        print(f'Environment file not found {not_file}')


def set_download_dir():
    # set default download path --- add path in environment variables
    download_dir = os.path.join(os.getcwd(),'src/python/resources/')
    if os.path.exists(download_dir):
        shutil.rmtree(download_dir)
        os.makedirs(download_dir, exist_ok=True)
    return download_dir

def config_driver(download_dir):

    # first configuration
    webdriver_service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    prefs = {"download.default_directory": download_dir}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(service=webdriver_service , options=options)

    return driver

def setup_log():

    # create three folder logs --- implement logic later
    list_log = [
        'logs/info', 'logs/error', 'logs/debug'
    ]

    for l in list_log:
        current_path = os.path.join(os.getcwd(),l)
        if not os.path.exists(current_path):
            os.makedirs(current_path)
