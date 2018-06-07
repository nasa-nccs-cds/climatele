from .cdms import Eof
import cdutil, os
import os.path
import cdms2 as cdms
import cdtime, math
from climatele.plotter import ResultsPlotter
PC = 0
EOF = 1

class EOFSolver:

    def __init__(self, _project, _experiment, _outDir ):
        self.project = _project
        self.experiment = _experiment
        self.directory = os.path.join( _outDir, self.project )
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)
        self.plotter = ResultsPlotter( self.directory )
        self.exts = { PC: '-PCs.nc', EOF: '-EOFs.nc' }

    def compute(self, data_variable, nModes, center=True, scale=True, removeCycle=True ):
        self.variable = data_variable                                                          # type: cdms.Variable
        data = cdutil.ANNUALCYCLE.departures(self.variable) if removeCycle else self.variable
        self.solver = Eof( data, weights='none', center=center, scale=scale )
        self.nModes = nModes
        print "Created solver"

        self.eofs = self.solver.eofs( neofs=nModes )
        self.pcs = self.solver.pcs().transpose()
        print "Computed EOFs"

        self.fracs = self.solver.varianceFraction()
        self.pves = [ str(round(float(frac*100.),1)) + '%' for frac in self.fracs ]
        self.save_results()
        print "Saved results"

    def save_results(self):
        self.savePCs()
        self.saveEOFs()

    def outfilePath(self, rType ):
        return os.path.join(self.directory, self.experiment + self.exts.get( rType, "Invalid response type: " + str(rType) ) )

    def savePCs(self):
        outfilePath = os.path.join( self.directory, self.outfilePath(PC) )
        outfile = cdms.open(outfilePath, 'w')
        timeAxis = self.variable.getTime()

        for iPlot in range(self.nModes):
            pc = self.pcs[iPlot]  # type: cdms.Variable
            plot_title_str = 'PC-' + str(iPlot) + ',' + self.experiment + ', ' + self.pves[iPlot]
            v = cdms.createVariable(pc.data, None, 0, 0, None, float('nan'), None, [timeAxis],  {"pve": self.pves[iPlot], "long_name": plot_title_str}, "PC-" + str(iPlot))
            outfile.write(v)
        outfile.close()

    def saveEOFs(self):
        outfilePath = os.path.join( self.directory, self.outfilePath(EOF)  )
        outfile = cdms.open(outfilePath, 'w')
        axes = [ self.variable.getLatitude(), self.variable.getLongitude() ]

        for iPlot in range(self.nModes):
            eof = self.eofs[iPlot]  # type: cdms.Variable
            plot_title_str = 'EOF-' + str(iPlot) + ',' + self.experiment + ', ' + self.pves[iPlot]
            v = cdms.createVariable(eof.data, None, 0, 0, None, float('nan'), None, axes,  {"pve": self.pves[iPlot], "long_name": plot_title_str}, "EOF-" + str(iPlot))
            outfile.write(v)
        outfile.close()

    def plotEOFs( self, nCols ):
        self.plotter.plotEOFs( self.outfilePath(EOF) , nCols )

    def plotPCs( self, nCols ):
        self.plotter.plotPCs ( self.outfilePath(PC), nCols  )
