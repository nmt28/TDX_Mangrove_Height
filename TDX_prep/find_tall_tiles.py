import os
import rasterio as rio
import glob
import numpy as np
import pandas as pd
import geopandas as gpd
from pyproj import Transformer
from shapely.geometry import Polygon
from shapely.geometry import box
import subprocess
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

in_dir = '/home/nmthoma1/nobackup/TanDEMx_Tiles/1_DEM_GLO/3_TDX_GLO_merge'
#in_dir = '/home/nmthoma1/nobackup/TDX_scratch/Gabon/TDX_EGM_MANG/'

files = glob.glob(in_dir + '/*.tif')

filepaths = []
geom = []
p99 = []
p95 = []
p90 = []
maximum = []
minimum = []

for file in files:
    with rio.open(file) as f:
        xmin, ymin, xmax, ymax = f.bounds
        #transformer = Transformer.from_crs(f.crs, "EPSG:4979")
        #ul = transformer.transform(xmin,ymax)
        #lr = transformer.transform(xmax,ymin)
        #shapely box: minx, miny, maxx, maxy of S1 bounds
        poly = box(xmin,ymin,xmax,ymax)
                
        data = f.read(1)
        data = data[data!=0]
        if len(data) > 0:
            d_max = np.amax(data)
            if d_max > 50:
                filepaths.append(file)
                geom.append(poly)
                minimum.append(np.amin(data))
                maximum.append(d_max)
                p99.append(np.percentile(data, 99))
                p95.append(np.percentile(data, 95))
                p90.append(np.percentile(data, 90))
                #name = file.split('/')[-1].split('.')[0]
                #out = '/home/nmthoma1/nobackup/TDX_scratch/find_tall_tiles/plots'
                #outfile = os.path.join(out, name + '.png')
                #print(outfile)

                #n, bins, patches = plt.hist(data, 100)
                #plt.savefig(outfile, format='PNG')
                #plt.clf()

df = gpd.GeoDataFrame({'filepaths':filepaths, 'geometry':geom, 'minimum':minimum, 'maximum':maximum, 'Perc99':p99, 'Perc95':p95, 'Perc90':p90}, crs='EPSG:4979')
gdf = df.to_crs("EPSG:4326")
gdf.to_file('/home/nmthoma1/nobackup/TDX_scratch/find_tall_tiles/tall_tiles.gpkg',driver='GPKG')

