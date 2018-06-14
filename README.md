## climatele
Exploratory project for computing the normal modes of the climate system and investigating teleconnections and predictability.


#### Known Problems:

1) ImportError: ... version `CXXABI_1.3.9' not found.

  * This is due to a problem with the Anaconda env.  The best solution:
```    
    > conda remove gcc
    > conda install -c conda-forge "gcc_linux-64"  
```    
  * If that doesn't work then you can try the following: 
    In the …/anaconda2/envs/cdat8x/lib directory change links libstdc++.so and libstdc++.so.6 to point to the most recent libstdc++.so.* version (e.g. libstdc++.so.6.0.24)
    
    