#!/usr/bin/env python
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
import os
import cartopy as cart


fname = '/gws/nopw/j04/odanceo/dkumar/AFRICA_SHAPE/afr_g2014_2013_0.shp'

adm1_shapes = list(shpreader.Reader(fname).geometries())


yaxis=[-35, -25, -15, -7, 0, 7, 15, 25,35]
ylab=['35\N{DEGREE SIGN}S','25\N{DEGREE SIGN}S','15\N{DEGREE SIGN}S','7\N{DEGREE SIGN}S','EQ','7\N{DEGREE SIGN}N','15\N{DEGREE SIGN}N', '25\N{DEGREE SIGN}N', '35\N{DEGREE SIGN}N']

xaxis=[-18,  -8,   2,  12,  22,  32,  42,  52]
xlab=['18\N{DEGREE SIGN}W', '8\N{DEGREE SIGN}W','2\N{DEGREE SIGN}E','12\N{DEGREE SIGN}E','22\N{DEGREE SIGN}E', '32\N{DEGREE SIGN}E', '42\N{DEGREE SIGN}E', '52\N{DEGREE SIGN}E']



base='/gws/nopw/j04/odanceo/public/goatsat/q0/'
years=os.listdir(base+'nc/')
#problem likely due to the presence of txt file in the directory so skipping the first and seconda entries: these are file list in text

for year in years[2:]:
    filepath=os.path.join(base + 'nc/'+ year)
    filename=year
    pngname=base+'png/'+ year[:-3]+'.png'
    if os.path.isfile(pngname) == False:
       Q0=xr.open_dataset(filepath)['Q0']
       #print(str(Q0['time'])[36:46])
       fig = plt.figure(figsize=(18, 14))
       ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
       plot=ax.contourf(Q0['longitude'], Q0['latitude'], Q0, np.arange(1, 21, 1), cmap='plasma_r', extend='max')
       ax.add_geometries(adm1_shapes, ccrs.PlateCarree(),
                      edgecolor='black', facecolor='None', alpha=0.15)
       ax.add_feature(cart.feature.OCEAN, zorder=1, edgecolor='k', facecolor='white')
       ax.set_title('Date='+str(Q0['time'])[36:46], fontsize=24)
       ax.set_yticks(yaxis)
       ax.set_yticklabels(ylab, minor=False, fontsize=24)
       ax.set_xticks(xaxis)
       ax.set_xticklabels(xlab, minor=False, fontsize=24)
       ax.grid(color='k', linestyle='--', alpha=0.14)
       cbar_ax = fig.add_axes([0.84, 0.12, 0.025, 0.76])
       col=fig.colorbar(plot, cax=cbar_ax, orientation='vertical')
       col.set_label(u'Q\u2080', rotation=90, fontsize=24)   #H2O2= print(u'H\u2082O\u2082')
       for t in col.ax.get_yticklabels():
           t.set_fontsize(24)
       ax.coastlines()
       plt.savefig(pngname)
       plt.close()
       print('created image file for '+ str(Q0['time'])[36:46])
    else:
       print('file already exists')


'''
####weekly dump
base='/gws/nopw/j04/odanceo/public/goatsat/q0/output/weekly/'
years=os.listdir(base)


for year in years:
    filepath=os.path.join(base + year)
    filename=year
    pngname=year[:-3]
    Q0=xr.open_dataset(filepath)['Q0']
    #print(str(Q0['time'])[36:46])
    fig = plt.figure(figsize=(18, 14))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    plot=ax.contourf(Q0['longitude'], Q0['latitude'], Q0, np.arange(1, 21, 1), cmap='plasma_r', extend='max')
    ax.add_geometries(adm1_shapes, ccrs.PlateCarree(),
                  edgecolor='black', facecolor='None', alpha=0.15)
    ax.set_title('Date='+str(Q0['time'])[36:46], fontsize=24)
    ax.set_yticks(yaxis)
    ax.set_yticklabels(ylab, minor=False, fontsize=24)
    ax.set_xticks(xaxis)
    ax.set_xticklabels(xlab, minor=False, fontsize=24)
    ax.grid(color='k', linestyle='--', alpha=0.14)
    cbar_ax = fig.add_axes([0.84, 0.12, 0.025, 0.76])
    col=fig.colorbar(plot, cax=cbar_ax, orientation='vertical')
    col.set_label(u'Q\u2080', rotation=90, fontsize=24)   #H2O2= print(u'H\u2082O\u2082')
    for t in col.ax.get_yticklabels():
        t.set_fontsize(24)
    ax.coastlines()
    plt.savefig('/gws/nopw/j04/odanceo/public/goatsat/q0/png/weekly/'+pngname+'.png')
    plt.close()
    print('created file for '+ str(Q0['time'])[36:46])
'''
