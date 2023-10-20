import os
import subprocess
import glob

# looks for erroneous values in the tdx and sets them to high values which
# will be obvious in teh differencing.

# Also does EEZ and GMW masking and conversion to EGM08

region = 'Global'

rios = '/home/nmthoma1/nobackup/TanDEMx_Tiles/1_DEM_GLO/code/RIOS_tiles.py'

in_dir = "/home/nmthoma1/nobackup/TanDEMx/12m_DEM/DEM/" + region + '/'

out_dir = "/home/nmthoma1/nobackup/TanDEMx_Tiles/1_DEM_GLO/1_TDX_EGM08_WM/"

EGM_dir = "/home/nmthoma1/nobackup/TanDEMx_Tiles/0_EGM/EGM_tiles/"

Watermask_dir = "/home/nmthoma1/nobackup/TanDEMx_Tiles/0_Watermask/watermask_tiles/"

GMW_dir = "/home/nmthoma1/nobackup/TanDEMx_Tiles/0_GMW_V3_new/GMW_tiles"

tdx_files = [file for file in os.listdir(in_dir) if file.endswith('.tif')]

print(tdx_files)

shell_file = '/home/nmthoma1/nobackup/TanDEMx_Tiles/1_DEM_GLO/code/1_run_' + region + '.sh'

shell = open(shell_file, 'w+')


for file in tdx_files:
    shell.write('python '  +  rios + ' -i ' + os.path.join(in_dir, file) + ' -g ' + os.path.join(GMW_dir, file.replace('.tif','_DEM_GMW314_2015.kea')) + ' -w ' + os.path.join(Watermask_dir, file.replace('.tif','_WM.tif')) + ' -e ' + os.path.join(EGM_dir, file.replace('.tif','_EGM08.tif')) + ' -o ' + os.path.join(out_dir, file.replace('.tif','_EGM08_WM.tif \n\n')))

