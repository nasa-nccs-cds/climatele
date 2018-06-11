from climatele.plotter import PlotMgr
from climatele.project import *
import datetime, matplotlib, math
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from climatele.project import *


projectName = "MERRA2_EOFs"
outDir = "/tmp/"
start_year = 1980
end_year = 2000
varName = "ts"
experiment = projectName + '_'+str(start_year)+'-'+str(end_year) + '_' + varName
project = Project( outDir, projectName )
file_path = os.path.dirname(os.path.realpath(__file__))

enso = open(file_path + "/enso_data.txt", "r")
months = range( 1, 13, 1 )
datetimes1 = []
enso_values = []

while True:
    line = enso.readline()
    toks = line.split()
    if not toks: break
    year = int( toks[0] )
    for month in months:
        datetimes1.append(  datetime.datetime( year, month, 1, 1, 1, 1 ) )
        enso_values.append( float( toks[month] ) )

pcVarList = project.getVariableNames( experiment, PC )
pcVariable = project.getVariable( pcVarList[0], experiment, PC)

fig = plt.figure()    # type: Figure
varName = pcVariable.id
long_name = pcVariable.attributes.get('long_name')
ax = fig.add_subplot( 1, 1, 1 )
title = varName if long_name is None else long_name
ax.set_title( title )

datetimes0 = [datetime.datetime(x.year, x.month, x.day, x.hour, x.minute, int(x.second)) for x in pcVariable.getTime().asComponentTime()]
dates0 = matplotlib.dates.date2num(datetimes0)
ax.plot(dates0, ( pcVariable.data * -0.008 ) + 0.4, label = "PC Timeseries for first EOF" )

dates1 = matplotlib.dates.date2num( datetimes1 )
ax.plot(dates1, enso_values, label = "ENSO Index"  )

ax.xaxis.set_major_formatter( mdates.DateFormatter('%b %Y') )
ax.grid(True)
fig.autofmt_xdate()
plt.legend()
plt.show()

