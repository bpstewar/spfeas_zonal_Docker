#!/usr/bin/env python

import os, time
import fnmatch
import json

import rasterio
import numpy
import geopandas as gpd
import pandas as pd

from affine import Affine
from rasterio.features import rasterize

from gbdx_task_interface import GbdxTaskInterface

def zonalStats(inVector, inRaster, bandNum=1, reProj = False, minVal = '', rastType='N', verbose=False):
        outputData=[]
        with rasterio.open(inRaster, 'r') as curRaster:
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
                try:
                    data = curRaster.read(bandNum, window=window)
                    # create an affine transform for the subset data
                    t = curRaster.affine
                    shifted_affine = Affine(t.a, t.b, t.c+ul[1]*t.a, t.d, t.e, t.f+lr[0]*t.e)

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
                    
                except Exception as e: 
                    print("Error %s: %s" % (fCount, e.message) )                               
                    outputData.append([-1, -1, -1, -1])
        return outputData   
    

class SpFeasTask(GbdxTaskInterface):
    
    def invoke(self):

        # Create the output folder  
        output_folder = self.get_output_data_port('data_out')
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Get the input image
        input_dir = self.get_input_data_port('rasterIn', default="/mnt/work/input")       
        input_image = os.path.join(input_dir, fnmatch.filter(os.listdir(input_dir), "*.vrt")[0])

        # Get the input shapefile
        input_shape_folder = self.get_input_data_port('shapeIn', default="/mnt/work/input")       
        input_shape = os.path.join(input_dir, fnmatch.filter(os.listdir(input_dir), "*.shp")[0])
        
        allRes = []
        allTitles = []
        totalBands = rasterio.open(input_image, 'r').count + 1
        inputShapeD = gpd.read_file(input_shape)
        origD = inputShapeD
        for bndCnt in range(1, totalBands):    
            # Run zonal statistics on raster using shapefile
            results = zonalStats(origD, input_image, bndCnt, True)
            allRes.append(results)
            columnNames = ["b%s_SUM" % bndCnt, "b%s_MIN" % bndCnt, "b%s_MAX" % bndCnt, "b%s_MEAN" % bndCnt]            
            curRes = pd.DataFrame(results, columns = columnNames)
            inputShapeD = pd.concat([inputShapeD, curRes], axis=1)
        
        #inputShapeD.drop('geometry', 1)
        inputShapeD.to_csv(os.path.join(output_folder, "Summarize_spFeas.csv"))
        outJSON = { "status": "success", "reason": "cause you rock!" }
        
        #Write status file as output
        with open("/mnt/work/status.json", 'w') as statusFile:
            json.dump(outJSON, statusFile)
            
if __name__ == '__main__':

    with SpFeasTask() as task:
        task.invoke()
