import geopandas as gpd
import geomappy as mp
import numpy as np
import pandas as pd
from functions import calc_emissions


M_extent_1 = mp.Raster("data/River_network/global_chans_30arcs.tif")
M_water_bodies = mp.Raster("data/reprojected/water_bodies.tif")
M_extent_10 = mp.Raster("data/reprojected/extent_10.tif")
M_extent_20 = mp.Raster("data/reprojected/extent_20.tif")
M_extent_50 = mp.Raster("data/reprojected/extent_50.tif")
M_extent_100 = mp.Raster("data/reprojected/extent_100.tif")
M_extent_200 = mp.Raster("data/reprojected/extent_200.tif")
M_extent_500 = mp.Raster("data/reprojected/extent_500.tif")
M_mpw = mp.Raster("data/reprojected/mpw.tif")

env = {"M_extent_1": M_extent_1,
       "M_extent_10": M_extent_10,
       "M_extent_20": M_extent_20,
       "M_extent_50": M_extent_50,
       "M_extent_100": M_extent_100,
       "M_extent_200": M_extent_200,
       "M_extent_500": M_extent_500,
       "M_water_bodies": M_water_bodies,
       "M_mpw": M_mpw}

continents = ['eu', 'as', 'af', 'au', 'ca', 'na', 'sa']
for continent in continents:
    print(continent)
    print("-----------------------------------------------")
    file_name = f"data/Hydrosheds_basins/{continent}_bas_30s_beta/{continent}_bas_30s_beta.shp"
    basins_shp = gpd.read_file(file_name)

    selected_basins = basins_shp.loc[basins_shp.AREA_SQKM > 5000, :]
    results = selected_basins.apply(lambda x: calc_emissions(x, id_column='BASIN_ID', env=env), axis=1, result_type="expand")
    results.columns = ["e_" + str(x) for x in [1, 10, 20, 50, 100, 200, 500]] + ['area_1', 'area_10']
    results.loc[:, 'jump'] = results.loc[:, (['e_1', 'e_10'])].apply(
            lambda x: x[1] / x[0] if x[0] != 0 else np.nan, axis=1)

    merged_results = basins_shp.merge(results, how='left', left_index=True, right_index=True)
    merged_results.to_file(f"data/plastic_mobilisation/basins/plastic_mobilisation_{continent}.shp")

mp.Raster.close()
print()

continents = ['ca', 'eu', 'as', 'af', 'au', 'na', 'sa']
for continent in continents:
    print(continent)
    file_name = f"data/plastic_mobilisation/basins/plastic_mobilisation_{continent}.shp"
    if continent == "ca":
        basins_shp = gpd.read_file(file_name)
    else:
        basins_shp = basins_shp.append(gpd.read_file(file_name))
basins_shp.to_file("data/plastic_mobilisation/basins.shp")
