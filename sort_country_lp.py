from pymongo import MongoClient

# 连接到 MongoDB 数据库
client = MongoClient("mongodb://localhost:27017/")
db = client['splitted_data']
collection = db['2024_landing-point']


# 使用 aggregate 方法按照 country 分组并排序
pipeline = [
    {
        "$group": {
            "_id": "$country",
            "count": {"$sum": 1},
            "landing_points": {"$push": "$$ROOT"}
        }
    },
    {
        "$sort": {
            "count": -1  # -1 表示降序排序
        }
    }
]

# 执行聚合查询
result = list(collection.aggregate(pipeline))

china_lp_set = set()
china_lp_list = []
taiwan_lp_list = []
print(f"{'rank':<5} {'country':<20} {'count':<5}")
cnt = 0
for doc in result:
    cnt += 1
    if doc['_id'] == 'China':
        china_lp_list = [lp['name'] for lp in doc['landing_points']]
    if doc['_id'] == 'Taiwan':
        taiwan_lp_list = [lp['name'] for lp in doc['landing_points']]
        china_lp_list.extend(taiwan_lp_list)
        china_lp_set = set(china_lp_list)
    print(f"{cnt:<5} {doc['_id']:<20} {doc['count']:<5}")
    lp_names = [lp['name'] for lp in doc['landing_points']]
    print(lp_names)
print(len(china_lp_set))
print(china_lp_list)
