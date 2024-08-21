import json
import requests
import time
from datetime import datetime
from utils import *


def get_vodafone_by_api():
    urls = ['https://globalnetworkmap.vodafone.com/api/cable/cable-geo.json',
            'https://globalnetworkmap.vodafone.com/api/landing-point/landing-point-geo.json',
            'https://globalnetworkmap.vodafone.com/api/pop/pop-geo.json',
            'https://globalnetworkmap.vodafone.com/api/service/services.json',
            'https://globalnetworkmap.vodafone.com/api/country/all.json',
            'https://globalnetworkmap.vodafone.com/api/satellite/satellite-geo.json',
            'https://globalnetworkmap.vodafone.com/api/terrestrial/terrestrial-geo.json',
            'https://globalnetworkmap.vodafone.com/api/service/mpls.json',
            'https://globalnetworkmap.vodafone.com/api/cable/all.json',
            'https://globalnetworkmap.vodafone.com/api/search.json',
            ]

    path = './data/data_' + formatted_date
    create_path_if_not_exists(path)
    create_path_if_not_exists(os.path.join(path, 'cable'))
    create_path_if_not_exists(os.path.join(path, 'landing-point'))
    create_path_if_not_exists(os.path.join(path, 'country'))
    create_path_if_not_exists(os.path.join(path, 'pop'))
    create_path_if_not_exists(os.path.join(path, 'service'))
    create_path_if_not_exists(os.path.join(path, 'satellite'))
    create_path_if_not_exists(os.path.join(path, 'terrestrial'))


    for url in urls:
        try:
            filename = url.split('/api/')[-1]
            response = requests.get(url, verify=False)
            f = open(os.path.join(path, filename), 'w', encoding='UTF-8')
            if response.status_code == 200:
                print(response.json())
                f.write(json.dumps(response.json()) + '\n')
            else:
                print("请求失败，状态码为：", response.status_code, "id: ", id)
            f.close()
        except Exception as e:
            continue

    country_url_base = 'https://globalnetworkmap.vodafone.com/api/country/'
    cable_url_base = 'https://globalnetworkmap.vodafone.com/api/cable/2africa.json'


if __name__ == '__main__':
    get_vodafone_by_api()
