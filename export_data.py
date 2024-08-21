import pymongo
import json
from bson import ObjectId
import os


def export_data_from_mongodb():
    # MongoDB连接信息
    mongo_uri = "mongodb://localhost:27017/"
    database_name = "filled_data"

    # 输出目录
    output_dir = "filled_data"


    # 自定义JSON编码器,处理ObjectId
    class JSONEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, ObjectId):
                return str(o)
            return json.JSONEncoder.default(self, o)


    # 连接到MongoDB
    client = pymongo.MongoClient(mongo_uri)
    db = client[database_name]

    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 获取数据库中的所有集合
    collections = db.list_collection_names()

    for collection_name in collections:
        collection = db[collection_name]

        # 查询所有文档
        documents = list(collection.find())

        # 为每个集合创建一个JSON文件
        output_file = os.path.join(output_dir, f"{collection_name}.json")

        # 将文档写入JSON文件
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(documents, f, ensure_ascii=False, indent=4, cls=JSONEncoder)

        print(f"集合 {collection_name} 的数据已成功导出到 {output_file}")

    # 关闭MongoDB连接
    client.close()

    print(f"所有集合的数据已成功导出到 {output_dir} 目录")


if __name__ == '__main__':
    export_data_from_mongodb()
