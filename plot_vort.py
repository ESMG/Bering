import numpy as np
import netCDF4
import os
import sys
import subprocess
import pyroms
from pyroms_toolbox import jday2date
import projmap
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# draw line around map projection limb.
# color background of map projection region.
# missing values over land will show up this color.
# plot sst, then ice with pcolor
# add a title.
#year = int(sys.argv[1])
#lst_year = [year]

lst_file = []

#for year in lst_year:
#    year = np.str(year)
#lst = subprocess.getoutput('ls clima/*.nc')
lst = subprocess.getoutput('ls 19800104.ocean_daily_old.nc')
lst = lst.split()
lst_file = lst_file + lst

#grd = netCDF4.Dataset('sea_ice_geometry.nc', "r")
#clat = grd.variables["geolatb"][:]
#clon = grd.variables["geolonb"][:]
grd = netCDF4.Dataset('INPUT/ocean_hgrid.nc', "r")
y = grd.variables["y"][:]
x = grd.variables["x"][:]
clat = grd.variables["y"][1:-1:2,1:-1:2]
clon = grd.variables["x"][1:-1:2,1:-1:2]
dims = clat.shape
print("dims = ", dims)
blat = np.zeros((dims[0]+2,dims[1]+2))
blon = np.zeros((dims[0]+2,dims[1]+2))
blat[1:-1,1:-1] = clat
blon[1:-1,1:-1] = clon
blat[1:-1,0] = y[1:-1:2,0]
blon[1:-1,0] = x[1:-1:2,0]
blat[1:-1,-1] = y[1:-1:2,-1]
blon[1:-1,-1] = x[1:-1:2,-1]
blat[0,1:-1] = y[0,1:-1:2]
blon[0,1:-1] = x[0,1:-1:2]
blat[-1,1:-1] = y[-1,1:-1:2]
blon[-1,1:-1] = x[-1,1:-1:2]
blat[0,0] = y[0,0]
blon[0,-1] = x[0,-1]
blat[-1,0] = y[-1,0]
blon[-1,-1] = x[-1,-1]

m = projmap.Projmap('arctic')
#m = Basemap(llcrnrlon=-121., llcrnrlat=17., urcrnrlon=-125.0, urcrnrlat=53.0,\
#            rsphere=(6378137.00,6356752.3142),\
#            resolution='h', projection='lcc',\
#            lat_0=30., lat_1=40.0, lon_0=-78.)
x, y = m(blon, blat)
levels = np.arange(-.6, 0.6, 0.01)
cmap = plt.cm.get_cmap("seismic")

for file in lst_file:
    print("Plotting "+file)
    nc = netCDF4.Dataset(file, "r")
    times = nc.variables["time"][:]
    ntimes = len(times)
    for it in range(ntimes):
        m = projmap.Projmap('arctic')
        fig = plt.figure(figsize=(8,9))
#       ax = fig.add_subplot(111)
#       ax.set_aspect('equal')
#       ax.axis(xmin=-300,xmax=300)
#       m.drawmapboundary(fill_color='0.3')
        m.drawcoastlines()
        m.drawmapboundary(fill_color='#99ffff')
        m.fillcontinents(color='0.3',lake_color='0.3')
        rv = nc.variables["RV"][it,0,:,:]
        rv *= 1.e4
        cs = m.pcolormesh(x, y, rv, vmin=-0.6, vmax=0.6, cmap=cmap)
#       cs = m.contourf(x, y, rv, levels=levels, cmap=cmap, extend='both')
#       cs = plt.contourf(clon, clat, rv, levels=levels, cmap=cmap, extend='both')
        plt.title('Surface RV')
#       csa = plt.contour(clon, clat, rv, levels=levels, linewidths=(0.5,))
        parallels = np.arange(45.,90.,15.)
        # labels = [left,right,top,bottom]
        m.drawparallels(parallels)
        meridians = np.arange(0.,360.,15.)
        m.drawmeridians(meridians,labels=[1, 0, 0, 1])

#       cbaxes = fig.add_axes([0.1, 0.05, 0.8, 0.02])
#       plt.colorbar(orientation='horizontal', cax=cbaxes)
        myday = jday2date(times[it]/24.)
        date_tag = myday.strftime('%d %B %Y')
        plt.title(date_tag, fontsize=20)
        fname = myday.strftime('movie_rv/frame_%(number)04d.png'%{'number': it})
        print(date_tag)
        cbar = plt.colorbar(cs, orientation='vertical')
        cbar.ax.tick_params(labelsize=15)

        plt.savefig(fname)
        plt.close()

    nc.close()
