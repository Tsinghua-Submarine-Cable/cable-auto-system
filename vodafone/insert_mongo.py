import json
import pymongo
import csv
from utils import *

def insert_mongo():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    my_db = myclient["vodafone_data_" + formatted_date]
    my_col = my_db["cable"]

    my_col.delete_many({})

    path = os.path.join('data', 'data_' + formatted_date)

    all_dir = ['cable', 'country', 'landing-point', 'ready-for-service', 'status', 'supplier']
    ignore = ['all.json', 'cable-geo.json', 'search.json', 'slider.json', 'landing-point-geo.json']

    for dir in all_dir:
        all_file = find_all_file(os.path.join(path, dir))
        mycol = my_db[dir]
        mycol.delete_many({})
        for file in all_file:
            try:
                if file in ignore or file[-4:] != 'json':
                    continue
                f = open(os.path.join(path, dir, file), 'r', encoding='utf-8')
                dic = json.load(f)
                mycol.insert_one(dic)
                f.close()
            except Exception as e:
                continue

    mycol = my_db['all']
    mycol.delete_many({})
    file = 'all.json'
    f = open(os.path.join(path, 'cable', file), 'r', encoding='utf-8')
    li = json.load(f)
    for dic in li:
        mycol.insert_one(dic)
    f.close()

    mycol = my_db['cable-geo']
    mycol.delete_many({})
    file = 'cable-geo.json'
    f = open(os.path.join(path, 'cable', file), 'r', encoding='utf-8')
    dic = json.load(f)
    for d in dic['features']:
        del d['type']
        d['properties']['id'] = d['properties']['slug']
        del d['properties']['slug']
        mycol.insert_one(d)
    f.close()

    mycol = my_db['landing-point-geo']
    mycol.delete_many({})
    file = 'landing-point-geo.json'
    f = open(os.path.join(path, 'landing-point', file), 'r', encoding='utf-8')
    dic = json.load(f)
    for d in dic['features']:
        del d['type']
        mycol.insert_one(d)
    f.close()

    mycol = my_db['terrestrial-geo']
    mycol.delete_many({})
    file = 'terrestrial-geo.json'
    f = open(os.path.join(path, 'terrestrial', file), 'r', encoding='utf-8')
    dic = json.load(f)
    for d in dic['features']:
        del d['type']
        mycol.insert_one(d)


if __name__=="__main__":
    insert_mongo()
