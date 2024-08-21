import json
import pymongo
import csv
from utils import *

def insert_mongo():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    my_db = myclient["gis"]
    my_col = my_db["terrestrial-geo"]

    my_col.delete_many({})

    path = os.path.join('../gis', 'geojson')

    all_files = find_all_file(path)
    for file in all_files:
        f = open(os.path.join(path, file), 'r', encoding='utf-8')
        dic = json.load(f)
        del dic['type']
        my_col.insert_one(dic['features'][0])


if __name__=="__main__":
    insert_mongo()
