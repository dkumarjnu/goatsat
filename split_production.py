#!/usr/bin/env python
import os
import xarray as xr
import numpy as np

base='/gws/nopw/j04/odanceo/dkumar/Q0/output_without_population/'
years=os.listdir(base)



#splitting into daily timesteps

for i in years:
    f=xr.open_dataset(base+str(i))['Q0']
    for i in range(len(f.time)):
        date=str(f['time'][i])[36:46]
        #replacing hyphen from the actual date for nomenclature
        date= date.replace('-','')
        data=f[i]
        data=data.rename('Q0')
        filename="/gws/nopw/j04/odanceo/public/goatsat/q0/nc/q0_nceo_v1p0p0_"+date+"_daily.nc"
        if os.path.isfile(filename) == False:
           data.to_netcdf(filename)
           print("saved data for: "+date)
        else:
           print("file already exists")




#splitting in to pentad files
#removing the 31st date from each month in order to avoid their inclusion

for i in years:
    f=xr.open_dataset(base+str(i))['Q0']
    f=f.groupby('time.month')
    for j in range(len(f)):
        if len(f[j+1]['time'])==31:
           f1=f[j+1][:-1, :, :]
        else:
           f1=f[j+1]
        f1=f1.resample(time='5D').mean('time')
        for k in range(len(f1.time)):
            date=str(f1['time'][k])[36:46]
            date= date.replace('-','')
            data=f1[k]
            filename="/gws/nopw/j04/odanceo/public/goatsat/q0/nc/q0_nceo_v1p0p0_"+date+"_5day.nc"
            if os.path.isfile(filename) == False:
               data.to_netcdf(filename)
               print("saved weekly data for the date: "+date)
            else:
               print("file already exists")


#using capabilities of shell to prepare filelist from the python code itself

#filelist for netcdf
#os.system("for i in /gws/nopw/j04/odanceo/public/goatsat/q0/nc/*_daily.nc; do   echo `realpath $i` >> /gws/nopw/j04/odanceo/public/goatsat/q0/nc/daily_nc_filelist.txt; done")
#os.system("for i in /gws/nopw/j04/odanceo/public/goatsat/q0/nc/*_5day.nc; do   echo `realpath $i` >> /gws/nopw/j04/odanceo/public/goatsat/q0/nc/fiveday_nc_filelist.txt; done")

