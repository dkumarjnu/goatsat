#!/usr/bin/env python
#code for production of Q0
#written by Dr. D Kumar (email: d.kumar@reading.ac.uk)


import os
import glob
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature


import cartopy.io.shapereader as shpreader

fname = '/gws/nopw/j04/odanceo/dkumar/AFRICA_SHAPE/afr_g2014_2013_0.shp'

adm1_shapes = list(shpreader.Reader(fname).geometries())



base='/gws/nopw/j04/tamsat/public/tamsat_alert_forcing_data/subset/Africa/0.25/yearly_files/'
years=os.listdir(base)


for year in years:
    filepath=os.path.join(base + year+ '/')
    print(filepath)
    if len(os.listdir(filepath)) == 0:
       print("Directory is empty")
    else:
       print("Found the files: Estimating Q0")
       if os.path.isfile(filepath+'prate_tamsat_'+year+'_sub.v3.2.nc') == True:
          prname=filepath+'prate_tamsat_'+year+'_sub.v3.2.nc'
       else:
          prname=filepath+'prate_tamsat_'+year+'_sub.nc'
       print(prname)
       pr = xr.open_dataset(prname)['rfe']
       sw = xr.open_dataset(filepath+'dswrf.sub.'+year+'.nc')['dswrf']
       lw = xr.open_dataset(filepath+'dlwrf.sub.'+year+'.nc')['dlwrf']
       #converting W/m2 to Mj/m2: multiply by 0.0864
       Ra = (sw + lw)*0.0864
       Tmean = xr.open_dataset(filepath+'air.sub.'+year+'.nc')['air']-273.15
       #Instantaneous daily development rate of eggs to L3
       Delta = 0.09746 + 0.01063*Tmean
       #Instantaneous daily mortality rate of eggs
       mu_e =   xr.ufuncs.exp(-1.3484 - 0.10488*Tmean + 0.00230 * (Tmean)**2)
       #Instantaneous daily mortality rate of L3 in faeces
       mu_l3 = xr.ufuncs.exp(-2.62088 - 0.14399*Tmean + 0.00462 * (Tmean)**2)
       #Instantaneous daily mortality rate of L3 on pasture
       rho = mu_l3/3
       #Instantaneous daily L3 migration rate between faeces and pasture
       m1 = np.full((len(pr['time']), len(pr['latitude']), len(pr['longitude'])), 0.25)
       #Proportion of total pasture L3 that are found on herbage
       m2 = np.full((len(pr['time']), len(pr['latitude']), len(pr['longitude'])), 0.2)
       #Probability of establishment of ingested L3
       p = np.full((len(pr['time']), len(pr['latitude']), len(pr['longitude'])), 0.4)
       #Instantaneous daily mortality rate of adult nematodes
       mu = np.full((len(pr['time']), len(pr['latitude']), len(pr['longitude'])), 0.05)
       #Fecundity (eggs/day/ adult)
       lamda = np.full((len(pr['time']), len(pr['latitude']), len(pr['longitude'])), 2250)
       #H = xr.open_dataset('/gws/nopw/j04/odanceo/dkumar/DATAVERSE/AFRICA/remapbil_Africa_6_Gt_2010_Aw.tif.nc')['Band1']
       #H1=np.repeat(H.values[np.newaxis, :, :], len(pr['time']), axis=0)
       H1 = np.ones((len(pr['time']), len(pr['latitude']), len(pr['longitude'])))
       #convert to degC
       Tmax = xr.open_dataset(filepath+'tmax.sub.'+year+'.nc')['tmax']-273.15
       Tmin = xr.open_dataset(filepath+'tmin.sub.'+year+'.nc')['tmin']-273.15
       E = 0.0023 * 0.408 * Ra * ((Tmax + Tmin)/2 + 17.8) * xr.ufuncs.sqrt(Tmax-Tmin)
       pre=np.zeros((len(pr['time']), len(pr['latitude']), len(pr['longitude'])))
       for i in range(len(pr['time'])):
           if i >= 4 and i <= 360:
              #print(str(i-4)+' to '+str(i+5))
              pre[i] = pr[i-4:i+5].mean('time').values
           else:
              pre[i] = pr[i]
       evap = np.zeros((len(E['time']), len(E['latitude']), len(E['longitude'])))
       for i in range(len(E['time'])):
           if i >= 4 and i <= 360:
              #print(str(i-4)+' to '+str(i+5))
              evap[i] = E[i-4:i+5].mean('time').values
           else:
              evap[i] = E[i]
       num_timestep=min(pr['time'].shape, E['time'].shape)[0]
       print(num_timestep)
       p_by_e = pre[:num_timestep, :, :]/evap[:num_timestep, :, :]
       #grazing area, ha= 1
       A = np.ones((len(pr['time']), len(pr['latitude']), len(pr['longitude'])))    
       #standing biomass, (kg DM/ha)
       B = np.full((len(pr['time']), len(pr['latitude']), len(pr['longitude'])), 2000)
       #Daily herbage dry matter intake per host (kg DM/day)
       c = np.full((len(pr['time']), len(pr['latitude']), len(pr['longitude'])), 1.4)
       #rate of ingestion of L3 on pasture
       beta = c/B*A
       q = (Delta[:num_timestep, :, :] * m1[:num_timestep, :, :])/(mu_e[:num_timestep, :, :] + Delta[:num_timestep, :, :])*(mu_l3[:num_timestep, :, :] + m1[:num_timestep, :, :])
       masked_array=np.where(p_by_e >= 1, q, 0)
       q.values=masked_array
       Q0 = ((q[:num_timestep, :, :] * lamda[:num_timestep, :, :])/mu[:num_timestep, :, :]) * ((beta[:num_timestep, :, :] * p[:num_timestep, :, :])/(rho[:num_timestep, :, :] + beta[:num_timestep, :, :] * H1[:num_timestep, :, :])) * H1[:num_timestep, :, :]* m2[:num_timestep, :, :]
       Q0=Q0.rename("Q0")
       Q0.to_netcdf('/gws/nopw/j04/odanceo/dkumar/Q0/output_without_population/'+year+'.nc')
       print("Save Output of Q0 for "+ year)
