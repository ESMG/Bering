import numpy as np
import netCDF4
import os
# These next two lines add the MOM6-examples/tools/analysis/ directory to the search path for python packages
import sys
sys.path.append('../../MOM6-examples/tools/analysis/')
# m6toolbox is a python package that has a function that helps visualize vertical sections
import m6toolbox
import matplotlib.pyplot as plt
from datetime import datetime
from pyroms_toolbox import jday2date
import pdb


z_file = netCDF4.Dataset('hourly_boom.nc')
grid_file = netCDF4.Dataset('sea_ice_geometry.nc')
xq = grid_file.variables['geolonb'][:] # This is the coordinate of the cell corners (u-points in 1D)
yq = grid_file.variables['geolatb'][:]
grid_file.close()

# Define a function to plot a section
def plot_section(file_handle, record, variable, x=19, vmin=None, vmax=None, plot_grid=True, rep='linear'):
    """Plots a section of by reading vertical grid and scalar variable and super-sampling
    both in order to plot vertical and horizontal reconstructions.

    Optional arguments have defaults for plotting salinity and overlaying the grid.
    """
    e = file_handle.variables['e'][record,:,118:125,19] # Vertical grid positions
    s = file_handle.variables[variable][record,:,118:125,x] # Scalar field to color
    x,z,q = m6toolbox.section2quadmesh(yq[117:125,123], e, s, representation=rep) # This yields three areas at twice the model resolution
    cs = plt.pcolormesh(x, z, q, vmin=vmin, vmax=vmax, cmap=cmap)
    if plot_grid: plt.plot(x, z.T, 'k');
#   if plot_grid: plt.plot(x, z.T, 'k', hold=True);
#   plt.ylim(-700,1)
    plt.ylim(-200,3)
    cbar = plt.colorbar(cs, orientation='horizontal')
    cbar.ax.tick_params(labelsize=15)
    #plt.xlim(400,600)

times = z_file.variables["time"][:]
ntimes = len(times)
cmap = plt.cm.get_cmap("seismic")
for record in range(ntimes-10,ntimes):
#record = -1 # Last record

    myday = jday2date(times[record]/24.)
    date_tag = myday.strftime('%H:%M, %d %B %Y')
    plt.figure(figsize=(10,6))
    plt.suptitle(date_tag, fontsize=20)
    plt.subplot(1,2,1); plot_section(z_file, record, x=20, variable='u', vmin=-1.5, vmax=1.5); plt.title('U');
    plt.subplot(1,2,2); plot_section(z_file, record, x=20, variable='v', vmin=-1.5, vmax=1.5); plt.title('V');
#   plt.subplot(2,2,1); plot_section(z_file, record, x=427, variable='u', vmin=-2., vmax=2.); plt.title('U');
#   plt.subplot(2,2,2); plot_section(z_file, record, variable='v', vmin=-2., vmax=2.); plt.title('V');
#   plt.subplot(2,2,3); plot_section(z_file, record, variable='salt', vmin=None, vmax=None); plt.title('salt');
#   plt.subplot(2,2,4); plot_section(z_file, record, variable='temp', vmin=None, vmax=None); plt.title('temp');
    fname = myday.strftime('movie_slice/frame_%(number)04d.png'%{'number': record})
    plt.savefig(fname)
    plt.close()

z_file.close()
