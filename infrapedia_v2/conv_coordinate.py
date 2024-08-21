import math


def vector_tile_coord_to_lonlat(coord, zoom, tile_x, tile_y, extent=4096):
    # 将切片内坐标转换为[0,1]范围
    x = coord[0] / extent
    y = coord[1] / extent

    # 计算整个世界范围内的坐标
    x = (tile_x + x) / (2 ** zoom)
    y = (tile_y + y) / (2 ** zoom)

    # 转换为经纬度
    lon = x * 360 - 180
    lat = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y))))

    return [lon, lat]

if __name__=='__main__':
    zoom = 2  # 假设的缩放级别
    tile_x = 0  # 假设的切片X索引
    tile_y = 0  # 假设的切片Y索引
    extent = 4096  # 从数据中获取的extent值
    tile_size = 256  # 实际的切片像素尺寸

    coordinates = [[635, 4176], [655, 4163], [737, 4143], [792, 4141],
                   [527, 4176], [524, 4096], [522, 4040], [542, 3918],
                   [593, 3856], [634, 3856], [664, 3875]]

    for x, y in coordinates:
        lon, lat = vector_tile_coord_to_lonlat(x, y, zoom, tile_x, tile_y, extent, tile_size)
        print(f"Tile Coordinate ({x}, {y}) -> Lon/Lat: ({lon:.6f}, {lat:.6f})")
