import os, datetime
import sortedcontainers

def parse_dict( dict_spec ):
    result = {}
    for elem in dict_spec.split(","):
        elem_toks = elem.split(":")
        result[ elem_toks[0].strip() ] = elem_toks[1].strip()

class Variable:

   def __init__(self, *args ):
       self.name = args[0].strip()
       self.long_name = args[1].strip()
       self.dods_name = args[2].strip()
       self.description = args[3].strip()
       self.shape = [ int(sval.strip()) for sval in args[4].split(",") ]
       self.resolution = parse_dict( args[5] )
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

    def __init__(self, _collection, *args ):
       self.collection = _collection
       self.start_time = float(args[0].strip())
       self.size = int(args[1].strip())
       self.relpath = args[2].strip()
       self.date = datetime.datetime.utcfromtimestamp(self.start_time*60)

    def getPath(self):
        return os.path.join( self.parm("base.path"), self.relpath )

    def parm(self, key ):
        return self.collection.parm( key )

class Collection:

    cacheDir = os.environ['EDAS_CACHE_DIR']
    baseDir = os.path.join( cacheDir, "collections", "agg" )

    @classmethod
    def new(cls, name ):
        agg_file = os.path.join( cls.baseDir, name + ".ag1" )
        return Collection( name, agg_file )

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
            elif type == 'C': self.dims[ toks[1].strip() ] = int( toks[2].strip() )
            elif type == 'V': self.vars[ toks[1].strip() ] = Variable( *toks[1:] )
            elif type == 'F': self.files[ toks[1].strip() ] = File( self, *toks[1:] )

    def parm(self, key ):
        return self.parms.get( key, "" )

    def file_list(self):
        # type: () -> list[File]
        return self._files.values()


if __name__ == "__main__":
    collection = Collection.new( "cip_merra2_mth-atmos-ts" )
    for file in collection.files.values():
        print str(file.date) +": " + file.getPath()