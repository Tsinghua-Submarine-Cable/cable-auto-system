import datetime
import json
import pymongo
import time
from utils import *

name_map = dict()
eol_map = dict()

def load_name_map():
    global name_map  # 将infra上的海缆名映射到标准名
    open_file = open('./auxiliary_data/more_standard_infra.csv', 'r', encoding='utf-8')
    reader = csv.reader(open_file)
    for row in reader:
         name_map[row[1]] = row[0]
    open_file.close()

def load_eol_map():
    global eol_map
    open_file = open('./data/data_' + formatted_date + '/id_eol.csv', 'r', encoding='utf-8')
    reader = csv.reader(open_file)
    for row in reader:
        dt = datetime.fromtimestamp(int(row[1])*100)
        eol_map[row[0]] = '{}-{}'.format(dt.year, dt.month)
    open_file.close()

def insert_mongo():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    my_db = myclient["infrapedia_data_" + formatted_date]
    my_col = my_db["cable"]

    my_col.delete_many({})

    load_name_map()
    load_eol_map()
    cable_info_path = os.path.join('./data/data_' + formatted_date, 'cable_info.json')
    f = open(cable_info_path, 'r', encoding='utf-8')

    for line in f.readlines():
        obj = json.loads(line)
        if obj['terrestrial']:
            continue

        dic = {}
        dic['_id'] = obj['_id']
        dic['name'] = obj['name']
        dic['length'] = obj['systemLength']

        dic['telegeography_name'] = ''
        if dic['name'] in name_map.keys():
            dic['telegeography_name'] = name_map[obj['name']]

        dic['design_capacity'] = obj['capacityTBPS']
        dic['lit_capacity'] = obj['litCapacity']
        dic['fiber_pairs'] = obj['fiberPairs']
        dic['status'] = obj['category']

        lpid2info = {}

        for lp_info in obj['cluster']['features']:
            lp_dic = {}
            lp_dic['name'] = lp_info['properties']['name']
            lp_dic['coordinates'] = lp_info['geometry']['coordinates']
            lpid2info[lp_info['properties']['_id']] = lp_dic

        new_lps = []
        for lp in obj['cls']:
            lp['name'] = lp['name'].replace(',  ', ', ')
            lp_dic = {
                '_id': lp['_id'],
                'name': lp['name'],
                'country': lp['name'].split(', ')[-1],
                'coordinates': lpid2info[lp['_id']]['coordinates']
            }
            new_lps.append(lp_dic)

        dic['landing_points'] = new_lps
        dic['facilities'] = obj['facilities']
        dic['owners'] = [owner['name'] for owner in obj['owners']]
        dic['known_users'] = obj['knownUsers']
        dic['eol'] = ''
        if dic['_id'] in eol_map.keys():
            dic['eol'] = eol_map[dic['_id']]
        dic['url'] = obj['urls']

        dic['update_time'] = obj['uDate']

        my_col.insert_one(dic)


if __name__=="__main__":
    insert_mongo()
