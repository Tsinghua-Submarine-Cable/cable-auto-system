import geopandas as gpd
import json
import utils


def export_lines_to_json(input_features, output_json_file):
    """
    使用GeoPandas从shapefile导出线要素为GeoJSON格式，坐标使用经纬度

    :param input_features: 输入线要素的路径（shapefile）
    :param output_json_file: 输出JSON文件的路径
    """
    try:
        # 读取shapefile
        gdf = gpd.read_file(input_features)

        # 检查是否为线要素
        if not all(gdf.geometry.type.isin(['LineString', 'MultiLineString'])):
            raise ValueError(f"输入要素 {input_features} 不全是线要素")

        # 确保坐标系统是WGS 84 (EPSG:4326)
        gdf = gdf.to_crs(epsg=4326)

        # 转换为GeoJSON格式
        geojson = json.loads(gdf.to_json())

        result = geojson["features"][0]
        result["geometry"]["type"] = "MultiLineString"
        coordinates = []
        shape_len = 0
        for feature in geojson["features"]:
            coordinates.append(feature["geometry"]["coordinates"])
            shape_len += feature["properties"]["Shape_Leng"]
        result["geometry"]["coordinates"] = coordinates
        result["properties"]["Shape_Leng"] = shape_len
        result["id"] = input_features.split('/')[-1][:-4]

        geojson["features"] = [result]

        # 写入JSON文件
        with open(output_json_file, 'w', encoding='utf-8') as f:
            json.dump(geojson, f, ensure_ascii=False, indent=2)

        print(f"线要素已成功导出为GeoJSON: {output_json_file}")

    except Exception as e:
        print(f"发生错误: {str(e)}")

# 使用示例
if __name__ == "__main__":
    names = [
        "china_kazakhstan",
        "china_kyrgyzstan",
        "china_laos_thailand",
        "china_mainland",
        "china_myanmar_bangladesh_india",
        "china_nepal",
        "china_pakistan",
        "china_tajikistan",
        "cr2",
        "cr3",
        "silk_road_north_line",
        "silk_road_south_line",
        "super_tsr",
        "tea_2",
        "tea_4",
        "tmp",
        "transit_silk_road",
        "tsr2",
        "tsr_plus"
    ]

    for name in names:
        shapefile_path = r"./gis/{}/{}.shp".format(name, name)
        output_file = r"./gis/geojson/{}.json".format(name)

        export_lines_to_json(shapefile_path, output_file)
