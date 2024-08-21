from protobuf_inspector.types import StandardParser
import csv
import json
import re
import os
import requests
import time
from utils import *
from tqdm import tqdm

name_map = dict()

def load_name_map():
    global name_map  # 将infra上的海缆名映射到标准名
    open_file = open('./auxiliary_data/more_standard_infra.csv', 'r', encoding='utf-8')
    reader = csv.reader(open_file)
    for row in reader:
         name_map[row[1]] = row[0]
    open_file.close()


def get_by_api():
    path = './data/data_' + formatted_date
    create_path_if_not_exists(os.path.join(path, 'cable'))
    while True:
        crawled_set = set()
        cable_info_path = os.path.join(path, 'cable_info.json')
        cable_csv_path = os.path.join(path, 'cable_info.csv')
        no_data_cable_path = os.path.join(path, 'no_info_cable_info.json')

        if os.path.exists(cable_info_path):
            f = open(cable_info_path, 'r', encoding='utf-8')
            for line in f.readlines():
                crawled_set.add(json.loads(line)['_id'].rstrip('\n'))
        if os.path.exists(no_data_cable_path):
            f_nodata = open(no_data_cable_path, 'r', encoding='utf-8')
            for line in f_nodata.readlines():
                crawled_set.add(line.rstrip('\n'))

        print('crawled: ', len(crawled_set))

        parser = StandardParser()

        ids = set()
        filenames = os.listdir(os.path.join(path, 'pbf'))

        for filename in filenames:
            with open(os.path.join(path, 'pbf', filename), 'rb') as fh:
                output = parser.parse_message(fh, "message")
                output = output.split('\n')
                for index, row in enumerate(output):
                    search_object = re.search('[a-z0-9]{24}', row)
                    if search_object != None and search_object.group() not in ids and search_object.group() not in crawled_set:
                        ids.add(search_object.group())

        print('To crawl cable number: ', len(ids))
        if len(ids) == 0:
            break

        url = "https://www.infrapedia.com/api/cables/view/"
        url_origanization = "https://www.infrapedia.com/api/organization/view/"

        f = open(cable_info_path, 'a', encoding='utf-8')
        f_nodata = open(no_data_cable_path, 'a', encoding='utf-8')

        for id in tqdm(ids):
            if id in crawled_set:
                continue
            try:
                response = requests.get(url + id, timeout=5)
                if response.status_code == 200:
                    if len(response.json()['data']['r']) == 0:
                        f_nodata.write(id + '\n')
                        continue
                    print(response.json())
                    f.write(json.dumps(response.json()['data']['r'][0]) + '\n')
                    tmp_f = open(os.path.join(path, 'cable', response.json()['data']['r'][0]['name'] + '.json'), 'w', encoding='utf-8')
                    tmp_f.write(json.dumps(response.json()['data']['r'][0]))
                    tmp_f.close()
                else:
                    print("请求失败，状态码为：", response.status_code, "id: ", id)
            except Exception as e:
                print("请求失败 ", e)
                continue
        f.close()

    load_name_map()

    f = open(cable_info_path, 'r', encoding='utf-8')
    os.remove(cable_csv_path)
    header = ['telegeography_name', 'name', 'status', 'length', 'rfs', 'design_capacity', 'fiber_pairs',
              'lit_capacity', 'landing_points', 'facilities', 'owners', 'known_users', 'url']
    dump_file(header, cable_csv_path)
    for line in f.readlines():
        obj = json.loads(line)
        _id = obj['_id']
        if obj['terrestrial']:
            continue
        infra_name = obj['name']
        standard_name = ''
        if infra_name in name_map:
            standard_name = name_map[infra_name]
        status = obj['category']
        length = obj['systemLength']
        rfs = obj['RFS']

        design_capacity = obj['capacityTBPS']
        fiber_pairs = obj['fiberPairs']
        lit_capacity = json.dumps(obj['litCapacity'])
        cls = []
        for t in obj['cls']:
            cls.append(t['name'])
        cls = json.dumps(cls)
        facilities = []
        for t in obj['facilities']:
            facilities.append(t['name'])
        facilities = json.dumps(facilities)
        owners = []
        for t in obj['owners']:
            owners.append(t['name'])
        owners = json.dumps(owners)
        known_users = []
        for t in obj['knownUsers']:
            known_users.append(t['name'])
        known_users = json.dumps(known_users)
        more_information = json.dumps(obj['urls'])
        row = [standard_name, infra_name, status, length, rfs, design_capacity, fiber_pairs, lit_capacity, cls,
               facilities, owners, known_users, more_information]
        print(row)
        dump_file(row, cable_csv_path)

if __name__ == '__main__':
    get_by_api()
