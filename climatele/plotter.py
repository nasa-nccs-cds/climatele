
import logging, os, time
import cdms2, datetime, matplotlib, math
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from climatele import Params
import numpy as np
import vcs, EzTemplate
from typing import List, Any

class ResultsPlotter:

    def __init__(self, projectDir ):
        self.dir = projectDir
        self.plotter = PlotMgr()

    def plotPCs( self, nCols=4 ):
        for root, dirs, files in os.walk(self.dir):
            for filename in files:
                if( filename.endswith( Params.PcExt )):
                    dataPath = os.path.join(self.dir,filename)
                    print "Plotting PC results from file " + dataPath
                    self.plotter.mpl_timeplot( dataPath, nCols )

    def plotEOFs( self, nCols, smooth=True ):
        for root, dirs, files in os.walk(self.dir):
            for filename in files:
                if( filename.endswith( Params.EofExt )):
                    dataPath = os.path.join(self.dir,filename)
                    print "Plotting EOF results from file " + dataPath
                    self.plotter.mpl_spaceplot( dataPath, nCols, 0, smooth )

class PlotMgr:

    def __init__(self):
        self.logger = logging.getLogger('cwt.wps')


    def graph_data(self , data, title="" ):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        xvalues = range( len(data ) )
        ax.set_title( title )
        ax.plot( xvalues, data )
        plt.show()

    def mpl_timeplot( self, dataPath, numCols = 4 ):
        if dataPath:
            for k in range(0,30):
                if( os.path.isfile(dataPath) ):
                    self.logger.info( "Plotting file: " +  dataPath )
                    f = cdms2.openDataset(dataPath) # type: cdms2.dataset.CdmsFile
                    varNames = [ vn for vn in f.variables.keys() if not vn.endswith('bnds') ]  # type: List[str]
                    varNames.sort()
                    fig = plt.figure()    # type: Figure
                    iplot = 1
                    nCols = min( len(varNames), numCols )
                    nRows = math.ceil( len(varNames) / float(nCols) )
                    for varName in varNames:  # type: str
                        self.logger.info( "  ->  Plotting variable: " +  varName + ", subplot: " + str(iplot) )
                        timeSeries = f( varName, squeeze=1 )  # type: cdms2.Variable
                        long_name = timeSeries.attributes.get('long_name')
                        datetimes = [datetime.datetime(x.year, x.month, x.day, x.hour, x.minute, int(x.second)) for x in timeSeries.getTime().asComponentTime()]
                        dates = matplotlib.dates.date2num(datetimes)
                        ax = fig.add_subplot( nRows, nCols, iplot )
                        title = varName if long_name is None else long_name
                        ax.set_title( title )
                        ax.plot(dates, timeSeries.data )
                        ax.xaxis.set_major_formatter( mdates.DateFormatter('%b %Y') )
                        ax.grid(True)
                        iplot = iplot + 1

                    fig.autofmt_xdate()
                    plt.show()
                    return
                else: time.sleep(1)


    def getAxis(self, axes, atype ):
        for axis in axes:
            try:
                if( (atype == "X") and self.isLongitude(axis) ): return axis[:]
                if( (atype == "Y") and self.isLatitude(axis) ): return axis[:]
                if( (atype == "Z") and axis.isLevel() ): return axis[:]
                if( (atype == "T") and axis.isTime() ): return axis[:]
            except Exception as ex:
                print "Exception in getAxis({0})".format(atype), ex
        return None

    def isLongitude(self, axis ):
        id = axis.id.lower()
        hasAxis = hasattr(axis, 'axis')
        isX = axis.axis == 'X'
        if ( hasAxis and isX ): return True
        return ( id.startswith( 'lon' ) )

    def isLatitude(self, axis ):
        id = axis.id.lower()
        if (hasattr(axis, 'axis') and axis.axis == 'Y'): return True
        return ( id.startswith( 'lat' ) )

    def getRowsCols( self, number ):
        largest_divisor = 1
        for i in range(2, number):
            if( number % i == 0 ):
                largest_divisor = i
        complement = number/largest_divisor
        return (complement,largest_divisor) if( largest_divisor > complement ) else (largest_divisor,complement)

    def mpl_plot(self, dataPath, timeIndex=0, smooth=False):
        f = cdms2.openDataset(dataPath)
        var = f.variables.values()[0]
        naxes = self.getNAxes( var.shape )
        if( naxes == 1 ): self.mpl_timeplot( dataPath )
        else: self.mpl_spaceplot( dataPath, timeIndex, smooth )

    def getNAxes(self, shape ):
        naxes = 0
        for axisLen in shape:
            if( axisLen > 1 ):
                naxes = naxes + 1
        return naxes

    def mpl_spaceplot( self, dataPath, numCols=4, timeIndex=0, smooth=False ):
        if dataPath:
            for k in range(0,30):
                if( os.path.isfile(dataPath) ):
                    self.logger.info( "Plotting file: " +  dataPath )
                    f = cdms2.openDataset(dataPath) # type: cdms2.dataset.CdmsFile
                    vars = f.variables.values()
                    axes = f.axes.values()
                    lons = self.getAxis( axes , "X" )
                    lats = self.getAxis( axes , "Y" )
                    fig = plt.figure()
                    varNames = list( map( lambda v: v.id, vars ) )
                    varNames.sort()
                    nCols = min( len(varNames), numCols )
                    nRows = math.ceil( len(varNames) / float(nCols) )
                    iplot = 1
                    for varName in varNames:
                        if not varName.endswith("_bnds"):
                            try:
                                variable = f( varName )
                                if len( variable.shape ) > 1:
                                    m = Basemap( llcrnrlon=lons[0],
                                                 llcrnrlat=lats[0],
                                                 urcrnrlon=lons[len(lons)-1],
                                                 urcrnrlat=lats[len(lats)-1],
                                                 epsg='4326',
                                                 lat_0 = lats.mean(),
                                                 lon_0 = lons.mean())
                                    ax = fig.add_subplot( nRows, nCols, iplot )
                                    ax.set_title(varName)
                                    lon, lat = np.meshgrid( lons, lats )
                                    xi, yi = m(lon, lat)
                                    smoothing = 'gouraud' if smooth else 'flat'
                                    spatialData = variable( time=slice(timeIndex,timeIndex+1), squeeze=1 )
                                    cs2 = m.pcolormesh(xi, yi, spatialData, cmap='jet', shading=smoothing )
                                    lats_space = abs(lats[0])+abs(lats[len(lats)-1])
                                    m.drawparallels(np.arange(lats[0],lats[len(lats)-1], round(lats_space/5, 0)), labels=[1,0,0,0], dashes=[6,900])
                                    lons_space = abs(lons[0])+abs(lons[len(lons)-1])
                                    m.drawmeridians(np.arange(lons[0],lons[len(lons)-1], round(lons_space/5, 0)), labels=[0,0,0,1], dashes=[6,900])
                                    m.drawcoastlines()
                                    m.drawstates()
                                    m.drawcountries()
                                    cbar = m.colorbar(cs2,location='bottom',pad="10%")
                                    print "Plotting variable: " + varName
                                    iplot = iplot + 1
                            except:
                                print "Skipping variable: " + varName
                    plt.show()
                    return
                else: time.sleep(1)

    def print_Mdata(self, dataPath ):
        for k in range(0,30):
            if( os.path.isfile(dataPath) ):
                f = cdms2.openDataset(dataPath)
                for variable in f.variables.values():
                    self.logger.info( "Produced result " + variable.id + ", shape: " +  str( variable.shape ) + ", dims: " + variable.getOrder() + " from file: " + dataPath )
                    self.logger.info( "Data Sample: " + str( variable[0] ) )
                    return
            else: time.sleep(1)



    def print_data(self, dataPath ):
        for k in range(0,30):
            if( os.path.isfile(dataPath) ):
                try:
                    f = cdms2.openDataset(dataPath) # """:type : cdms2.CdmsFile """
                    varName = f.variables.values()[0].id
                    spatialData = f( varName ) # """:type : cdms2.FileVariable """
                    self.logger.info( "Produced result, shape: " +  str( spatialData.shape ) + ", dims: " + spatialData.getOrder() )
        #            self.logger.info( "Data: \n" + ', '.join( str(x) for x in spatialData.getValue() ) )
                    self.logger.info( "Data: \n" + str( spatialData.squeeze().flatten().getValue() ) )
                except Exception:
                    self.logger.error( " ** Error printing result data ***")
                return
            else: time.sleep(1)


    def plot_eofs( eofs, nMode, experiment_title, pve ):
        canvas = vcs.init(geometry=(1400,1000))
        canvas.open()
        canvas.setcolormap('bl_to_darkred')
        M=EzTemplate.Multi(rows=nMode/2,columns=2)
        M.margins.top=0.1
        M.margins.bottom=0.05
        M.spacing.horizontal=.05
        M.spacing.vertical=.05

        for iPlot in range( nMode ):
            iso = canvas.createisofill()
            level_distribution = np.array( [-1.0, -0.9, -0.8, -0.7, -0.6, -0.5, -0.4, -0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0] )
            iso.levels = list( level_distribution*0.007 )
            iso.ext_1 = 'y' # control colorbar edge (arrow extention on/off)
            iso.ext_2 = 'y' # control colorbar edge (arrow extention on/off)
            cols = vcs.getcolors(iso.levels, range(16,240), split=0)
            iso.fillareacolors = cols
            iso.missing = 0
            variable = eofs[iPlot]
            percentage = str(round(float(pve[iPlot]*100.),1)) + '%'
            plot_title_str = 'EOF mode ' + str(iPlot) + ',' + experiment_title +  ', ' + percentage

            p = vcs.createprojection()
            p.type = 'robinson'
            iso.projection = p
            t=M.get( legend='local' )
            variable.setattribute( "long_name", plot_title_str )
            canvas.plot(variable,iso,t)
            canvas.png('/tmp/eof_analysis-mode{0}.png'.format(iPlot))

        canvas.interact()

