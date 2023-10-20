import rsgislib
import rsgislib.imageutils
import rsgislib.vectorutils
import rsgislib.vectorutils.createrasters
import rsgislib.imagecalc
import rsgislib.tools.geometrytools
import glob
import os
from multiprocessing import pool
import multiprocessing
import fiona

def CreateRef(infile, outfile):

    if os.path.isfile(outfile):
        pass
    else:
        rsgislib.imagecalc.image_math(infile, outfile, '(b1==0)?0:1.020 * sqrt(b1) + 0.33', 'KEA', rsgislib.TYPE_32FLOAT)

        rsgislib.imageutils.pop_img_stats(outfile, use_no_data=True, no_data_val=0, calc_pyramids=True)



def main():

    in_dir = '/home/nmthoma1/nobackup/TanDEMx_Tiles/1_DEM_GLO/3_TDX_GLO_merge/'

    out_dir = '/home/nmthoma1/nobackup/TanDEMx_Tiles/ApplyEquation/'



    file_names = [file for file in os.listdir(in_dir) if file.endswith('.tif')]
    
    infiles = [os.path.join(in_dir, file) for file in file_names]
    outfiles = [os.path.join(out_dir, file.replace('.tif','_maxHeight.kea')) for file in file_names]
   
    
    with multiprocessing.Pool(processes=20) as pool:
        pool.starmap(CreateRef, zip(infiles, outfiles))
    
if __name__ == "__main__":
    main()

