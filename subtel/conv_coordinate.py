from pyproj import Transformer

def convert_to_lonlat(x, y, from_epsg, to_epsg=4326):
    transformer = Transformer.from_crs(from_epsg, to_epsg, always_xy=True)
    lon, lat = transformer.transform(x, y)
    return lon, lat


# x = 251338.48209999874
# y = 6258525.720899999
# from_epsg = 3857  # Web墨卡托
#
# lon, lat = convert_to_lonlat(x, y, from_epsg)
# print(f"Longitude: {lon:.6f}, Latitude: {lat:.6f}")
