import os.path
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
from utils import *

def get_station_links():
    url = r'https://www.submarinenetworks.com/en/stations/'
    # I already get every region by hand
    regions = ['africa', 'asia', 'europe',
               'north-america', 'south-america', 'oceania',
               ]


    option = webdriver.ChromeOptions()
    option.add_argument("headless")
    browser = webdriver.Chrome(options=option)
    res = []

    for region in regions:
        print(region)
        path = url+region+'/'
        browser.get(path)
        headers = browser.find_elements(By.TAG_NAME, 'h3')
        print('country numbers: ', len(headers))
        for header in headers:
            browser.find_elements(By.XPATH, '//*[@id="adminForm"]/table/tbody')
            if header.get_attribute('class') == 'page-header item-title':
                a = header.find_element(By.TAG_NAME, 'a')
                res.append({
                    'country_name': a.text,
                    'href': a.get_attribute('href')
                })
    with open(os.path.join('data', 'data_' + formatted_date, 'station-of-country-links.json'), 'w') as f:
        data_str = json.dumps(res, indent=4, sort_keys=True)
        f.write(data_str)
        f.close()

if __name__=='__main__':
    get_station_links()
