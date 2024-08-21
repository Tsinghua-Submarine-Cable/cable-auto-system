from pymongo import MongoClient

# 连接到 MongoDB 数据库
client = MongoClient("mongodb://localhost:27017/")
db = client['telegeography_data_2024-07-10']
collection = db['country']

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
for doc in result:
    cnt += 1
    print(f"{cnt:<5} {doc['name']:<20} {len(doc['cables']):<15}")
