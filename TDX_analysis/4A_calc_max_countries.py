import numpy
import pickle
import math
import rsgislib.tools.utils
import rsgislib.vectorattrs
import osgeo.ogr as ogr
import pandas as pd
import glob

out_json_files = glob.glob("/home/nmthoma1/nobackup/TanDEMx_Tiles/4_max_countries/*.json")


out_data = pd.DataFrame({})

for file in out_json_files:
    num = file.split('/')[-1].split('_')[2][3:]

    out_json = rsgislib.tools.utils.read_json_to_dict(file)

    countries_lut = "/home/nmthoma1/nobackup/TanDEMx_Tiles/TDX_Mangrove/country_ids_lut.json"
    countries_json = rsgislib.tools.utils.read_json_to_dict(countries_lut)['val']

    countries = []
    values = []

    for id in out_json:
        values.append(out_json[id])
        countries.append(countries_json[id])
    
    out_data['Top' + str(num) + 'Max'] = values
    out_data['countries_' + str(num)] = countries


print(out_data)
print('writing csv')
out_data.to_csv("/home/nmthoma1/nobackup/TanDEMx_Tiles/4_max_countries/country_tdx_top2000_med.csv")

