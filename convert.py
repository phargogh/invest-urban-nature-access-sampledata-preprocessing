import logging
import os

import pygeoprocessing
import numpy
from osgeo import gdal

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)


def convert(base_dir, out_dir):
    commune_vector = os.path.join(base_dir, 'Commune.shp')
    greenspace_raster_path = os.path.join(base_dir, 'Greenspace.tif')
    population_raster = os.path.join(base_dir, 'population.tif')

    for raster_path in (greenspace_raster_path, population_raster):
        target_raster_path = os.path.join(
            out_dir, os.path.basename(raster_path).lower())
        LOGGER.info(f'Starting {raster_path} --> {target_raster_path}')
        raster_info = pygeoprocessing.get_raster_info(raster_path)
        nodata = raster_info['nodata'][0]
        pygeoprocessing.new_raster_from_base(
            base_path=raster_path,
            target_path=target_raster_path,
            datatype=raster_info['datatype'],
            band_nodata_list=[nodata],
            fill_value_list=[nodata])

        pygeoprocessing.rasterize(
            vector_path=commune_vector,
            target_raster_path=target_raster_path,
            burn_values=[0])

        source_raster = gdal.OpenEx(raster_path, gdal.GA_Update)
        source_band = source_raster.GetRasterBand(1)
        target_raster = gdal.OpenEx(target_raster_path, gdal.GA_Update)
        target_band = target_raster.GetRasterBand(1)
        for block_data in pygeoprocessing.iterblocks(
                (target_raster_path, 1), offset_only=True):
            source_array = (source_band.ReadAsArray(**block_data))
            target_array = (target_band.ReadAsArray(**block_data))

            valid_pixels = ~numpy.isclose(source_array, nodata)

            target_array[valid_pixels] = numpy.maximum(
                source_array[valid_pixels],
                target_array[valid_pixels])

            target_band.WriteArray(
                target_array,
                xoff=block_data['xoff'],
                yoff=block_data['yoff'])


if __name__ == '__main__':
    convert('invest-una-sampledata/', 'out-data')
