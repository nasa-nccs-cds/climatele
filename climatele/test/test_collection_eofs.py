import cdms2 as cdms
import numpy as np
from netCDF4 import MFDataset, Variable
import cdtime, math, cdutil, time
from climatele.EOFs.solver import EOFSolver
from climatele.plotter import MPL, VCS
from climatele.aggregation import Aggregation, Collection

#------------------------------ SET PARAMETERS   ------------------------------

project = "MERRA2_EOFs"
varName = "tas"
collectionName = 'giss_r1i1p1'
outDir = "/tmp/"
start_year = 1800
end_year = 2100
nModes = 4

experiment = project + '_'+str(start_year)+'-'+str(end_year) + '_' + varName
start_time = cdtime.comptime(start_year)
end_time = cdtime.comptime(end_year)

#------------------------------ READ DATA ------------------------------

read_start = time.time()
collection = Collection.new( collectionName )
agg = collection.getAggregation(collectionName)
dset = agg.getDataset()
axis = agg.getAxis('x')

print str( axis )





