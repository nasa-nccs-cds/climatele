from .cdms import Eof
import time
from climatele.plotter import ResultsPlotter
from climatele.project import *
from cdutil.times import ANNUALCYCLE
import numpy as np


class EOFSolver:

    def __init__(self, _project, experiment, outDir ):
        self.experiment = experiment
        self.project = Project( outDir, _project )
        self.plotter = ResultsPlotter( self.project.directory )

    def compute(self, data_variable, nModes, **kwargs ):
        removeCycle = kwargs.get( "decycle", True )
        detrend = kwargs.get( "detrend", False )
        self.variable = data_variable                                       # type: cdms.tvariable.TransientVariable
        decycled_data = self.remove_cycle(self.variable) if removeCycle else self.variable
        detrended_data = self.remove_trend(decycled_data,100) if detrend else decycled_data
        self.nModes = nModes

        eof_start = time.time()
        self.solver = Eof( detrended_data, **kwargs )
        self.eofs = self.solver.eofs( neofs=nModes )
        self.pcs = self.solver.pcs( npcs=nModes ).transpose()
        self.projected_pcs = self.solver.projectField(detrended_data,neofs=32).transpose()
        self.fracs = self.solver.varianceFraction( neigs=nModes )
        self.pves = [ str(round(float(frac*100.),1)) + '%' for frac in self.fracs ]
        print "Computed EOFs in " + str(time.time()-eof_start) + " sec "

        self.save_results()

    def remove_cycle(self, variable ):
        start = time.time()
        decycle = ANNUALCYCLE.departures( variable )
        print "completed decycle in " + str(time.time()-start) + " sec "
        return decycle

    def remove_trend(self, variable, window_size ):
        from scipy import ndimage
        start = time.time()
        trend = ndimage.convolve1d( variable.data, np.ones((window_size,))/float(window_size), 0, None, "reflect" )
        detrend = variable - trend
        print "completed detrend in " + str(time.time()-start) + " sec "
        return detrend

    def save_results(self):
        start = time.time()
        self.savePCs()
        self.saveEOFs()
        print "Saved results in " + str(time.time() - start) + " sec "

    def savePCs(self):
        outfilePath = self.project.outfilePath( self.experiment, PC )
        outfile = cdms.open(outfilePath, 'w')
        timeAxis = self.variable.getTime()

        for iPlot in range(self.nModes):
            pc = self.pcs[iPlot]  # type: cdms.Variable
            plot_title_str = 'PC-' + str(iPlot) + ',' + self.experiment + ', ' + self.pves[iPlot]
            v = cdms.createVariable(pc.data, None, 0, 0, None, float('nan'), None, [timeAxis],  {"pve": self.pves[iPlot], "long_name": plot_title_str}, "PC-" + str(iPlot))
            outfile.write(v)
        outfile.close()
        print "Saved PCs to file " + outfilePath

    def saveEOFs(self):
        outfilePath = self.project.outfilePath( self.experiment, EOF )
        outfile = cdms.open(outfilePath, 'w')
        axes = [ self.variable.getLatitude(), self.variable.getLongitude() ]

        for iPlot in range(self.nModes):
            eof = self.eofs[iPlot]  # type: cdms.tvariable.TransientVariable
            plot_title_str = 'EOF-' + str(iPlot) + ',' + self.experiment + ', ' + self.pves[iPlot]
            eof_data = eof.data.squeeze()
            v = cdms.createVariable( eof_data, None, 0, 0, None, float('nan'), None, axes,  { "pve": self.pves[iPlot], "long_name": plot_title_str }, "EOF-" + str(iPlot) )
            outfile.write(v)
        outfile.close()
        print "Saved EOFs to file " + outfilePath

    def plotEOFs( self, nCols, plotPkg ):
        self.plotter.plotEOFs( self.project, self.experiment, nCols, plotPkg )

    def plotPCs( self, nCols ):
        self.plotter.plotPCs ( self.project, self.experiment, nCols  )

    def plotPCComparison(self, nModes ):
        vars = [ self.projected_pcs, self.pcs ]
        self.plotter.plotter.mpl_comparison_timeplot_variables( self.variable, vars, nModes)
