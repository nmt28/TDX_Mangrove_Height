import rsgislib.tools.utils
import numpy
import pickle
import glob
import pprint

countries_lut_file = "/home/nmthoma1/nobackup/TanDEMx_Tiles/TDX_Mangrove/country_ids_lut.json"
countries_lut = rsgislib.tools.utils.read_json_to_dict(countries_lut_file)

countries_idxs = list(countries_lut['val'].keys())

print(countries_idxs)

countries_hists = dict()
for country_idx in countries_idxs:
    countries_hists[country_idx] = []

stats = ['min','max','median']

for stat in stats:

    tile_hist_files = glob.glob('/home/nmthoma1/nobackup/TanDEMx_Tiles/2_TopValue/*_' + stat + '.pkl')
    print(tile_hist_files)

    for tile_hist in tile_hist_files:
        hist_pklobj = pickle.load(open(tile_hist, 'rb'))
        for country_idx in hist_pklobj.keys():
            country_idx_str = str(country_idx)
            if country_idx_str in countries_idxs:
                countries_hists[country_idx_str] = numpy.append(countries_hists[country_idx_str], hist_pklobj[country_idx])
                # old
                #countries_hists[country_idx_str].append(hist_pklobj[country_idx])
            else:
                print("{} is not in countries_idxs.".format(country_idx))

    countries_hist_file = "/home/nmthoma1/nobackup/TanDEMx_Tiles/3_max_merged/country_tdx_" + stat + ".pkl"

    with open(countries_hist_file, 'wb') as out_pkl_obj:
        pickle.dump(countries_hists, out_pkl_obj, protocol=pickle.HIGHEST_PROTOCOL)


