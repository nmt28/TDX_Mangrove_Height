import os
import pickle
import glob
import numpy as np
from multiprocessing import pool
import multiprocessing
import fiona
from osgeo import gdal

def CreateRef(infile, ref_img, outfile):
    # open EEZ and omit 0
    ref_ds = gdal.Open(ref_img)
    ref_arr = ref_ds.GetRasterBand(1).ReadAsArray()
    unq_vals = np.unique(ref_arr)
    unq_vals = unq_vals[unq_vals!=0]
    # open TDX
    infile_ds = gdal.Open(infile)
    infile_arr = infile_ds.GetRasterBand(1).ReadAsArray()
    
    pixel_nums = [2000]
    for num in pixel_nums:
    # create out dict
        out_dict={}

        for val in unq_vals:
            sub_arr = np.where(ref_arr==val, infile_arr, 0)
            sub_arr[np.isnan(sub_arr)]==0
            sub_arr_0 = sub_arr[sub_arr>0]
            if len(sub_arr_0) > 0:
                sub_arr_0_sort = np.sort(sub_arr_0.flatten())[::-1]
                sub_arr_0_sort_100 = sub_arr_0_sort[:num]
                out_dict[val] = sub_arr_0_sort_100
            else:
                print('empty')
                sub_arr_0_sort_100 = []
                out_dict[val] = sub_arr_0_sort_100


        with open(outfile.replace('.pkl','_' + str(num) + '.pkl'), 'wb') as out_pkl_obj:
            pickle.dump(out_dict, out_pkl_obj, protocol=pickle.HIGHEST_PROTOCOL)

def main():

    in_dir = '/home/nmthoma1/nobackup/TanDEMx_Tiles/1_DEM_GLO/3_TDX_GLO_merge/'

    ref_img_dir = '/home/nmthoma1/nobackup/TanDEMx_Tiles/0_EEZ/EEZ_tiles/'

    out_dir = '/home/nmthoma1/nobackup/TanDEMx_Tiles/2_Top2000/'

    file_names = [file for file in os.listdir(in_dir) if file.endswith('.tif')]

    infiles = [os.path.join(in_dir, file) for file in file_names]
    outfiles = [os.path.join(out_dir, file.replace('.tif','.pkl')) for file in file_names]
    ref_imgs = [os.path.join(ref_img_dir, file.replace('_EGM08_GMW314_2015_WM.tif','_EEZ.kea')) for file in file_names]

    print('test suite = ', infiles[0], ref_imgs[0], outfiles[0])

    with multiprocessing.Pool(processes=20) as pool:
        pool.starmap(CreateRef, zip(infiles, ref_imgs, outfiles))


if __name__ == "__main__":
    main()
