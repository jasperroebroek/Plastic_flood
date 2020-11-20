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

file_name = "data/Flood_defences/Flopros_shp/Simplified_states.shp"
polygons = gpd.read_file(file_name)

polygons = polygons.loc[~pd.isna(polygons.geometry), :]
results = polygons.apply(lambda x: calc_emissions(x, id_column='OBJECTID', env=env), axis=1, result_type="expand")
results.columns = ["e_" + str(x) for x in [1, 10, 20, 50, 100, 200, 500]] + ['area_1', 'area_10']
results.loc[:, 'jump'] = results.loc[:, (['e_1', 'e_10'])].apply(
        lambda x: x[1] / x[0] if x[0] != 0 else np.nan, axis=1)

merged_results = polygons.merge(results, how='left', left_index=True, right_index=True)
merged_results.to_file(f"data/plastic_mobilisation/flopros.shp")

mp.Raster.close()
