# calculates 95th percentile of the histograms by country
import numpy
import pickle
import math
import rsgislib.tools.utils
import rsgislib.vectorattrs
import osgeo.ogr as ogr

histfile = "/home/nmthoma1/nobackup/TanDEMx_Tiles/_2_country_tdx_histograms/country_tdx_histograms.pkl"

hist_pklobj = pickle.load(open(histfile, 'rb'))

vals_95th = dict()
for country_idx in hist_pklobj.keys():
    print("Country {}".format(country_idx))
    n_vals = numpy.sum(hist_pklobj[country_idx])
    print("\tTotal = {}".format(n_vals))
    if n_vals > 0:
        percent_1 = n_vals/100
        percent_95 = math.floor(percent_1*99)
        print("\t95th idx = {}".format(percent_95))
        bin_sum = 0
        val = 0.0
        for bin in hist_pklobj[country_idx]:
            val = val + 0.1
            if (percent_95 > bin_sum) and (percent_95 < (bin_sum+bin)):
                break
            bin_sum = bin_sum + bin
        vals_95th[country_idx] = val
    else:
        vals_95th[country_idx] = 0.0
    print("\t95th val = {}".format(vals_95th[country_idx]))


out_json_file = "/home/nmthoma1/nobackup/TanDEMx_Tiles/_3_calc_99perc/country_tdx_95th_percentiles.json"
rsgislib.tools.utils.write_dict_to_json(vals_95th, out_json_file)

vec_file="/home/nmthoma1/nobackup/TanDEMx_Tiles/0_EEZ/UN_GPKG/GADM_EEZ_WCMC_4326_UnqID_clean.gpkg"
vec_lyr="GADM_EEZ_WCMC_4326_UnqID_clean"

ctry_uid = rsgislib.vectorattrs.read_vec_column(vec_file, vec_lyr, att_column="unqid")
percent95th_vals = numpy.zeros_like(ctry_uid, dtype=float)

for i, uid in enumerate(ctry_uid):
    uid_str = f"{uid}"
    if uid_str in vals_95th:
        percent95th_vals[i] = vals_95th[uid_str]


rsgislib.vectorattrs.write_vec_column(vec_file, vec_lyr, "percent99th", ogr.OFTReal, percent95th_vals.tolist())




