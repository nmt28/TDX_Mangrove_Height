import rsgislib
import rsgislib.imageutils
import glob
import os
import multiprocessing
from multiprocessing import pool
import fiona
import rsgislib.imagecalc

def CreateRef(infile, outfile):

    if os.path.isfile(outfile):
        pass
    else:
        # (0.98*sqrt(TDX)+0.31)^2
        rsgislib.imageutils.set_env_vars_lzw_gtiff_outs(False)
        rsgislib.imagecalc.image_math(infile, outfile, '(b1==0)?0:(sqrt(b1)*0.98+0.31)^2', 'GTiff', rsgislib.TYPE_32FLOAT)
        


def main():

    in_dir = '/home/nmthoma1/nobackup/TanDEMx_Tiles/1_DEM_GLO/6_TDX_cap/'

    out_dir = '/home/nmthoma1/nobackup/TanDEMx_Tiles/1_DEM_GLO/8_TDX_Cal/'



    file_names = [file for file in os.listdir(in_dir) if file.endswith('.tif')]
    
    infiles = [os.path.join(in_dir, file) for file in file_names]
    outfiles = [os.path.join(out_dir, file.replace('.tif','_cal.tif')) for file in file_names]
    
    print(infiles[0], outfiles[0])
    
    with multiprocessing.Pool(processes=20) as pool:
        pool.starmap(CreateRef, zip(infiles, outfiles))
        
    
if __name__ == "__main__":
    main()

