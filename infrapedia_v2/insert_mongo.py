import json
import pymongo
import csv
from utils import *

def insert_mongo():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    my_db = myclient["infrapedia_v2_data_" + formatted_date]
    my_col = my_db["cable"]

    my_col.delete_many({})
    dir_path = os.path.join('./data', 'data_' + formatted_date, 'decoded_pbf')
    files = find_all_file(dir_path)
    for f in files:
        with open(os.path.join(dir_path, f), 'r', encoding='utf-8') as f:
            try:
                dic = json.load(f)
                my_col.insert_one(dic)
            except Exception as e:
                print(f, e)
                continue


if __name__=="__main__":
    insert_mongo()
