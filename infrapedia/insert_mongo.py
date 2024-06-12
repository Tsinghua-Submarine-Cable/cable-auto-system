import json

import pymongo
import csv
from utils import *

def insert_mongo():
    header = ["Standard_name", "Infrapedia_Name", "Status", "Length", "RFS", "EOL", "Design Capacity", "Fiber Pairs",
              "Lit Capacity", "Cls", "Facilities", "Owners", "Known Users", "More Information"]

    new_header = ["telegeography_name", "name", "status", "length", "rfs", "eol", "design_capacity", "fiber_pairs", "lit_capacity",
                  "landing_points", "facilities", "owners", "known_users", "url"]
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    my_db = myclient["infrapedia_data_" + formatted_date]
    my_col = my_db["cable"]

    my_col.delete_many({})

    fp = open(os.path.join('data_' + formatted_date, "cable_info.csv"), "r", encoding="utf-8")
    reader = csv.DictReader(fp)
    for row in reader:
        row['lit_capacity'] = json.loads(row['lit_capacity'])
        row['landing_points'] = json.loads(row['landing_points'])
        row['facilities'] = json.loads(row['facilities'])
        row['owners'] = json.loads(row['owners'])
        row['known_users'] = json.loads(row['known_users'])
        row['url'] = json.loads(row['url'])

        my_col.insert_one(row)


if __name__=="__main__":
    insert_mongo()