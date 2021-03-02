import numpy as np
import netCDF4
import os
import sys
import subprocess
import pyroms
from pyroms_toolbox import jday2date
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
lst = subprocess.getoutput('ls 20120102.ocean_daily.nc')
lst = lst.split()
lst_file = lst_file + lst

#grd = netCDF4.Dataset('sea_ice_geometry.nc', "r")
#clat = grd.variables["geolatb"][:]
#clon = grd.variables["geolonb"][:]
grd = netCDF4.Dataset('/import/c1/AKWATERS/kate/ESMG/ESMG-configs/Bering/INPUT/ocean_hgrid.nc', "r")
y = grd.variables["y"][:]
x = grd.variables["x"][:]
clat = grd.variables["y"][1:-1:2,1:-1:2]
clon = grd.variables["x"][1:-1:2,1:-1:2]
blat = grd.variables["y"][::2,::2]
blon = grd.variables["x"][::2,::2]
dims = clat.shape
#print("dims = ", dims)
#blat = np.zeros((dims[0]+1,dims[1]+1))
#blon = np.zeros((dims[0]+1,dims[1]+1))
#blat[1:-1,1:-1] = clat
#blon[1:-1,1:-1] = clon
#blat[1:-1,0] = y[1:-1:2,0]
#blon[1:-1,0] = x[1:-1:2,0]
#blat[1:-1,-1] = y[1:-1:2,-1]
#blon[1:-1,-1] = x[1:-1:2,-1]
#blat[0,1:-1] = y[0,1:-1:2]
#blon[0,1:-1] = x[0,1:-1:2]
#blat[-1,1:-1] = y[-1,1:-1:2]
#blon[-1,1:-1] = x[-1,1:-1:2]
#blat[0,0] = y[0,0]
#blon[0,-1] = x[0,-1]
#blat[-1,0] = y[-1,0]
#blon[-1,-1] = x[-1,-1]

m = Basemap(projection='lcc', lat_1=60, lat_2=60, lon_0=260, \
llcrnrlon=194.25, llcrnrlat=44, urcrnrlon=160.8, urcrnrlat=74.0, \
resolution='h')
#m = Basemap(projection='stere', lat_0=90, lon_0=180, llcrnrlon=-210,
#    llcrnrlat=40, urcrnrlon=-50, urcrnrlat=50, resolution='h')
#m = Basemap(llcrnrlon=-121., llcrnrlat=17., urcrnrlon=-125.0, urcrnrlat=53.0,\
#            rsphere=(6378137.00,6356752.3142),\
#            resolution='h', projection='lcc',\
#            lat_0=30., lat_1=40.0, lon_0=-78.)
#x, y = m(blon, blat)
x, y = m(clon, clat)
#levels = np.arange(.0, 0.0010, 0.0005)
levels = np.arange(.0, 0.0010, 0.0005)
cmap = plt.cm.get_cmap("Set1")

for file in lst_file:
    print("Plotting "+file)
    nc = netCDF4.Dataset(file, "r")
    times = nc.variables["time"][:]
    ntimes = len(times)
    for it in range(ntimes):
        m = Basemap(projection='lcc', lat_1=60, lat_2=60, lon_0=260, \
                llcrnrlon=194.25, llcrnrlat=44, urcrnrlon=160.8, urcrnrlat=74.0, \
                resolution='h')
        fig = plt.figure(figsize=(8,9))
#       ax = fig.add_subplot(111)
#       ax.set_aspect('equal')
#       ax.axis(xmin=-300,xmax=300)
#       m.drawmapboundary(fill_color='0.3')
        m.drawcoastlines()
        m.drawmapboundary(fill_color='#99ffff')
        m.fillcontinents(color='0.3',lake_color='0.3')
        u = nc.variables["uice"][it,:,:]
        v = nc.variables["vice"][it,:,:]
        ut = 0.5*(u[:,:-1] + u[:,1:])
        vt = 0.5*(v[:-1,:] + v[1:,:])
        speed = np.sqrt(ut**2 + vt**2)
        print('speed', speed[184,172], speed[122,210])
        print('speed u', u[184,172], u[122,210])
        print('speed v', v[184,172], v[122,210])
#       cs = m.pcolormesh(x, y, speed, vmin=0.0005, vmax=0.0005, cmap=cmap)
        cs = m.contourf(x, y, speed, levels=levels, cmap=cmap, extend='both')
#       cs = plt.contourf(clon, clat, speed, levels=levels, cmap=cmap, extend='both')
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
        fname = myday.strftime('movie_ispeed/frame_%(number)04d.png'%{'number': it})
        print(date_tag)
        cbar = plt.colorbar(cs, orientation='vertical')
        cbar.ax.tick_params(labelsize=15)

        plt.savefig(fname)
        plt.close()

    nc.close()
