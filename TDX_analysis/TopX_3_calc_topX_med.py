import numpy
import pickle
import math
import rsgislib.tools.utils
import rsgislib.vectorattrs
import osgeo.ogr as ogr
import numpy as np

pixel_nums = [0, 100, 200, 500, 1000, 2000]

histfile = "/home/nmthoma1/nobackup/TanDEMx_Tiles/3_top2000_merged/country_tdx_top2000.pkl"

hist_pklobj = pickle.load(open(histfile, 'rb'))


for pixel_num in pixel_nums:
    
    vals_med = dict()
    for country_idx in hist_pklobj.keys():
        pkl_lists = hist_pklobj[country_idx]
        if len(pkl_lists) > 0:
            sorted = np.sort(pkl_lists)[::-1]
            if pixel_num == 0:
                median_val = sorted[pixel_num]
            else:
                median_val = np.median(sorted[:pixel_num])
            vals_med[country_idx] = median_val
        else:
            vals_med[country_idx] = 0.0
        print("\tvals_med100 val = {}".format(vals_med[country_idx]))

    
    out_json_file = "/home/nmthoma1/nobackup/TanDEMx_Tiles/4_Top2000_merged_med/country_tdx_top" + str(pixel_num) + "_med.json"
    rsgislib.tools.utils.write_dict_to_json(vals_med, out_json_file)
    
    vec_file="/home/nmthoma1/nobackup/TanDEMx_Tiles/0_EEZ/UN_GPKG/GADM_EEZ_WCMC_4326_UnqID_clean.gpkg"
    vec_lyr="GADM_EEZ_WCMC_4326_UnqID_clean"

    ctry_uid = rsgislib.vectorattrs.read_vec_column(vec_file, vec_lyr, att_column="unqid")
    
    median_2000 = numpy.zeros_like(ctry_uid, dtype=float)
    
    for i, uid in enumerate(ctry_uid):
        uid_str = f"{uid}"
        if uid_str in vals_med:
            median_2000[i] = vals_med[uid_str]


    rsgislib.vectorattrs.write_vec_column(vec_file, vec_lyr, "med_top_" + str(pixel_num), ogr.OFTReal, median_2000.tolist())
            
