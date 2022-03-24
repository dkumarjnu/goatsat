#!/bin/sh


rm -rf /gws/nopw/j04/odanceo/public/goatsat/q0/nc/*txt
#daily filelist for netcdf
for i in /gws/nopw/j04/odanceo/public/goatsat/q0/nc/*_daily.nc; do   echo `realpath $i` >> /gws/nopw/j04/odanceo/public/goatsat/q0/nc/daily_nc_filelist.txt; done

#weekly filelist for netcdf
for i in /gws/nopw/j04/odanceo/public/goatsat/q0/nc/*_5day.nc; do   echo `realpath $i` >> /gws/nopw/j04/odanceo/public/goatsat/q0/nc/fiveday_nc_filelist.txt; done
