#!/usr/bin/env python
# conda create --name geog python=2.7
# activate geog
# conda install rasterio
# conda install -c conda-forge geopandas

import os
import fnmatch
import json
import pdb

import rasterio
import numpy
import geopandas as gpd

from affine import Affine
from rasterio.features import rasterize

def zonalStats(inShp, inRaster, bandNum=1, reProj = False, minVal = '', rastType='N', verbose=False):
        outputData=[]
        with rasterio.open(inRaster, 'r') as curRaster:
            inVector = gpd.read_file(inShp)
            if inVector.crs != curRaster.crs:
                if reProj:
                    inVector = inVector.to_crs(curRaster.crs)
                else:
                    raise ValueError("Input CRS do not match")
            fCount = 0
            tCount = len(inVector['geometry'])
            for geometry in inVector['geometry']:
                fCount = fCount + 1
                if fCount % 100 == 0 and verbose:
                    print("Processing %s of %s" % (fCount, tCount) )
                # get pixel coordinates of the geometry's bounding box
                ul = curRaster.index(*geometry.bounds[0:2])
                lr = curRaster.index(*geometry.bounds[2:4])

                # read the subset of the data into a numpy array
                window = ((lr[0], ul[0]+1), (ul[1], lr[1]+1))
                #try:
                data = curRaster.read(bandNum, window=window)
                # create an affine transform for the subset data
                t = curRaster.affine
                shifted_affine = Affine(t.a, t.b, t.c+ul[1]*t.a, t.d, t.e, t.f+lr[0]*t.e)
                print geometry.wkt

                # rasterize the geometry
                mask = rasterize(
                    [(geometry, 0)],
                    out_shape=data.shape,
                    transform=shifted_affine,
                    fill=1,
                    all_touched=True,
                    dtype=numpy.uint8)

                # create a masked numpy array
                masked_data = numpy.ma.array(data=data, mask=mask.astype(bool))
                if rastType == 'N':
                    if minVal != '':
                        masked_data = numpy.ma.masked_where(masked_data < minVal, masked_data)
                        if masked_data.count() > 0:
                            results = [masked_data.sum(), masked_data.min(), masked_data.max(), masked_data.mean()]
                        else :
                            results = [-1, -1, -1, -1]
                    else:
                        results = [masked_data.sum(), masked_data.min(), masked_data.max(), masked_data.mean()]
                if rastType == 'C':
                    results = numpy.unique(masked_data, return_counts=True)

                outputData.append(results)

                '''
                except Exception as e:
                    print("Error %s: %s" % (fCount, e.message) )
                    outputData.append([-1, -1, -1, -1])
                '''
        return outputData

input_dir = r'/mnt/work/input/data_out/'
# input_image = r'/mnt/work/input/temp.vrt'
input_image = os.path.join(input_dir, fnmatch.filter(
    os.listdir(input_dir), "*.vrt")[0])
input_shape = r'/mnt/work/input/SampleData/agebs_val_muni.shp'

totalBands = rasterio.open(input_image, 'r').count + 1
for bndCnt in range(1, totalBands):
    print ("%s of %s" % (bndCnt, totalBands))
    # Run zonal statistics on raster using shapefile
    results = zonalStats(input_shape, input_image, bndCnt, True)
    allRes.append(results)
    allTitles.append("b%s_SUM" % bndCnt, "b%s_MIN" % bndCnt, "b%s_MAX" % bndCnt, "b%s_MEAN" % bndCnt, "b%s_SD" % bndCnt)

finalRes = pd.DataFrame(allRes, columns=allTitles)
finalRes.to_csv(os.path.join(output_folder, "Summarize_spFeas.csv"))
outJSON = { "status": "success", "reason": "cause you rock!" }
