import matplotlib.pyplot as plt
import numpy as np
from rasterio.mask import mask


def draw_annotations(t, x, y, ax=None, overlapping_pixels=0, fontsize=10, **kwargs):
    if isinstance(ax, type(None)):
        ax = plt.gca()

    mask = np.zeros(ax.figure.canvas.get_width_height(), bool)
    plt.tight_layout()
    ax.figure.canvas.draw()

    va_positions = {'b': 'bottom', 't': 'top', 'c': 'center'}
    ha_positions = {'l': 'left', 'r': 'right', 'c': 'center'}

    indices = np.arange(len(t))

    for i in indices:
        for position in ['bl', 'tl', 'tr', 'br', 'cl', 'cr', 'tc', 'bc']:
            va = va_positions[position[0]]
            ha = ha_positions[position[1]]

            a = ax.text(x=x[i], y=y[i], s=t[i], ha=ha, va=va, fontsize=fontsize, **kwargs)

            bbox = a.get_window_extent()
            x0 = int(bbox.x0)+overlapping_pixels
            x1 = int(np.ceil(bbox.x1))-overlapping_pixels
            y0 = int(bbox.y0)+overlapping_pixels
            y1 = int(np.ceil(bbox.y1))-overlapping_pixels

            s = np.s_[x0:x1 + 1, y0:y1 + 1]
            if np.any(mask[s]):
                a.set_visible(False)
            else:
                mask[s] = True
                break


def calc_emissions(polygon, id_column="ID", env=None):
    """
    Returns
    -------
    e_1, e_10, e_20, e_50, e_100, e_200, e_500, area_1, area_10
    """
    id = polygon[id_column]
    polygon = [polygon.geometry]

    M_extent_1 = env['M_extent_1']
    M_extent_10 = env['M_extent_10']
    M_extent_20 = env['M_extent_20']
    M_extent_50 = env['M_extent_50']
    M_extent_100 = env['M_extent_100']
    M_extent_200 = env['M_extent_200']
    M_extent_500 = env['M_extent_500']
    M_water_bodies = env['M_water_bodies']
    M_mpw = env['M_mpw']

    try:
        extent_1 = mask(M_extent_1._file, polygon, crop=True, nodata=0)[0].squeeze().astype(np.float64)
        if extent_1.sum() == 0:
            return [np.nan] * 9
    except ValueError:
        print(f"{id}: aborted, geometry not present in the raster")
        return [np.nan] * 9

    water_bodies = mask(M_water_bodies._file, polygon, crop=True, nodata=0)[0].squeeze()
    extent_10 = mask(M_extent_10._file, polygon, crop=True, nodata=np.nan)[0].squeeze()
    extent_20 = mask(M_extent_20._file, polygon, crop=True, nodata=np.nan)[0].squeeze()
    extent_50 = mask(M_extent_50._file, polygon, crop=True, nodata=np.nan)[0].squeeze()
    extent_100 = mask(M_extent_100._file, polygon, crop=True, nodata=np.nan)[0].squeeze()
    extent_200 = mask(M_extent_200._file, polygon, crop=True, nodata=np.nan)[0].squeeze()
    extent_500 = mask(M_extent_500._file, polygon, crop=True, nodata=np.nan)[0].squeeze()
    mpw = mask(M_mpw._file, polygon, crop=True, nodata=0)[0].squeeze()

    if not all([extent.shape == mpw.shape for extent in (extent_1, extent_10, extent_20, extent_50, extent_100,
                                                         extent_200, extent_500)]):
        print(f"{id}: aborted, due to mismatch of shapes")
        return [np.nan] * 9
    else:
        print(id)

    extent_1_mask = np.logical_or(extent_1 == 1, water_bodies == 1)
    extent_10_mask = np.logical_and(~np.isnan(extent_10), ~extent_1_mask)
    extent_20_mask = np.logical_and(~np.isnan(extent_20), ~extent_1_mask)
    extent_50_mask = np.logical_and(~np.isnan(extent_50), ~extent_1_mask)
    extent_100_mask = np.logical_and(~np.isnan(extent_100), ~extent_1_mask)
    extent_200_mask = np.logical_and(~np.isnan(extent_200), ~extent_1_mask)
    extent_500_mask = np.logical_and(~np.isnan(extent_500), ~extent_1_mask)

    combined_extents = [np.full_like(extent_10_mask, 0), extent_10_mask, extent_20_mask, extent_50_mask,
                        extent_100_mask, extent_200_mask, extent_500_mask]

    return [((extent + extent_1_mask) * mpw).sum() for extent in combined_extents] + \
           [extent_1_mask.sum(), extent_10_mask.sum() + extent_1_mask.sum()]
