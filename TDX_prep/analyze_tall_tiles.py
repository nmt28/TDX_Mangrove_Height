import pandas as pd
import geopandas as gpd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.ndimage import gaussian_filter1d

# script that finds sensitivity of 99th percentile for all tiles with max > 50m. plots 99th perc of each tile in order, then uses polynomial to find the value at which the change in ordered 99th percentile is 0 (inflection point) - basically is the max likely to be a real value or noise value based on what the 99th percentile value is. At this value, tiles where difference between max and 99th percentile is greater than this value, 99th percentile is taken as max
def open_gpkg(file):
    data = gpd.read_file(file)
    
    print(data.head())
    
    #data.plot()
    #plt.show()
    
    return data
    
def analyze_heights_histos(gdf):
    
    fig, ax = plt.subplots()
    sns.histplot(gdf['Perc99'], ax=ax, color='orange')
    
    ax2 = ax.twinx()
    sns.histplot(gdf['maximum'], bins=10, ax=ax2)

    plt.tight_layout()
    plt.savefig('/home/nmthoma1/nobackup/TDX_scratch/find_tall_tiles/tall_tiles.png', format='PNG')

def analyze_heights_plot(gdf):
    
    
    x = np.arange(1, len(gdf) +1, 1)
    n = gdf['Perc99'].argsort()
    #names = gdf['country_names'][n]
    y = gdf.sort_values(['Perc99'])
    
    # calculate polynomial
    z = np.polyfit(x, y['Perc99'], 5)
    print(z)
    f = np.poly1d(z)
    print(f)
    
    # fit the polynominal
    x_new = np.linspace(x[0], x[-1], len(gdf))
    y_new = f(x_new)
    print(y_new)
    # finds rate of change
    diffs = [y - x for x, y in zip(y_new, y_new[1:])]
    
    # where slope (rates of change) is smallest
    infl = x[1:][diffs==np.min(diffs)]
    print(infl)
    
    # value where slope (rate of change) is smallest
    infl_val = y['Perc99'][x==infl].iloc[0]
    print(infl_val)
            
    
    plt.plot(x_new, y_new, c='blue')
    plt.scatter(x[y['Perc99']==infl_val], y['Perc99'][y['Perc99']==infl_val])
    plt.plot(x, y['Perc99'], c='orange')
    plt.xlabel('n')
    plt.ylabel('99th perc')
    #plt.legend()
    plt.savefig('/home/nmthoma1/nobackup/TDX_scratch/find_tall_tiles/tall_tiles.png', format='PNG')
    
def subset_10perc(gdf):
    
    gdf['80perc_of_max'] = gdf['maximum']*0.8
    
    sub_gdf = gdf[gdf['Perc99'] > gdf['80perc_of_max']]
    
    print(len(sub_gdf))
    
def main():
    
    file = '/home/nmthoma1/nobackup/TDX_scratch/find_tall_tiles/tall_tiles.gpkg'
    
    gdf = open_gpkg(file)
    
    #analyze_heights_histos(gdf)
    
    analyze_heights_plot(gdf)
    
    #subset_10perc(gdf)
    
if __name__ == "__main__":
    main()
