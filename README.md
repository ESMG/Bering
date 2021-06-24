Bering is a regional domain covering the Bering Sea at 10 km resolution. These are some of the files needed to run it with
MOM6-SIS2. The odd number of gridpoints came about because it was originally generated as a WRF grid by Rob Cermak.

For the processor mask: check_mask --grid_file INPUT/ocean_mosaic.nc --ocean_topog INPUT/ocean_topog.nc --min_pe 40 --max_pe 80 --halo 4 --model ocean
I took the 6.6x13 one which uses 72 cores.

or (doesn't change answers)

check_mask --grid_file INPUT/ocean_mosaic.nc --ocean_topog INPUT/ocean_topog.nc --min_pe 24 --max_pe 80 --halo 4 --nobc 4 --direction north,west,south,east --is 192,1,1,237 --ie 237,1,230,237 --js 277,1,1,143 --je 277,275,1,277 --model ocean
