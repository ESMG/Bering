Bering is a regional domain covering the Bering Sea at 10 km resolution. These are some of the files needed to run it with
MOM6-SIS2. The odd number of gridpoints came about because it was originally generated as a WRF grid by Rob Cermak.

For the processor mask: check_mask --grid_file INPUT/ocean_mosaic.nc --ocean_topog INPUT/ocean_topog.nc --min_pe 40 --max_pe 80 --halo 4 --model ocean
I took the 6.6x13 one which uses 72 cores.
