from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pymongo
import uvicorn
from utils import *

app = FastAPI()

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:60817"],  # 允许的源，这里假设你的 React 应用运行在 localhost:3000
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
my_db = myclient["vodafone_data_" + formatted_date]
my_col = my_db["terrestrial-geo"]

gis_db = myclient["gis"]
gis_col = gis_db["terrestrial-geo"]

cable_db = myclient["telegeography_data_2024-07-10"]
cable_geo_col = cable_db["cable-geo"]
cable_col = cable_db["cable"]
lp_col = cable_db["landing-point"]
lp_geo_col = cable_db["landing-point-geo"]
country_col = cable_db["country"]
supplier_col = cable_db["supplier"]

subtel_db = myclient["subtel_data_2024-08-21"]
dc_geo_col = subtel_db["data-center-geo"]

@app.get("/api/terrestrial/geo")
async def get_coordinates():
    geo_infos = gis_col.find({})
    coordinates = []
    for dic in geo_infos:
        coordinates.append(dic['geometry']['coordinates'])
    return {"coordinates": coordinates}

@app.get("/api/submarine/geo")
async def get_coordinates():
    geo_infos = cable_geo_col.find({})
    coordinates = []
    for dic in geo_infos:
        coordinates.append(dic['geometry']['coordinates'])
    return {"coordinates": coordinates}

@app.get("/api/cables")
async def get_cables_info():
    cables = cable_col.find({})
    cable_infos = []
    for dic in cables:
        del dic['_id']
        cable_infos.append(dic)
    return cable_infos

@app.get("/api/landing_points")
async def get_landing_points_info():
    lps = lp_col.find({})
    lp_infos = []
    for dic in lps:
        del dic['_id']
        lp_infos.append(dic)
    return lp_infos

@app.get("/api/landing_points/geo")
async def get_coordinates():
    geo_infos = lp_geo_col.find({})
    coordinates = []
    for dic in geo_infos:
        point = {
          'coordinates': [dic['geometry']['coordinates'][0], dic['geometry']['coordinates'][1]],
          'name': dic['properties']['name'],
          'color': "#FF5733",
          'label': dic['properties']['name']
        }
        coordinates.append(point)
    return {"points": coordinates}

@app.get("/api/data_centers")
async def get_landing_points_info():
    lps = lp_col.find({})
    lp_infos = []
    for dic in lps:
        del dic['_id']
        lp_infos.append(dic)
    return lp_infos

@app.get("/api/data_centers/geo")
async def get_coordinates():
    geo_infos = lp_geo_col.find({})
    coordinates = []
    for dic in geo_infos:
        point = {
          'coordinates': [dic['geometry']['coordinates'][0], dic['geometry']['coordinates'][1]],
          'name': dic['properties']['name'],
          'color': "#FF5733",
          'label': dic['properties']['name']
        }
        coordinates.append(point)
    return {"points": coordinates}

@app.get("/api/countries")
async def get_countries_info():
    countries = country_col.find({})
    c_infos = []
    for dic in countries:
        del dic['_id']
        c_infos.append(dic)
    return c_infos

@app.get("/api/suppliers")
async def get_suppliers_info():
    suppliers = supplier_col.find({})
    s_infos = []
    for dic in suppliers:
        del dic['_id']
        s_infos.append(dic)
    return s_infos


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
