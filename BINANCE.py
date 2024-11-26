import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
import csv
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import os
import zipfile

import pandas as pd


# unzip extracted zip into destination folder
def unzip_all_zips(source_folder, destination_folder, keyword):

    # Iterate through all files in the source folder
    for filename in os.listdir(source_folder):

        # complete the file path
        filepath = os.path.join(source_folder, filename)

        # check if this is a zip file and contains keywords
        if filename.endswith('.zip') and keyword in filename:

            # if it is, unzip this zip file into destination folder
            with zipfile.ZipFile(filepath, 'r') as zip_ref:
                zip_ref.extractall(destination_folder)
            print(f"{filename} finished unzips.")

            # delete proceeded zip file
            os.remove(filepath)
        else:
            print(f"{filename} not include keywords, jump unzip.")
    print("All file with keywords finished unzip.")


# merge files of same cryptocurrency but different dates
def merge_csv_files(source_folder, destination_folder, output_filename, column_indexes):

    # List to store column data from all files
    all_column_data = []

    for filename in os.listdir(source_folder):

        # add target file paths
        filepath = os.path.join(source_folder, filename)

        # Process only CSV files
        if filename.endswith('.csv'):

            # Read the specified columns from the file without treating the first row as headers
            data = pd.read_csv(filepath, usecols=column_indexes, header=None)
            all_column_data.append(data)

    # Concatenate all the collected data into a single DataFrame
    merged_column_data = pd.concat(all_column_data, ignore_index=True)

    # Store concatenated files into csv
    os.makedirs(destination_folder, exist_ok=True)
    output_filepath = os.path.join(destination_folder, output_filename)
    merged_column_data.to_csv(output_filepath, index=False, header=False)
    print(f"Combined files have been stored to {output_filepath}")


# Get data from Binance website for future klines
def get_data(driver):

    # Navigate to the Binance vision data webpage
    driver.get('https://data.binance.vision/?prefix=data/futures/um/daily/klines/')

    # Wait for the page to load and locate the listing table
    WebDriverWait(driver, 2000).until(EC.presence_of_element_located((By.XPATH, '//*[@id="listing"]/tr')))
    sleep(1)

    # Scroll down the page to ensure all content is loaded (if applicable)
    for i in range(1):
        driver.execute_script('document.documentElement.scrollTo(0,document.body.scrollHeight)')
        sleep(0.3)

    # Get the page source and parse it with lxml
    a1 = driver.page_source
    tree = etree.HTML(a1)

    # Extract the rows in the table, skipping the header
    data_list = tree.xpath('//*[@id="listing"]/tr')[1:]

    # Loop through each entry in the main listing
    for data in data_list:
        sleep(2)

        # Extract the file name and URL
        fileName = data.xpath('.//td[1]/a/text()')[0]
        url = data.xpath('.//td[1]/a/@href')[0] + '1m/'

        # Navigate to the subfolder page
        driver.get(url)
        sleep(2)

        # Wait for the subfolder page to load
        WebDriverWait(driver, 2000).until(EC.presence_of_element_located((By.XPATH, '//*[@id="listing"]/tr')))

        # Get the subfolder page source and parse it
        a1 = driver.page_source
        tree = etree.HTML(a1)
        data_list1 = tree.xpath('//*[@id="listing"]/tr')[1:]

        # Loop through each file in the subfolder
        for data1 in data_list1:
            url = data1.xpath('.//td[1]/a/@href')[0]
            name = data1.xpath('.//td[1]/a/text()')[0]

            # Process files that are not CHECKSUM files
            if '.CHECKSUM' not in name:
                name = name.split('-1m-')[-1].split('.zip')[0]
                name = name.replace('-', '')
                name = int(name)

                # Check if the file's date falls within the specified range
                if name >= 20220201 and name <= 20220401:
                    url = data1.xpath('.//td[1]/a/@href')[0]
                    driver.get(url)
                    sleep(0.1)
        sleep(3)

        try:
            # Define source and destination folder paths for unzipping
            source_folder = r'[local-path]'
            destination_folder = r'[local-path]/{}'.format(fileName)

            # Unzip all zip files in the source folder to the destination folder
            unzip_all_zips(source_folder, destination_folder, '-')
        except:
            # Handle exceptions during unzipping
            aaaaa = 1
        try:
            # Prepare paths for merging CSV files
            fileName = fileName[:-1]
            source_folder = r'[local-path]/{}'.format(fileName)
            destination_folder = r'[local-path]/{}/{}'.format(fileName, "Combined_files")
            output_filename = '{}.csv'.format(fileName)

            # Specify the column indexes to extract, and could change to columns you want
            column_indexes = [0, 1, 2, 3, 4, 5, 6]

            # Merge the CSV files into one
            merge_csv_files(source_folder, destination_folder, output_filename, column_indexes)
        except:
            # Handle exceptions during CSV merging
            aaaaa = 0


options = Options()  # create instance
options.add_argument('--disable-blink-features=AutomationControlled')  # Implement anti-scraping measures
options.add_experimental_option('excludeSwitches', ['enable-automation']) # Hide the notification bar

driver = webdriver.Chrome(options=options)  # Define the automation object driver
get_data(driver)  # call get data function
print("Finish!!!")
