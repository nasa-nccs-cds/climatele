import os, datetime
import sortedcontainers
import netCDF4
import numpy as np

def parse_dict( dict_spec ):
    result = {}
    for elem in dict_spec.split(","):
        elem_toks = elem.split(":")
        result[ elem_toks[0].strip() ] = elem_toks[1].strip()

def intArg( sarg, default = 0 ):
    return int(sarg) if( sarg ) else default

def floatArg( sarg, default = float("nan") ):
    return float(sarg) if( sarg ) else default

class Collection:

    cacheDir = os.environ['EDAS_CACHE_DIR']
    baseDir = os.path.join( cacheDir, "collections", "agg" )

    @classmethod
    def new(cls, name ):
        # type: (str) -> Collection
        spec_file = os.path.join( cls.baseDir, name + ".csv" )
        return Collection(name, spec_file)

    def __init__(self, _name, _spec_file ):
        self.name = _name
        self.spec = _spec_file
        self.aggs = {}
        self.parms = {}
        self._parseSpecFile()

    def _parseSpecFile(self):
        file = open( self.spec, "r" )
        for line in file.readlines():
            if not line: break
            if( line[0] == '#' ):
                toks = line[1:].split(",")
                self.parms[toks[0].strip()] = ",".join(toks[1:]).strip()
            else:
                toks = line.split(",")
                self.aggs[toks[0].strip()] = ",".join(toks[1:]).strip()

    def getAggregation( self, varName ):
        # type: (str) -> Aggregation
        agg_id = self.aggs.get( varName )
        agg_file = os.path.join( Collection.baseDir, agg_id + ".ag1")
        return Aggregation( self.name, agg_file )

    def getVariable( self, varName ):
        # type: (str) -> netCDF4.Variable
        agg =  self.getAggregation( varName )
        return agg.getVariable(varName)

class Variable:

   def __init__(self, *args ):
       self.name = args[0].strip()
       self.long_name = args[1].strip()
       self.dods_name = args[2].strip()
       self.description = args[3].strip()
       self.shape = [ intArg(sval.strip()) for sval in args[4].split(",") ]
       self.resolution = parse_dict( args[5] )
       self.dims = args[6].strip().split(' ')
       self.units = args[7].strip()

class Axis:

   def __init__(self, *args ):
       self.name = args[0].strip()
       self.long_name = args[1].strip()
       self.type = args[2].strip()
       self.length = intArg(args[3].strip())
       self.units = args[4].strip()
       self.bounds = [ floatArg(args[5].strip()), floatArg(args[6].strip()) ]

   def getIndexList(self, dset, min_value, max_value):
       values = dset.variables[self.name][:]
       return np.where((values > min_value) & (values < max_value))

class File:

    def __init__(self, _collection, *args ):
       self.collection = _collection
       self.start_time = float(args[0].strip())
       self.size = intArg(args[1].strip())
       self.relpath = args[2].strip()
       self.date = datetime.datetime.utcfromtimestamp(self.start_time*60)

    def getPath(self):
        return os.path.join( self.parm("base.path"), self.relpath )

    def parm(self, key ):
        return self.collection.parm( key )

class Aggregation:

    def __init__(self, _name, _agg_file ):
        self.name = _name
        self.spec = _agg_file
        self.parms = {}
        self.files = sortedcontainers.SortedDict()
        self.axes = {}
        self.dims = {}
        self.vars = {}
        self._parseAggFile()

    def _parseAggFile(self):
        file = open( self.spec, "r" )
        for line in file.readlines():
            if not line: break
            toks = line.split(";")
            type = toks[0]
            if type == 'P': self.parms[ toks[1].strip() ] = ";".join( toks[2:] ).strip()
            elif type == 'A': self.axes[ toks[3].strip() ] = Axis( *toks[1:] )
            elif type == 'C': self.dims[ toks[1].strip() ] = intArg( toks[2].strip() )
            elif type == 'V': self.vars[ toks[1].strip() ] = Variable( *toks[1:] )
            elif type == 'F': self.files[ toks[1].strip() ] = File( self, *toks[1:] )

    def getAxis( self, atype ):
        return next((x for x in self.axes.values() if x.type == atype), None)

    def parm(self, key ):
        return self.parms.get( key, "" )

    def fileList(self):
        # type: () -> list[File]
        return self.files.values()

    def pathList(self):
        # type: () -> list[str]
        return [ file.getPath() for file in self.files.values() ]

    def getVariable( self, varName ):
        # type: (str) -> netCDF4.Variable
        ds = self.getDataset()
        return ds.variables[varName]

    def getDataset( self ):
        # type: () -> netCDF4.MFDataset
        return netCDF4.MFDataset( self.pathList() )