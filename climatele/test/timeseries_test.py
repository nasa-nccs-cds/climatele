import cdms2 as cdms
import cdtime, math, cdutil, time
from climatele.EOFs.solver import EOFSolver
from climatele.plotter import PlotMgr
from climatele.project import *

#------------------------------ SET PARAMETERS   ------------------------------

projName = "MERRA2_EOFs"
varName = "ts"
data_path = 'https://dataserver.nccs.nasa.gov/thredds/dodsC/bypass/CREATE-IP/Reanalysis/NASA-GMAO/GEOS-5/MERRA2/mon/atmos/' + varName + '.ncml'
outDir = "/tmp/"
start_year = 1980
end_year = 2000
nModes = 4
latitiude = 38
longitude = 120
level = 500

experiment = projName + '_'+str(start_year)+'-'+str(end_year) + '_' + varName
start_time = cdtime.comptime(start_year)
end_time = cdtime.comptime(end_year)
solver = EOFSolver( projName, experiment, outDir )

#------------------------------ READ DATA ------------------------------

read_start = time.time()
f = cdms.open(data_path)
variable = f(varName,latitude=(latitiude,latitiude),longitude=(longitude,longitude), level=(level,level), squeeze=1 )  # type: cdms.tvariable.TransientVariable
print "Completed data read in " + str(time.time()-read_start) + " sec "


variable.setattribute( "long_name", experiment + ":  Raw Data" )

decycled_variable = solver.remove_cycle( variable )
decycled_variable.setattribute( "long_name", experiment + ": Cycle removed" )

detrended_variable = solver.remove_trend( decycled_variable, 100 )
detrended_variable.setattribute( "long_name", experiment + ": Trend removed" )

plotter = PlotMgr()
plotter.mpl_timeplot_variables( [ variable, decycled_variable, detrended_variable ], 3 )


