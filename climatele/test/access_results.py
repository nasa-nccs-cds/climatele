from climatele.plotter import ResultsPlotter
from climatele.project import *
import numpy.ma as ma

project = "MERRA2_EOFs"
outDir = "/tmp/"
start_year = 1980
end_year = 2000
varName = "ts"
experiment = project + '_'+str(start_year)+'-'+str(end_year) + '_' + varName

project = Project( outDir, project )
plotter = ResultsPlotter( project.directory )
plotResults = False

nPlotCols = 2
eofFilePath = project.outfilePath( experiment, EOF )
pcFilePath = project.outfilePath( experiment, PC )

if plotResults:
    plotter.plotEOFs( eofFilePath, nPlotCols )
    plotter.plotPCs( pcFilePath, nPlotCols )

eofVarList = project.getVariableNames( experiment, EOF)
print "EOF file: " + eofFilePath+ ", EOF variables: " + str(eofVarList)

eofVariable0 = project.getVariable( eofVarList[0], experiment, EOF)
eofRawData0 = eofVariable0.data  # type: ma.masked_array
print "EOF variable shape: " + str( eofRawData0.shape )
