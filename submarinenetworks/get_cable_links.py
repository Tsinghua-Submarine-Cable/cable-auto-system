from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
from utils import *


def get_cable_links():
    create_path_if_not_exists(os.path.join('data_' + formatted_date))
    url = "https://www.submarinenetworks.com/en/systems/"

    regions = ['trans-pacific', 'trans-atlantic', 'intra-asia',
               'intra-europe', 'asia-europe-africa', 'australia-usa',
               'asia-australia', 'eurasia-terrestrial', 'brazil-us',
               'brazil-africa', 'euro-africa']

    option = webdriver.ChromeOptions()
    option.add_argument("headless")
    browser = webdriver.Chrome(options=option)

    res = []

    for region in regions:
        print(region)
        path = url+region+'/'
        browser.get(path)
        time.sleep(10)
        headers = browser.find_elements(By.TAG_NAME, 'h3')
        print('cable numbers: ', len(headers))
        for header in headers:
            if header.get_attribute('class') == 'page-header item-title':
                a = header.find_element(By.TAG_NAME, 'a')
                res.append({
                    'cable_name': a.text,
                    'href': a.get_attribute('href')
                })
    with open(os.path.join('data_' + formatted_date, 'cable_links.json'), 'w') as f:
        data_str = json.dumps(res)
        f.write(data_str)
        f.close()


if __name__ == '__main__':
    get_cable_links()
