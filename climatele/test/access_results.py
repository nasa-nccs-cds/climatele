from climatele.plotter import ResultsPlotter
from climatele.project import *
import numpy.ma as ma

projectName = "MERRA2_EOFs"
outDir = "/tmp/"
start_year = 1980
end_year = 2000
varName = "ts"
experiment = projectName + '_'+str(start_year)+'-'+str(end_year) + '_' + varName

project = Project( outDir, projectName )
plotter = ResultsPlotter( project.directory )
plotResults = True
nPlotCols = 2

if plotResults:
    plotter.plotEOFs( project, experiment, nPlotCols )
    plotter.plotPCs( project, experiment, nPlotCols )

eofVarList = project.getVariableNames( experiment, EOF )
eofVariable0 = project.getVariable( eofVarList[0], experiment, EOF)
eofRawData0 = eofVariable0.data  # type: ma.masked_array
print "EOF variable shape: " + str( eofRawData0.shape )
