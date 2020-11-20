from geomappy.utils import reproject_map_like
from rasterio.warp import Resampling

template = "data/River_network/global_chans_30arcs.tif"

water_bodies = "data/Flood_extents/floodMapGL_permWB/floodMapGL_permWB.tif"
mpw = "data/Mismanaged_plastic_waste/LebretonAndrady2019_MismanagedPlasticWaste.tif"
extent_10 = "data/Flood_extents/floodMapGL_rp10y/floodMapGL_rp10y.tif"
extent_20 = "data/Flood_extents/floodMapGL_rp20y/floodMapGL_rp20y.tif"
extent_50 = "data/Flood_extents/floodMapGL_rp50y/floodMapGL_rp50y.tif"
extent_100 = "data/Flood_extents/floodMapGL_rp100y/floodMapGL_rp100y.tif"
extent_200 = "data/Flood_extents/floodMapGL_rp200y/floodMapGL_rp200y.tif"
extent_500 = "data/Flood_extents/floodMapGL_rp500y/floodMapGL_rp500y.tif"

reproject_map_like(water_bodies, template, "data/reprojected/water_bodies.tif", resampling=Resampling.nearest)
reproject_map_like(mpw, template, "data/reprojected/mpw.tif", resampling=Resampling.nearest)
reproject_map_like(extent_10, template, "data/reprojected/extent_10.tif", resampling=Resampling.nearest)
reproject_map_like(extent_20, template, "data/reprojected/extent_20.tif", resampling=Resampling.nearest)
reproject_map_like(extent_50, template, "data/reprojected/extent_50.tif", resampling=Resampling.nearest)
reproject_map_like(extent_100, template, "data/reprojected/extent_100.tif", resampling=Resampling.nearest)
reproject_map_like(extent_200, template, "data/reprojected/extent_200.tif", resampling=Resampling.nearest)
reproject_map_like(extent_500, template, "data/reprojected/extent_500.tif", resampling=Resampling.nearest)
