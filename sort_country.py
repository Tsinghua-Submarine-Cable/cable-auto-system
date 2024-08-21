from pymongo import MongoClient

# 连接到 MongoDB 数据库
client = MongoClient("mongodb://localhost:27017/")
db = client['splitted_data']
collection = db['2024_country']

# 使用 aggregate 方法按照 cable 长度排序
pipeline = [
    {
        "$addFields": {
            "cableLength": {
                "$size": "$cables"
            }
        }
    },
    {
        "$sort": {
            "cableLength": -1  # 1 表示升序，-1 表示降序
        }
    },
    {
        "$project": {
            "cableLength": 0  # 不返回中间字段
        }
    }
]

# 执行聚合查询
result = list(collection.aggregate(pipeline))

cnt = 0
china_cable_set = set()
china_cable_list = []
taiwan_cable_list = []
for doc in result:
    cnt += 1
    if doc['name'] == 'China':
        china_cable_list = [cable['name'] for cable in doc['cables']]
    if doc['name'] == 'Taiwan':
        taiwan_cable_list = [cable['name'] for cable in doc['cables']]
        china_cable_list.extend(taiwan_cable_list)
        china_cable_set = set(china_cable_list)
    cable_names = [cable['name'] for cable in doc['cables']]
    print(f"{cnt:<5} {doc['name']:<20} {len(doc['cables']):<15}")
    print(cable_names)

print(len(china_cable_set))
print(china_cable_set)