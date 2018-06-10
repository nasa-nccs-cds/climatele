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
detrend_window = 7

detrended_variable0 = solver.remove_cycle( variable, detrend_window )
detrended_variable0.setattribute( "long_name", experiment + ": Cycle/Trend removed" )

decycled_variable = solver.remove_cycle( variable )
detrended_variable1 = solver.remove_trend( decycled_variable, detrend_window*12 )
detrended_variable1.setattribute( "long_name", experiment + ": Cycle & Trend removed separately" )

diff0 = detrended_variable0-decycled_variable
diff0.setattribute( "long_name",  "DIFF: Cycle/Trend removed" )
diff1 = detrended_variable1-decycled_variable
diff1.setattribute( "long_name", "DIFF: Cycle & Trend removed separately" )

plotter = PlotMgr()
plotter.mpl_timeplot_variables( [ diff0, diff1 ], 2 )


