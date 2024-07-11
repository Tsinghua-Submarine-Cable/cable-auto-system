from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
import pandas as pd
from utils import *


def get_cable_introduction():
    create_path_if_not_exists(os.path.join('data_' + formatted_date, 'cable_introduction'))

    # configurations of webpage, if it does not need to show
    option = webdriver.ChromeOptions()
    option.add_argument("headless")
    browser = webdriver.Chrome(options=option)

    # links of all cable systems are in cable-links.json
    path = './data_' + formatted_date
    data = json.load(open(os.path.join(path, 'cable_links.json'), 'r'))

    for cable in data:
        try:
            # open the page
            print('done')
            cable_name = cable['cable_name'].replace('/', '-')
            print(cable['cable_name'], end=' ')
            url = cable['href']
            browser.get(url)
            cable_intro = browser.find_element(by=By.CLASS_NAME, value='content-category')
            time.sleep(2)
            title = cable_intro.find_element(by=By.TAG_NAME, value='h2').text
            content_div = cable_intro.find_element(by=By.CLASS_NAME, value='category-desc').find_elements(by=By.TAG_NAME,
                                                                                                          value='p')
            content = ''
            for p in content_div:
                content += p.text + '\n'

            dic = {'title': title, 'content': content}
            f = open(os.path.join(path, 'cable_introduction', cable_name + '.json'), 'w', encoding='UTF-8')
            f.write(json.dumps(dic) + '\n')
            f.close()
        except Exception as e:
            continue

if __name__ == '__main__':
    get_cable_introduction()
