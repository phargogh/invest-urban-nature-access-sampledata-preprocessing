# invest-urban-nature-access-sampledata-preprocessing
Sample data preprocessing scripts for the InVEST Urban Nature Access model development

The sampledata came to me with a few problems:


## Populations were all nodata where they should have been 0

To fix:

1. Create a new target float32 raster
2. Rasterize `Commune.shp` onto the new raster.  Anywhere there's geometry
   overlap, use the pixel value of 0
3. Iterblocks over the source population raster and take the max of the
   population pixels.

## Landcover raster is incomplete

To fix:

1. Create a new byte raster
2. Rasterize `Commune.shp` onto the new raster.  Anywhere there's geometry
   overlap, use a pixel value of some reasonable non-natural landcover code.
3. Iterblocks over the source greenspace raster and copy over the greespace
   pixels.
