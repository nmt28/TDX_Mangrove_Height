# script deals witht eh 259 tall tiles only. remaining are oved ovet in script 7
import os
import geopandas as gpd
import subprocess
# Replaces teh TDX with GLO where differences are large. Also caps at 70m

tdxdir = '/home/nmthoma1/nobackup/TanDEMx_Tiles/1_DEM_GLO/3_TDX_GLO_merge/'

outdir = '/home/nmthoma1/nobackup/TanDEMx_Tiles/1_DEM_GLO/6_TDX_cap/'

shellfile = '/home/nmthoma1/nobackup/TanDEMx_Tiles/1_DEM_GLO/code/6_run_new_max.sh'

rios = '/home/nmthoma1/nobackup/TanDEMx_Tiles/1_DEM_GLO/code/RIOS_tiles_newmax.py'

shell = open(shellfile, 'w+')


GPKG_file = '/home/nmthoma1/nobackup/TDX_scratch/find_tall_tiles/tall_tiles.gpkg'

tiles = gpd.read_file(GPKG_file)

threshold = 31.02

subset_tiles = tiles[tiles['Perc99']<threshold]

print(len(tiles))
print(len(subset_tiles))


for filepath in tiles['filepaths']:
    if filepath in subset_tiles['filepaths'].values:
        print('found file')
        
        name = filepath.split('/')[-1]
        perc99_val = subset_tiles[subset_tiles['filepaths']==filepath].iloc[0]['Perc99']
        
        shell.write('python ' + rios + ' -i ' + os.path.join(filepath) + ' -o ' + os.path.join(outdir, name.replace('.tif','_hcap.tif')) + ' -v ' + str(perc99_val) + '\n')
    else:
        name = filepath.split('/')[-1]
        subprocess.call('cp ' + filepath + ' ' + os.path.join(outdir,name.replace('.tif','_hcap.tif')),shell=True)
        
        
