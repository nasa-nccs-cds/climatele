import cdms2 as cdms
import cdtime, time

#------------------------------ SET PARAMETERS   ------------------------------

project = "MERRA2_EOFs"
varName = "ts"
data_path = 'https://dataserver.nccs.nasa.gov/thredds/dodsC/bypass/CREATE-IP/Reanalysis/NASA-GMAO/GEOS-5/MERRA2/mon/atmos/' + varName + '.ncml'
outDir = "/tmp/"
start_year = 1990
end_year = 2000
nModes = 4

experiment = project + '_'+str(start_year)+'-'+str(end_year) + '_' + varName
start_time = cdtime.comptime(start_year)
end_time = cdtime.comptime(end_year)

#------------------------------ READ DATA ------------------------------

read_start = time.time()
f = cdms.open(data_path)
variable = f(varName,latitude=(-80,80), level=(500,500), time=(start_time,end_time) )  # type: cdms.fvariable.FileVariable
#slicer = Seasons("JJA")
#sliced_var = slicer.get( variable )







