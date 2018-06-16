import cdms2 as cdms
import numpy as np
from netCDF4 import MFDataset
import cdtime, math, cdutil, time
from climatele.EOFs.solver import EOFSolver
from climatele.plotter import MPL, VCS
from climatele.aggregation import Aggregation, Collection

#------------------------------ SET PARAMETERS   ------------------------------

project = "MERRA2_EOFs"
varName = "ts"
collection = 'cip_merra2_mth-atmos-ts'
outDir = "/tmp/"
start_year = 1980
end_year = 2000
nModes = 4

experiment = project + '_'+str(start_year)+'-'+str(end_year) + '_' + varName
start_time = cdtime.comptime(start_year)
end_time = cdtime.comptime(end_year)

#------------------------------ READ DATA ------------------------------

read_start = time.time()
collection = Collection.new("cip_merra2_mth")
agg =  collection.getAggregation( varName )
files = agg.pathList()

print "files: " + str( files )
ds = MFDataset( files )
print "MFDataset: " + str( ds.variables.keys )

f = cdms.open( files[0] )
variable = f( varName, latitude=(-80,80), level=(500,500), time=(start_time,end_time) )  # type: cdms.fvariable.FileVariable
print "Completed data read in " + str(time.time()-read_start) + " sec "

#------------------------------ COMPUTE EOFS  ------------------------------

solver = EOFSolver( project, experiment, outDir )
solver.compute( variable, nModes, detrend=True, scale=True )
print "Completed computing Eofs"






