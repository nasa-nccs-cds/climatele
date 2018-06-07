import cdms2 as cdms
import cdtime, math, cdutil
from climatele.EOFs.solver import EOFSolver


project = "MERRA2_EOFs"
varName = "ts"
data_path = 'https://dataserver.nccs.nasa.gov/thredds/dodsC/bypass/CREATE-IP/Reanalysis/NASA-GMAO/GEOS-5/MERRA2/mon/atmos/' + varName + '.ncml'
outDir = "/tmp/"
start_year = 1980
end_year = 2000
nModes = 4

experiment = 'MERRA2-' + varName + '('+str(start_year)+'-'+str(end_year)+')'
start_time = cdtime.comptime(start_year)
end_time = cdtime.comptime(end_year)

f = cdms.open(data_path)
variable = f(varName,latitude=(-80,80), level=(500,500) )  # type: cdms.AbstractVariable
print "Completed data read"

solver = EOFSolver( project, experiment, outDir )
solver.compute( variable, nModes )
print "Completed computing Eofs"

solver.plotEOFs()
solver.plotPCs()





