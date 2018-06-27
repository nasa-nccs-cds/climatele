import cdms2 as cdms
import cdtime, math, cdutil, time, os
from climatele.EOFs.solver import EOFSolver
from climatele.plotter import MPL, VCS

#------------------------------ SET PARAMETERS   ------------------------------

project = "MERRA2_EOFs"
varName = "zg"
outDir = os.path.expanduser("~/results/")
start_year = 1980
end_year = 2015
nModes = 32
plotResults = True
level = 100000

data_path = 'https://dataserver.nccs.nasa.gov/thredds/dodsC/bypass/CREATE-IP/Reanalysis/NASA-GMAO/GEOS-5/MERRA2/mon/atmos/' + varName + '.ncml'
start_time = cdtime.comptime(start_year)
end_time = cdtime.comptime(end_year)

#------------------------------ READ DATA ------------------------------

read_start = time.time()

if level:
    experiment = project + '_'+str(start_year)+'-'+str(end_year) + '_M' + str(nModes) + "_" + varName + "-" + str(level)
    f = cdms.open(data_path)
    variable = f( varName, latitude=(-80,80), level=(level,level), time=(start_time,end_time) )  # type: cdms.tvariable.TransientVariable
else:
    experiment = project + '_'+str(start_year)+'-'+str(end_year) + '_M' + str(nModes) + "_" + varName
    f = cdms.open(data_path)
    variable = f( varName, latitude=(-80,80), time=(start_time,end_time) )  # type: cdms.tvariable.TransientVariable


print "Completed data read in " + str(time.time()-read_start) + " sec "

#------------------------------ COMPUTE EOFS  ------------------------------

solver = EOFSolver( project, experiment, outDir )
solver.compute( variable, nModes, detrend=True, scale=True )
print "Completed computing Eofs"

#------------------------------ PLOT RESULTS   ------------------------------

if plotResults:
    solver.plotEOFs( 5, MPL )    # Change MPL to VCS for vcs plots (thomas projection)
    solver.plotPCs( 5 )





