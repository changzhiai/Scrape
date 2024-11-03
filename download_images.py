# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 09:53:35 2024

@author: chang
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import requests,os,logging


def download_images(file_path=None, sheet_name=None):
    """Read excel table"""
    folder = sheet_name
    os.makedirs(folder, exist_ok=True)
    logging.basicConfig(
        filename=f'{folder}/{folder}.log',
        filemode='a', 
        format='%(asctime)s - %(levelname)s - %(message)s',  
        level=logging.INFO
    )
    options = Options()
    options.add_argument('--headless')  # Example option
    driver = webdriver.Chrome(options=options)
    source = 'https://www.gbif.org/occurrence'
    driver.get(source)

    df = pd.read_excel(file_path, sheet_name)
    page_urls = df['ich']
    
    logging.info(f'Total entries: {len(page_urls)}')
    data = {}
    
    for i, page_url in page_urls.items():
        logging.info(f'Downloading: {i}, url: {page_url}')
        current_url = f'{source}/{page_url}'
        driver.execute_script(f"window.location.href='{current_url}' ")

        header_div = WebDriverWait(driver, 5).until( \
            EC.presence_of_element_located((By.XPATH, \
            "//div[@class='term-block__header' and h4[text()='Location']]")))
        table_div = header_div.find_element(By.XPATH, ".//following-sibling::div")
        table = table_div.find_element(By.XPATH, ".//table")
        latitude_row = table.find_element(By.XPATH, ".//tr[td[contains(text(), 'Decimal latitude')]]")
        latitude_cells = latitude_row.find_elements(By.XPATH, ".//td")
        if latitude_cells:
            latitude = latitude_cells[1].text 
        longitude_row = table.find_element(By.XPATH, ".//tr[td[contains(text(), 'Decimal longitude')]]")
        longitude_cells = longitude_row.find_elements(By.XPATH, ".//td")
        if longitude_cells:
            longitude = longitude_cells[1].text 
        image = driver.find_element(By.XPATH, \
            "//div[@class='card-figure']/figure/a/img")
        img_url = image.get_attribute("src")
        name = img_url.split('/')[-1]
        
        data[f'{i}_{name}'] = {
            'latitude': latitude,
            'longitude': longitude,
            'img_url': img_url,
            'current_url': current_url}
        
        response = requests.get(img_url)
        name = img_url.split('/')[-1]
        if response.status_code == 200:
            with open(f"{folder}/{name}.jpg", "wb") as file:
                file.write(response.content)
            logging.info(f"Downloaded image {i} - {name} successfully.")
            print(f"Downloaded image {i} - {name} successfully.")
        else:
            logging.info(f"Failed to download image {i} - {name}")

    
if __name__ == '__main__':
    download_images(file_path='results.xlsx', sheet_name='Michigan')