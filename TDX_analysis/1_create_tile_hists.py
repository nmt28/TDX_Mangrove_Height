# creates histograms for each tile with a 10cm bin
import os
import pickle
import glob
import numpy as np
from multiprocessing import pool
import multiprocessing
import fiona
from osgeo import gdal
import rsgislib
from rsgislib import imagecalc

def CreateRef(infile, ref_img, outfile):
    hist_dict = rsgislib.imagecalc.calc_histograms_for_msk_vals(infile, 1, ref_img, 1, 0.1, 60.1, 0.1, msk_vals=None)

    with open(outfile, 'wb') as out_pkl_obj:
        pickle.dump(hist_dict, out_pkl_obj, protocol=pickle.HIGHEST_PROTOCOL)

def main():

    in_dir = '/home/nmthoma1/nobackup/TanDEMx_Tiles/1_DEM_GLO/8_TDX_Cal/'

    ref_img_dir = '/home/nmthoma1/nobackup/TanDEMx_Tiles/0_EEZ/EEZ_tiles/'

    out_dir = '/home/nmthoma1/nobackup/TanDEMx_Tiles/_1_tile_hists/'

    file_names = [file for file in os.listdir(in_dir) if file.endswith('.tif')]

    infiles = [os.path.join(in_dir, file) for file in file_names]
    outfiles = [os.path.join(out_dir, file.replace('.tif','.pkl')) for file in file_names]
    ref_imgs = [os.path.join(ref_img_dir, file.replace('_EGM08_GMW314_2015_WM_hcap_cal.tif','_EEZ.kea')) for file in file_names]

    print('test suite = ', infiles[0], ref_imgs[0], outfiles[0])

    with multiprocessing.Pool(processes=20) as pool:
        pool.starmap(CreateRef, zip(infiles, ref_imgs, outfiles))


if __name__ == "__main__":
    main()

