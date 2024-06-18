from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import os
import pandas as pd


def get_station_article():
    # configurations of webpage, if it does not need to show
    option = webdriver.ChromeOptions()
    option.add_argument("headless")
    browser = webdriver.Chrome(options=option)

    titles, authors, dates, regions, cables = [], [], [], [], []
    for dirpath, dirnames, filenames in os.walk("./data/station-article-links/"):
        for filename in filenames:
            df = pd.read_csv(os.path.join(dirpath, filename))
            print(filename)
            for path in df['href']:
                print(path)
                browser.get(path)
                section = browser.find_element(By.XPATH, '//article/section')
                author = browser.find_element(By.XPATH, "//article/aside/dl//dd[@data-original-title='Written by ']")
                date = browser.find_element(By.XPATH, "//article/aside/dl//dd[@data-original-title='Published: ']")
                route = path.split('/')
                title = route[-1]
                region = route[-3]
                cable = route[-2]
                titles.append(title)
                authors.append(author.text)
                dates.append(date.text)
                regions.append(region)
                cables.append(cable)
                dirs = "./data/station-articles/"+region+'/'+cable+'/'
                if not os.path.exists(dirs):
                    os.makedirs(dirs)
                with open(dirs+title+'.txt', 'w', encoding='UTF-8') as file:
                    file.close()
                print("done")
    dic = { 'title': titles, 'author': authors, 'date': dates,
            'region': regions, 'cable-system': cables}
    info = pd.DataFrame(dic)
    info.to_csv("./data/station-articles/article-info.csv", index=False)


if __name__=='__main__':
    get_station_article()
