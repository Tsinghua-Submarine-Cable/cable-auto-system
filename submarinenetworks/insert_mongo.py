import json
import pymongo
import csv
from utils import *

def insert_mongo():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    my_db = myclient["submainenetworks_data_" + formatted_date]
    my_col = my_db["landing_point"]
    my_col.delete_many({})

    path = os.path.join('data', 'data_' + formatted_date, 'ai_output_station')
    all_dir = find_all_dir(path)

    for dir_name in all_dir:
        all_subdir = find_all_dir(os.path.join(path, dir_name))
        for j in range(len(all_subdir)):
            subdir_name = all_subdir[j]
            all_file = find_all_file(os.path.join(path, dir_name, subdir_name))
            for file_name in all_file:
                f = open(os.path.join(path, dir_name, subdir_name, file_name), 'r', encoding='UTF-8')
                data = f.read()
                f.close()
                data = json.loads(data)
                my_col.insert_one(data)

if __name__=="__main__":
    insert_mongo()
