from utils import *
import requests
import json
from tqdm import tqdm

if __name__=='__main__':
    id_url = 'https://services8.arcgis.com/eQokUDmReWyB8og0/arcgis/rest/services/STFCableMap_WFL1/FeatureServer/1/query?f=json&maxRecordCountFactor=4&resultOffset=0&resultRecordCount=8000&where=1%3D1&orderByFields=OBJECTID&outFields=OBJECTID&outSR=102100&spatialRel=esriSpatialRelIntersects'
    cables_url = 'https://services8.arcgis.com/eQokUDmReWyB8og0/arcgis/rest/services/OnlineMapv2_1_3_WFL1_view/FeatureServer/4/query?f=json&cacheHint=true&maxRecordCountFactor=5&resultOffset=0&resultRecordCount=10000&where=1%3D1&outFields=CABLE_ID%2CCABLE_SYSTEM_NAME%2COBJECTID&outSR=102100&spatialRel=esriSpatialRelIntersects'
    detail_info = 'https://services8.arcgis.com/eQokUDmReWyB8og0/arcgis/rest/services/STFCableMap_WFL1/FeatureServer/1/query?f=json&objectIds={}&outFields=*&returnZ=true&spatialRel=esriSpatialRelIntersects'

    create_path_if_not_exists(os.path.join('./data', 'data_' + formatted_date))

    for id in tqdm(range(1, 1742)):
        try:
            response = requests.get(detail_info.format(id), timeout=5)
            if response.status_code == 200:
                print(response.json())
                with open(os.path.join('./data', 'data_' + formatted_date, '{}.json'.format(id)), 'w', encoding='utf-8') as f:
                    f.write(json.dumps(response.json(), indent=4))
            else:
                print("请求失败，状态码为：", response.status_code, "id: ", id)
        except Exception as e:
            print("请求失败 ", e)
