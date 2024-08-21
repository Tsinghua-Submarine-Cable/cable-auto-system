import json
import pymongo
from conv_coordinate import convert_to_lonlat
from utils import *

def insert_mongo():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    my_db = myclient["subtel_" + formatted_date]
    my_col = my_db["data-center"]

    my_col.delete_many({})
    dir_path = os.path.join('./data', 'data_' + formatted_date, 'datacenter')
    files = find_all_file(dir_path)
    for f in files:
        with open(os.path.join(dir_path, f), 'r', encoding='utf-8') as f:
            try:
                dic = json.load(f)
                new_dic = dic['features'][0]['attributes']
                new_dic['geometry'] = dic['features'][0]['geometry']
                my_col.insert_one(new_dic)
            except Exception as e:
                print(f, e)
                continue


if __name__=="__main__":
    insert_mongo()
