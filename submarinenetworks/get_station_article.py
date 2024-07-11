from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import os
import pandas as pd
from utils import *


def get_station_article():
    create_path_if_not_exists("./data/data_" + formatted_date + "/station-articles")
    # configurations of webpage, if it does not need to show
    option = webdriver.ChromeOptions()
    option.add_argument("headless")
    browser = webdriver.Chrome(options=option)

    titles, authors, dates, regions, countrys = [], [], [], [], []
    for dirpath, dirnames, filenames in os.walk(os.path.join("data", "data_" + formatted_date, "station-article-links")):
        for filename in filenames:
            df = pd.read_csv(os.path.join(dirpath, filename))
            print(filename)
            for path in df['href']:
                print(path)
                browser.get(path)
                section = browser.find_element(By.XPATH, '//*[@id="t4-main-body"]/div/div/div[1]/div[2]')
                author = browser.find_element(By.XPATH, '//*[@id="t4-main-body"]/div/div/div[1]/div[2]/div[2]/dl/dd[1]/a/span')
                date = browser.find_element(By.XPATH, '//*[@id="t4-main-body"]/div/div/div[1]/div[2]/div[2]/dl/dd[3]/time')
                route = path.split('/')
                title = route[-1]
                region = route[-3]
                country = route[-2]
                titles.append(title)
                authors.append(author.text)
                dates.append(date.text)
                regions.append(region)
                countrys.append(country)
                dirs = './data/data_' + formatted_date + '/station-articles/'+region+'/'+country+'/'
                if not os.path.exists(dirs):
                    os.makedirs(dirs)
                with open(dirs+title+'.txt', 'w', encoding='UTF-8') as file:
                    file.write(section.text)
                    file.close()
                print("done")
    dic = { 'title': titles, 'author': authors, 'date': dates,
            'region': regions, 'countrys': countrys}
    info = pd.DataFrame(dic)
    info.to_csv("./data/data_" + formatted_date + "/station-articles/article-info.csv", index=False)


if __name__=='__main__':
    get_station_article()
