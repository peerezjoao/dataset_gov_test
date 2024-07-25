# imports functions
from src.python.utils import init_settings
from src.python.pages import app_data_gov as app
from python.pages import analitycs
import os

def main():

    # config functions
    init_settings.load_environ()
    download_dir = init_settings.set_download_dir()
    driver = init_settings.config_driver(download_dir)

    # open application
    app.open_site(driver)
    datasets_string = os.getenv('DATASETS')
    dataset_list = datasets_string.split('|')

    # # download datasets
    for dataset in dataset_list:
        app.search_dateset(driver, dataset)
        app.download_dataset(driver,download_dir ,dataset)

    # cross datasets
    files = os.listdir(download_dir)
    path_1 = os.path.join(download_dir, files[1])
    path_2 = os.path.join(download_dir, files[0])

    analitycs.cross_datasets(download_dir, path_1, path_2)
 

if __name__ == '__main__':
    main()