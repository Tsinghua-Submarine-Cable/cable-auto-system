import json
import pymongo
from utils import *

def insert_mongo():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    my_db = myclient["wiki_data_" + formatted_date]
    my_col = my_db["cable"]
    my_col.delete_many({})

    path = os.path.join('data', 'data_' + formatted_date, 'ai_output_cable')
    all_file = find_all_file(path)

    for filename in all_file:
            f = open(os.path.join(path, filename), 'r', encoding='UTF-8')
            data = f.read()
            f.close()
            data = json.loads(data)
            my_col.insert_one(data)

if __name__=="__main__":
    insert_mongo()
