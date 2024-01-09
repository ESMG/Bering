import numpy as np
import netCDF4
import sys

ncfile = sys.argv[1]
nc = netCDF4.Dataset(ncfile, 'r')

v = nc.variables['v'][1,:,:,:]

dims = v.shape

vmin = v[0,0,0]
imin = 0
jmin = 0
kmin = 0
for k in range(dims[0]):
  for j in range(dims[1]):
    for i in range(dims[2]):
      if (v[k,j,i] < vmin):
        vmin = v[k,j,i]
        imin = i
        jmin = j
        kmin = k

print(imin, jmin, kmin, vmin)

vmax = v[0,0,0]
imax = 0
jmax = 0
kmax = 0
for k in range(dims[0]):
  for j in range(dims[1]):
    for i in range(dims[2]):
      if (v[k,j,i] > vmax):
        vmax = v[k,j,i]
        imax = i
        jmax = j
        kmax = k

print(imax, jmax, kmax, vmax)
