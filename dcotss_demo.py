#+
# Name:
#		DCOTSS Python Module
# Purpose:
#		This module reads a single DCOTSS 1-s merge file and creates several plots of the data.
#       The flight used is the 29 July 2021 DCOTSS flight, which sampled a large volume of
#       water vapor enhancement from recent tropopause-overshooting convection. The final
#       DCOTSS data from this flight is publicly available at https://asdc.larc.nasa.gov/project/DCOTSS.
# Author and history:
#		Cameron R. Homeyer  2022-12-05.
# Warning:
#		The authors' primary coding language is not Python. This code works, but may not be
#       the most efficient or proper approach. Please suggest improvements by sending an email
#		to chomeyer@ou.edu.
#-

# Import python libraries
import sys
import os
import numpy as np
import netCDF4
import matplotlib.pyplot as plt

from netCDF4 import Dataset

# Location of DCOTSS data file
infile = 'DCOTSS-MERGE-1S_MERGE_20210729_R2.nc'

# Open DCOTSS file
id = Dataset(infile, "r", format="NETCDF4")

# Read variables
x = id.variables['G_LONG_MMS']
y = id.variables['G_LAT_MMS']
z = id.variables['G_ALT_MMS']
t = id.variables['epoch_time']
theta = id.variables['POT_MMS']
trop = id.variables['Z_trop_ERA5']
h2o = id.variables['HHH_H2O']
o3 = id.variables['O3_ROZE']


# Simple time plot of ER-2 and ERA5 tropopause altitude
time_plot = (t[:]-t[0])/3600.0
altitude_plot = 0.001*z[:]
trop_plot = 0.001*trop[:]

plt.plot(time_plot,trop_plot,color='orange',label="ERA5 Tropopause")
plt.plot(time_plot,altitude_plot,color='black',label="MMS GPS Alt")
plt.xlabel('Flight Time (hr)')
plt.ylabel('Altitude (km)')
plt.title('DCOTSS 29 July 2021 Flight')
plt.legend(loc="lower center")
plt.show()


# 3D flight plot
xplot = x[:]+360.0
yplot = y[:]
ax = plt.figure().add_subplot(projection='3d')
ax.plot(xplot[xplot >= 0],yplot[xplot >= 0],altitude_plot[xplot >= 0])
ax.set_xlabel('Longitude (deg E)')
ax.set_ylabel('Latitude (deg N)')
ax.set_zlabel('Altitude (km)')
ax.set_title('DCOTSS 29 July 2021 Flight')
plt.show()


# H2O & O3 timeseries plot
h2o_plot = h2o[:]
o3_plot = o3[:]

fig, ax = plt.subplots()
ax.plot(time_plot,h2o_plot,color="blue")
ax.set_xlabel('Flight Time (hr)')
ax.set_ylabel('HHH H2O (ppmv)',color='blue')
plt.semilogy()
plt.ylim(1.0,1000.0)
plt.title('DCOTSS 29 July 2021 Flight')
#add second axis & plot
ax2=ax.twinx()
ax2.plot(time_plot,o3_plot,color="red")
ax2.set_ylabel("ROZE O3 (ppbv)",color="red")
plt.semilogy()
plt.ylim(10.0,10000.0)
plt.show()


# H2O potential temperature plot
theta_plot = theta[:]
plt.scatter(h2o_plot,theta_plot,s=0.75,color='blue')
plt.xlabel('HHH H2O (ppmv)')
plt.ylabel('MMS Pot. Temp. (K)')
plt.semilogx()
plt.xlim(1.0,1000.0)
plt.title('DCOTSS 29 July 2021 Flight')
plt.show()


# O3-H2O tracer-tracer plot
plt.scatter(h2o_plot,o3_plot,s=0.75,c=np.minimum(np.maximum(theta_plot,350.0),450.0),cmap=plt.cm.viridis)
plt.xlabel('HHH H2O (ppmv)')
plt.ylabel('ROZE O3 (ppbv)')
plt.semilogx()
plt.xlim(1.0,1000.0)
plt.ylim(0.0,800.0)
plt.title('DCOTSS 29 July 2021 Flight')
plt.colorbar(location='right',label='MMS Pot. Temp. (K)',extend='both',ticks=(350,370,390,410,430,450))
plt.show()


# Close netCDF4 file
id.close()
