import os
import wget
import json
import time
import wget
from utils import *
from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
import requests


def download_pbf(url, file_path):
    """
    下载PBF文件并保存到本地。

    参数:
    - url: PBF文件的URL。
    - file_path: 保存文件的本地路径。
    """
    # 发起GET请求下载文件
    wget.download(url, out=file_path)


def format_pbf_url(x, y, z):
    url_template = "https://www.infrapedia.com/map/cables/{}/{}/{}.pbf"
    return url_template.format(x, y, z)


def get_all_pbf():
    path = './data/data_' + get_formatted_date()
    create_path_if_not_exists(os.path.join(path, 'pbf'))
    for zoom in range(2, 3):
        for x in range(0, 4):
            for y in range(0, 3):
                try:
                    print('Downloading {}-{}-{}.pbf'.format(zoom, x, y))
                    download_pbf(format_pbf_url(zoom, x, y), os.path.join(path, 'pbf', '{}-{}-{}.pbf'.format(zoom, x, y)))
                except Exception as e:
                    print('Fail downloading {}-{}-{}.pbf'.format(zoom, x, y), e)
                    continue


if __name__=='__main__':
    get_all_pbf()
