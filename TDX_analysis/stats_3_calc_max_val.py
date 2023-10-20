import numpy
import pickle
import math
import rsgislib.tools.utils
import rsgislib.vectorattrs
import osgeo.ogr as ogr
import numpy as np

stats = ['min', 'max', 'median']

for stat in stats:
    histfile = "/home/nmthoma1/nobackup/TanDEMx_Tiles/3_max_merged/country_tdx_" + stat + ".pkl"

    hist_pklobj = pickle.load(open(histfile, 'rb'))



    vals_max = dict()
    for country_idx in hist_pklobj.keys():
        pkl_lists = hist_pklobj[country_idx]
        if len(pkl_lists) > 0:
            sorted = np.sort(pkl_lists)[::-1]
            if stat == 'max':
                stat_val = np.max(sorted)
            elif stat == 'min':
                stat_val = np.min(sorted)
            elif stat == 'median':
                stat_val = np.median(sorted)
            vals_max[country_idx] = stat_val
        else:
            vals_max[country_idx] = 0.0
        print("\tvals_max100 val = {}".format(vals_max[country_idx]))

    out_json_file = "/home/nmthoma1/nobackup/TanDEMx_Tiles/4_max_countries/country_tdx_max.json"
    rsgislib.tools.utils.write_dict_to_json(vals_max, out_json_file)

    vec_file="/home/nmthoma1/nobackup/TanDEMx_Tiles/0_EEZ/UN_GPKG/GADM_EEZ_WCMC_4326_UnqID_clean.gpkg"
    vec_lyr="GADM_EEZ_WCMC_4326_UnqID_clean"

    ctry_uid = rsgislib.vectorattrs.read_vec_column(vec_file, vec_lyr, att_column="unqid")
    print(ctry_uid)

    median_2000 = numpy.zeros_like(ctry_uid, dtype=float)
    print(np.shape(ctry_uid))
    print(np.shape(median_2000))

    for i, uid in enumerate(ctry_uid):
        uid_str = f"{uid}"
        if uid_str in vals_max:
            median_2000[i] = vals_max[uid_str]


    rsgislib.vectorattrs.write_vec_column(vec_file, vec_lyr, "final_" + stat, ogr.OFTReal, median_2000.tolist())
            

