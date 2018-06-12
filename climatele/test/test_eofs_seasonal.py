import cdms2 as cdms
import cdtime, math, cdutil, time
from climatele.EOFs.solver import EOFSolver
from climatele.util.times import TimeSlicer

#------------------------------ SET PARAMETERS   ------------------------------

project = "MERRA2_EOFs"
varName = "ts"
data_path = 'https://dataserver.nccs.nasa.gov/thredds/dodsC/bypass/CREATE-IP/Reanalysis/NASA-GMAO/GEOS-5/MERRA2/mon/atmos/' + varName + '.ncml'
outDir = "/tmp/"
start_year = 1980
end_year = 2000
nModes = 4

experiment = project + '_'+str(start_year)+'-'+str(end_year) + '_' + varName
start_time = cdtime.comptime(start_year)
end_time = cdtime.comptime(end_year)

#------------------------------ READ DATA ------------------------------

read_start = time.time()
f = cdms.open(data_path)
variable = f(varName,latitude=(-80,80), level=(500,500) )  # type: cdms.AbstractVariable
slicer = TimeSlicer()
sliced_var = slicer.get( variable, "JJA" )
print "Completed data read in " + str(time.time()-read_start) + " sec "

#------------------------------ COMPUTE EOFS  ------------------------------

solver = EOFSolver( project, experiment, outDir )
solver.compute( sliced_var, nModes )
print "Completed computing Eofs"

#------------------------------ PLOT RESULTS   ------------------------------

solver.plotEOFs(2)
solver.plotPCs(2)





