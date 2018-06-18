from climatele.plotter import ResultsPlotter, MPL
from climatele.project import *
import numpy.ma as ma

projectName = "MERRA2_EOFs"
varName = "ts"
outDir = "/tmp/"
start_year = 1980
end_year = 2015
nModes = 32
experiment = projectName + '_'+str(start_year)+'-'+str(end_year) + '_M' + str(nModes) + "_" + varName

if __name__ == "__main__":
    project = Project( outDir, projectName )
    plotter = ResultsPlotter( project.directory )
    plotResults = True
    nPlotCols = 5

    if plotResults:
        plotter.plotEOFs( project, experiment, nPlotCols, MPL )
        plotter.plotPCs( project, experiment, nPlotCols )

    eofVarList = project.getVariableNames( experiment, EOF )
    eofVariable0 = project.getVariable( eofVarList[0], experiment, EOF)
    eofRawData0 = eofVariable0.data  # type: ma.masked_array
    print "EOF variable shape: " + str( eofRawData0.shape )
