import os

# Replaces teh TDX with GLO where differences are large. Also caps at 70m

tdxdir = '/home/nmthoma1/nobackup/TanDEMx_Tiles/1_DEM_GLO/1_TDX_EGM08_WM/'

tdxfiles = [file for file in os.listdir(tdxdir)]

glodir = '/home/nmthoma1/nobackup/TDX_GLO30/Global/DEM_TDX_12/'

diff_dir = '/home/nmthoma1/nobackup/TanDEMx_Tiles/1_DEM_GLO/2_TDX_GLO_diff'

outdir = '/home/nmthoma1/nobackup/TanDEMx_Tiles/1_DEM_GLO/3_TDX_GLO_merge'

shellfile = '/home/nmthoma1/nobackup/TanDEMx_Tiles/1_DEM_GLO/code/3_run_merge.sh'

rios = '/home/nmthoma1/nobackup/TanDEMx_Tiles/1_DEM_GLO/code/RIOS_merge.py'

shell = open(shellfile, 'w+')

for file in tdxfiles:
    if os.path.isfile(os.path.join(outdir, file.replace('_WM.tif','_GMW314_2015_WM.tif'))):
        pass
    else:
        glofile = file.replace('__04_','__10_').replace('_EGM08_WM.tif','_GLO30.kea')
        shell.write('python ' + rios + ' -i ' + os.path.join(tdxdir, file) + ' -g ' + os.path.join(glodir, glofile) + ' -d ' + os.path.join(diff_dir, file.replace('.tif','_diff.tif')) + ' -o ' + os.path.join(outdir, file.replace('_WM.tif','_GMW314_2015_WM.tif')) + '\n\n')
