import os

# Differences the TDX and the GLO data to look for anomalous differences

tdxdir = '/home/nmthoma1/nobackup/TanDEMx_Tiles/1_DEM_GLO/1_TDX_EGM08_WM/'

tdxfiles = [file for file in os.listdir(tdxdir)]

glodir = '/home/nmthoma1/nobackup/TDX_GLO30/Global/DEM_TDX_12/'

outdir = '/home/nmthoma1/nobackup/TanDEMx_Tiles/1_DEM_GLO/2_TDX_GLO_diff'

shellfile = '/home/nmthoma1/nobackup/TanDEMx_Tiles/1_DEM_GLO/code/2_run_diff.sh'

rios = '/home/nmthoma1/nobackup/TanDEMx_Tiles/1_DEM_GLO/code/RIOS_diff.py'

shell = open(shellfile, 'w+')

for file in tdxfiles:
    glofile = file.replace('__04_','__10_')
    shell.write('python ' + rios + ' -i ' + os.path.join(tdxdir, file) + ' -g ' + os.path.join(glodir, glofile.replace('_EGM08_WM.tif','_GLO30.kea')) + ' -o ' + os.path.join(outdir, file.replace('.tif','_diff.tif')) + '\n\n')
    
