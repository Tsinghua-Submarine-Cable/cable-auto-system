import json

from utils import *
import mapbox_vector_tile
import re
from conv_coordinate import vector_tile_coord_to_lonlat

id_set = set()

def map_coordinates(coords, map_func):
    """
    递归地对嵌套坐标列表应用映射函数
    """
    if isinstance(coords[0], list):
        return [map_coordinates(sublist, map_func) for sublist in coords]
    else:
        return map_func(coords)
def extract_numbers_regex(filename):
    # 使用正则表达式
    match = re.match(r'(\d+)-(\d+)-(\d+)', filename)
    if match:
        return tuple(map(int, match.groups()))
    return None

# 如果您有本地PBF文件
def parse_local_pbf(file_path):
    file_name = os.path.basename(file_path)
    zoom, tile_x, tile_y = extract_numbers_regex(file_name)
    extent = 4096
    with open(file_path, 'rb') as f:
        data = f.read()

    tile = mapbox_vector_tile.decode(data)

    # 解析逻辑与上面相同
    for layer_name, layer_data in tile.items():
        print(f"Layer: {layer_name}")

        # 遍历图层中的每个要素
        for feature in layer_data['features']:
            if feature['id'] in id_set:
                continue
            feature_type = feature['type']
            geometry = feature['geometry']
            properties = feature.get('properties', {})
            geometry['coordinates'] = map_coordinates(geometry['coordinates'], lambda coord: vector_tile_coord_to_lonlat(coord, zoom, tile_x, tile_y))

            f = open(
                os.path.join('./data', 'data_' + formatted_date, 'decoded_pbf', str(feature['id']) + '.json'), 'w', encoding='utf-8')
            id_set.add(feature['id'])
            json.dump(feature, f, indent=4)
            print(f"  Feature Type: {feature_type}")
            print(f"  Properties: {properties}")
            print(f"  Geometry: {geometry}")
            print("---")

def decode_pbf():
    dir_path = os.path.join('./data', 'data_' + formatted_date)
    create_path_if_not_exists(os.path.join(dir_path, 'decoded_pbf'))

    pbf_files = find_all_file(os.path.join(dir_path, 'pbf'))
    id_set = set()
    for pbf in pbf_files:
        pbf_path = os.path.join(dir_path, 'pbf', pbf)
        print(pbf_path)
        parse_local_pbf(pbf_path)

if __name__=='__main__':
    decode_pbf()
