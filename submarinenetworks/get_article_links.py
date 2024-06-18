# -*- coding: utf-8 -*-
# @Author: Yang Li
# @Date:   2023-09-17 00:15:56
# @Last Modified by:   Yang Li
# @Last Modified time: 2023-09-17 00:35:17
import json
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


def get_article_links():
    # configurations of webpage, if it does not need to show
    option = webdriver.ChromeOptions()
    option.add_argument("headless")
    browser = webdriver.Chrome(options=option)

    # links of all cable systems are in cable-links.json
    data = json.load(open('./data/cable_links.json', 'r'))

    for cable in data:
        # open the page
        print('done')
        cable_name = cable['cable_name'].replace('/', '-')
        print(cable['cable_name'], end=' ')
        url = cable['href']
        browser.get(url)
        number = browser.find_element(By.ID, 'limit')
        select = Select(number)
        select.select_by_value("0")
        time.sleep(2)
        title = []
        link = []
        while 1:
            print(browser.current_url, end=' ')
            try:
                tables = browser.find_elements(By.TAG_NAME, 'table')
                table = None
                for item in tables:
                    if item.get_attribute('class') == 'category table table-striped table-bordered table-hover':
                        table = item
                        break
                    else:
                        continue
                # now we find the table
                tbody = table.find_element(By.TAG_NAME, 'tbody')
                trs = tbody.find_elements(By.TAG_NAME, 'tr')
                for tr in trs:
                    td = tr.find_element(By.TAG_NAME, 'td')
                    a = td.find_element(By.TAG_NAME, 'a')
                    title.append(a.text)
                    link.append(a.get_attribute('href'))
                # now we get all atricle links
                # now try to save them as csv files according to their categories

                # if pagination do not exist
                try:
                    lis = browser.find_elements(By.XPATH,
                        "//form[@id='adminForm']//div[@class='pagination']//ul[@class='pagination']/li")
                    nxt = lis[-2]
                    a = nxt.find_element(By.TAG_NAME, 'a')
                    browser.get(a.get_attribute('href'))
                    time.sleep(2)
                except:
                    break
            except:
                print('no data', end=' ')
                break
        df = pd.DataFrame({'title': title, 'href': link})
        # print(df.head())
        df.to_csv(cable_name + '.csv', mode='w', index=False)


if __name__ == '__main__':
    get_article_links()
