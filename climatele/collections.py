import os
import cdms2 as cdms

class Collections:

    def __init__(self):
        self.cacheDir = os.environ['EDAS_CACHE_DIR']
        self.baseDir = os.path.join( self.cacheDir, "collections", "agg" )

    def getCollection( self, name ):
        agg_file = os.path.join( self.baseDir, name + ".ag1" )
        return Collection( name, agg_file )




class Collection:

    def __init__(self, _name, _agg_file ):
        self.name = _name
        self.file = _agg_file
        self.parms = {}
        self.files = {}
        self.axes = {}
        self.vars = {}
        self._parseAggFile()

    def _parseAggFile(self):
        file = open( self.file, "r" )
        for line in file.readlines():
            if not line: break
            print line


if __name__ == "__main__":
    collections = Collections()
    collection = collections.get( "cip_merra2_mth-atmos-ts" )