import csv
import json
import re
import os
import requests
import time
from datetime import datetime
from config import *
from utils import *
def get_telegeography_by_api():
    proxies = {
        'http': 'http://127.0.0.1:10809',
        'https': 'https://127.0.0.1:10809'
    }

    urls = ['https://www.submarinecablemap.com/api/v3/cable/cable-geo.json',
                'https://www.submarinecablemap.com/api/v3/cable/all.json',
                'https://www.submarinecablemap.com/api/v3/search.json',
                'https://www.submarinecablemap.com/api/v3/config.json',
                'https://www.submarinecablemap.com/api/v3/landing-point/landing-point-geo.json',
                ]

    today = datetime.today()
    today_str = today.strftime('%Y-%m-%d')
    path = './data/data_' + today.strftime('%Y-%m-%d') + '/v3'
    create_path_if_not_exists(path)
    create_path_if_not_exists(os.path.join(path, 'cable'))
    create_path_if_not_exists(os.path.join(path, 'landing-point'))
    create_path_if_not_exists(os.path.join(path, 'ready-for-service'))
    create_path_if_not_exists(os.path.join(path, 'country'))
    create_path_if_not_exists(os.path.join(path, 'supplier'))
    create_path_if_not_exists(os.path.join(path, 'status'))


    for url in urls:
        try:
            response = requests.get(url)
            filename = url.split('/v3/')[-1]
            f = open(os.path.join(path, filename), 'w', encoding='UTF-8')
            if response.status_code == 200:
                print(response.json())
                f.write(json.dumps(response.json()) + '\n')
            else:
                print("请求失败，状态码为：", response.status_code, "id: ", id)
            f.close()
        except Exception as e:
            continue

    for country in country_list:
        url = 'https://www.submarinecablemap.com/api/v3/country/' + country
        try:
            response = requests.get(url)
            filename = url.split('/v3/')[-1]
            f = open(os.path.join(path, filename), 'w', encoding='UTF-8')
            if response.status_code == 200:
                print(response.json())
                f.write(json.dumps(response.json()) + '\n')
            else:
                print("请求失败，状态码为：", response.status_code, "id: ", id)
            f.close()
        except Exception as e:
            continue

    for supplier in supplier_list:
        url = 'https://www.submarinecablemap.com/api/v3/supplier/' + supplier
        try:
            response = requests.get(url)
            filename = url.split('/v3/')[-1]
            f = open(os.path.join(path, filename), 'w', encoding='UTF-8')
            if response.status_code == 200:
                print(response.json())
                f.write(json.dumps(response.json()) + '\n')
            else:
                print("请求失败，状态码为：", response.status_code, "id: ", id)
            f.close()
        except Exception as e:
            continue


    for year in [str(i) + '.json' for i in range(1989, 2028)]:
        url = 'https://www.submarinecablemap.com/api/v3/ready-for-service/' + year
        try:
            response = requests.get(url)
            filename = url.split('/v3/')[-1]
            f = open(os.path.join(path, filename), 'w', encoding='UTF-8')
            if response.status_code == 200:
                print(response.json())
                f.write(json.dumps(response.json()) + '\n')
            else:
                print("请求失败，状态码为：", response.status_code, "id: ", id)
            f.close()
        except Exception as e:
            continue


    for status in ['in-service.json', 'planned.json']:
        url = 'https://www.submarinecablemap.com/api/v3/status/' + status
        try:
            response = requests.get(url)
            filename = url.split('/v3/')[-1]
            f = open(os.path.join(path, filename), 'w', encoding='UTF-8')
            if response.status_code == 200:
                print(response.json())
                f.write(json.dumps(response.json()) + '\n')
            else:
                print("请求失败，状态码为：", response.status_code, "id: ", id)
            f.close()
        except Exception as e:
            continue


    f = open(os.path.join(path, 'cable', 'all.json'), 'r', encoding='UTF-8')
    cable_list = json.load(f)
    for cable_dic in cable_list:
        url = 'https://www.submarinecablemap.com/api/v3/cable/' + cable_dic['id'] + '.json'
        try:
            response = requests.get(url)
            filename = url.split('/v3/')[-1]
            f = open(os.path.join(path, filename), 'w', encoding='UTF-8')
            if response.status_code == 200:
                print(response.json())
                f.write(json.dumps(response.json()) + '\n')
            else:
                print("请求失败，状态码为：", response.status_code, "id: ", id)
            f.close()
        except Exception as e:
            continue

    f = open(os.path.join(path, 'landing-point', 'landing-point-geo.json'), 'r', encoding='UTF-8')
    lp_list = json.load(f)['features']
    for lp_dic in lp_list:
        url = 'https://www.submarinecablemap.com/api/v3/landing-point/' + lp_dic['properties']['id'] + '.json'
        try:
            response = requests.get(url)
            filename = url.split('/v3/')[-1]
            f = open(os.path.join(path, filename), 'w', encoding='UTF-8')
            if response.status_code == 200:
                print(response.json())
                f.write(json.dumps(response.json()) + '\n')
            else:
                print("请求失败，状态码为：", response.status_code, "id: ", id)
            f.close()
        except Exception as e:
            continue

    years = [str(i) for i in range(1989, 2030)]
    for year in years:
        url = 'https://www.submarinecablemap.com/api/v3/ready-for-service/' + year + '.json'
        try:
            response = requests.get(url)
            filename = url.split('/v3/')[-1]
            f = open(os.path.join(path, filename), 'w', encoding='UTF-8')
            if response.status_code == 200:
                print(response.json())
                f.write(json.dumps(response.json()) + '\n')
            else:
                print("请求失败，状态码为：", response.status_code, "id: ", id)
            f.close()
        except Exception as e:
            continue


if __name__ == '__main__':
    get_telegeography_by_api()
