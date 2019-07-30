"""
Kepler Data Analysis. The following program calculates the period of the transit from the light flux versus 
time data from the Kepler Input Catalogue
"""
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal

#Please download the tbl file from the GitHub repository. More data can be obtained from 
#http://exoplanetarchive.ipac.caltech.edu
#https://www.qmul.ac.uk/spa/outreach/in-school/school-activities/research-in-schools/our-projects/planet-hunting-with-python/
file = open('KIC006922244.tbl') 

time = []
flux = []
timeFloat = []
fluxFloat = []

for line in file:
    line = line.rstrip()
    line = line.split()
    time.append(line[1])
    flux.append(line[2])
    
file.close()
for item in time[3:]:
    timeFloat.append(float(item))

for item in flux[3:]:
    fluxFloat.append(np.abs(float(item)))

peaks,_ = scipy.signal.find_peaks(fluxFloat,height=0.004) #Peak detection

plt.figure(1)
plt.plot(timeFloat,fluxFloat)
plt.xlabel('Time (Julian Days)')
plt.ylabel('Relative Flux')
plt.xlim(1500,1590)
periodArray = []

for i in range(0,len(peaks)-1):
    periodArray.append(timeFloat[peaks[i+1]]-timeFloat[peaks[i]])

transitPeriod = sum(periodArray)/len(periodArray)
    