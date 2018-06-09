from .cdms import Eof
import cdutil, os, time
import os.path
import cdms2 as cdms
import cdtime, math
from climatele.plotter import ResultsPlotter
from climatele.project import *
import numpy as np
from scipy import ndimage

class EOFSolver:

    def __init__(self, _project, experiment, outDir ):
        self.experiment = experiment
        self.project = Project( outDir, _project )
        self.plotter = ResultsPlotter( self.project.directory )

    def compute(self, data_variable, nModes, center=True, scale=True, removeCycle=True, detrend=True ):
        self.variable = data_variable                                                          # type: cdms.Variable
        decycled_data = self.remove_cycle(self.variable) if removeCycle else self.variable
        normalized_data = self.remove_trend(decycled_data,100) if detrend else decycled_data
        self.solver = Eof( normalized_data, weights='none', center=center, scale=scale )
        self.nModes = nModes
        print "Created solver"

        eof_start = time.time()
        self.eofs = self.solver.eofs( neofs=nModes )
        self.pcs = self.solver.pcs().transpose()
        print "Computed EOFs in " + str(time.time()-eof_start) + " sec "

        self.fracs = self.solver.varianceFraction()
        self.pves = [ str(round(float(frac*100.),1)) + '%' for frac in self.fracs ]
        self.save_results()
        print "Saved results"

    def remove_cycle(self, variable ):
        start = time.time()
        decycle = cdutil.ANNUALCYCLE.departures( variable )
        print "completed decycle in " + str(time.time()-start) + " sec "
        return decycle

    def remove_trend(self, variable, window_size ):
        start = time.time()
#        trend = np.apply_along_axis( lambda m: np.convolve(m, np.ones((window_size,))/window_size, mode='valid'), axis=0, arr=variable )
        trend = ndimage.convolve1d( variable.data, np.ones((window_size,))/float(window_size), 0, None, "reflect" )
        detrend = variable - trend
        print "completed detrend in " + str(time.time()-start) + " sec "
        return detrend

    def save_results(self):
        self.savePCs()
        self.saveEOFs()

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

    def saveEOFs(self):
        outfilePath = self.project.outfilePath( self.experiment, EOF )
        outfile = cdms.open(outfilePath, 'w')
        axes = [ self.variable.getLatitude(), self.variable.getLongitude() ]

        for iPlot in range(self.nModes):
            eof = self.eofs[iPlot]  # type: cdms.Variable
            plot_title_str = 'EOF-' + str(iPlot) + ',' + self.experiment + ', ' + self.pves[iPlot]
            v = cdms.createVariable(eof.data, None, 0, 0, None, float('nan'), None, axes,  {"pve": self.pves[iPlot], "long_name": plot_title_str}, "EOF-" + str(iPlot))
            outfile.write(v)
        outfile.close()

    def plotEOFs( self, nCols ):
        self.plotter.plotEOFs( self.project.outfilePath( self.experiment, EOF ) , nCols )

    def plotPCs( self, nCols ):
        self.plotter.plotPCs ( self.project.outfilePath( self.experiment, PC ), nCols  )
