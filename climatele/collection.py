import os
import cdms2 as cdms
import collections, sortedcontainers

class Variable:
   def __init__(self, *args ):
       self.name = args[0].strip()
       self.long_name = args[1].strip()
       self.dods_name = args[2].strip()
       self.description = args[3].strip()
       self.shape = [ int(sval.strip()) for sval in args[4].split(",") ]
       self.resolution = dict( args[5] )
       self.dims = args[6].strip().split(' ')
       self.units = args[7].strip()

class Axis:
   def __init__(self, *args ):
       self.name = args[0].strip()
       self.long_name = args[1].strip()
       self.type = args[2].strip()
       self.length = int(args[3].strip())
       self.units = args[4].strip()
       self.bounds = [ float(args[5].strip()), float(args[6].strip()) ]

class File:
   def __init__(self, *args ):
       self.start_time = float(args[0].strip())
       self.size = int(args[1].strip())
       self.path = args[2].strip()

class CollectionFactory:

    def __init__(self):
        self.cacheDir = os.environ['EDAS_CACHE_DIR']
        self.baseDir = os.path.join( self.cacheDir, "collections", "agg" )

    def get( self, name ):
        # type: (str) -> Collection
        agg_file = os.path.join( self.baseDir, name + ".ag1" )
        return Collection( name, agg_file )

class Collection:

    def __init__(self, _name, _agg_file ):
        self.name = _name
        self.file = _agg_file
        self.parms = {}
        self.files = sortedcontainers.SortedDict()
        self.axes = {}
        self.dims = {}
        self.vars = {}
        self._parseAggFile()

    def _parseAggFile(self):
        file = open( self.file, "r" )
        for line in file.readlines():
            if not line: break
            toks = line.split(";")
            type = toks[0]
            if type == 'P': self.parms[ toks[1] ] = ";".join( toks[2:] )
            elif type == 'A': self.axes[ toks[3] ] = Axis( *toks[1:] )
            elif type == 'C': self.dims[ toks[1] ] = int( toks[2] )
            elif type == 'V': self.vars[ toks[1] ] = Variable( *toks[1:] )
            elif type == 'F': self.files[ toks[1] ] = File( *toks[1:] )


if __name__ == "__main__":
    colls = CollectionFactory()
    collection = colls.get( "cip_merra2_mth-atmos-ts" )