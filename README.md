## climatele
Exploratory project for computing the normal modes of the climate system and investigating teleconnections and predictability.

#### Setup

The following conda enviroment is recommended:

``` 
    > conda create -n climatele -c conda-forge -c cdat cdat
    > conda activate climatele
    > conda install -c anaconda netcdf4
```   

#### Installation

``` 
    > git clone https://github.com/nasa-nccs-cds/climatele.git
    > cd climatele
    > python setup.py install
```   

#### Known Problems:

1) ImportError: ... version `CXXABI_1.3.9' not found.

  * This is due to a known problem with the Anaconda env.  Solution: In the …/anaconda2/envs/cdat8x/lib directory change links libstdc++.so and libstdc++.so.6 to point to the most recent libstdc++.so.* version (e.g. libstdc++.so.6.0.24)
    
    