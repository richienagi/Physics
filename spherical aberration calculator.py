# -*- coding: utf-8 -*-
"""
The following program traces a ray of light through an optical system in air using the paraxial approximation model. The user defines 
height of the image at the first lens surface, as well as the slope at which the the ray is incident on the first surface. The program 
calculates the speherical aberration introduced by each surface in the system, as well as the total spherical aberration of the 
given optical system configaration.
    
To run this code, download the Anaconda Python distribution, and copy this code in the Syder editor. No external
libraries need to be imported (as of October 2017).
"""
import numpy as np
import math
import matplotlib.pyplot as plt 

# Notes: For planar surfaces, set the radius of curvature to a extremely large number (> positive or negative 500000).
# All distances are in mm, unless otherwise noted.

# Set initial parameters for the optical system. Remember to keep the distance units consistent.
nair = 1 # Assumes the optical system is in air. Any free sepcae between lenses has arefarctive index of 1.
surfaces = int(input('Enter the number of lens surfaces in the system: ')) # For example, an equiconvex lens has two surfaces
radiusArray = np.zeros((surfaces,1)) # defines array to store radii of user defined surfaces
thicknessArray = np.zeros((surfaces,1)) # defines array to store user defined thicknesses between surfaces
indexArray = np.zeros((surfaces,1)) # defines array to store user defined index of refraction data 
curvatureArray = np.zeros((len(radiusArray),1)) # array to store curvature of each surface
surfacePowerArray = np.zeros((len(radiusArray),1)) # array to store power of each surface
reducedThicknessArray = np.zeros((len(thicknessArray),1)) # array to store reduced thicknesses (t/n)
sphericalaberrationArray = np.zeros((surfaces,1)) # array to store spherical aberration introduced at each surface

for istep in range(0,surfaces):
    radiusArray[istep] = float(input('Enter the radius of surface ' + str(istep+1) + ' (mm): '))  # mm

for istep in range(0,surfaces-1):
    thicknessArray[istep] = float(input('Enter the thickness from surface ' + str(istep+1) + ' to surface ' + str(istep+2) + ' (mm): '))  # mm
thicknessArray = np.trim_zeros(thicknessArray,'b')

for istep in range(0,surfaces-1):
    indexArray[istep] = float(input('Enter the index from surface ' + str(istep+1) + ' to surface ' + str(istep+2) + ': ')) # mm
indexArray = np.trim_zeros(indexArray,'b')

# Calculates curvature of each surface from the user defined radius
for istep in range(0,len(radiusArray)):
    curvatureArray[istep] = 1/radiusArray[istep]

# Calculates power of each surface. Assumes the optical system is in air
for istep in range(0,len(radiusArray)):
    if istep == 0:
        surfacePowerArray[istep] = (indexArray[istep] - nair)*curvatureArray[istep]
    elif istep == (len(indexArray)):
        surfacePowerArray[istep] = (nair - indexArray[istep-1])*curvatureArray[istep]
    else:
        surfacePowerArray[istep] = (indexArray[istep] - indexArray[istep-1])*curvatureArray[istep]

# Calculates reduced thicknees (t/n)       
for istep in range(0,len(thicknessArray)):
    reducedThicknessArray[istep] = thicknessArray[istep]/indexArray[istep]

rayHeightArray = np.zeros((len(radiusArray),1)) # defines array to store ray height at each surface
slopeArray = np.zeros((len(radiusArray),1)) # defines array to store slope of ray incidence at each surface

# Asks for user input regarding the height and slope of the incident ray on the first surface of the optical system
rayHeightArray[0] = float(input('Enter the height of the ray of light at the first surface (mm): '))
w0 = float(input('Enter the slope at which the light ray is incident of the first surface: ')) # slope can be positive or negative
objectDistance = float(input('Enter the distance of the object from the first surface (mm): '))

# Ray tracing physics engine (paraxial approximation)  
for istep in range(0,len(radiusArray)):
    if istep == 0:
        rayHeightArray[istep] = rayHeightArray[istep] # Height of ray on the first surface, as defined by the user
        slopeArray[istep] = w0 - (rayHeightArray[istep]*surfacePowerArray[istep])
    else:
        rayHeightArray[istep] = rayHeightArray[istep-1] + (slopeArray[istep-1]*reducedThicknessArray[istep-1])
        slopeArray[istep] = slopeArray[istep-1] - (rayHeightArray[istep]*surfacePowerArray[istep-1])

# Calculates spherical aberration introduced at each surface. Assumes medium before the first surface and after the last surface
# is air. To simulate other medium, replace the 1 in the below for loop with the desired refractive medium 
for istep in range(0,len(radiusArray)):
    if istep == 0:
        incidenceAngle = math.atan(rayHeightArray[istep]/objectDistance) + math.asin(rayHeightArray[istep]/radiusArray[istep])
        sphericalaberrationArray[istep] = rayHeightArray[istep]*1*((1/indexArray[istep]) - 1)*((slopeArray[istep]/indexArray[istep]) + incidenceAngle)*math.pow(incidenceAngle,2)
    elif istep == len(radiusArray)-1:
        sphericalaberrationArray[istep] = rayHeightArray[istep]*indexArray[istep-1]*((indexArray[istep-1]/1)-1)*(slopeArray[istep] + (slopeArray[istep-1]/indexArray[istep-1]))*math.pow(slopeArray[istep-1]/indexArray[istep-1],2)
    else:
        sphericalaberrationArray[istep] = rayHeightArray[istep]*indexArray[istep-1]*((indexArray[istep-1]/indexArray[istep])-1)*(slopeArray[istep] + (slopeArray[istep-1]/indexArray[istep-1]))*math.pow(slopeArray[istep-1]/indexArray[istep-1],2)

# Print outputs (ray height and slope immediatelt after interation with every user defined surface in the system)
for istep in range(0,len(rayHeightArray)):
    print("Image height at surface ",istep+1, " is ", rayHeightArray[istep], " mm")
    print("Slope of light ray at surface ",istep+1, " is ",slopeArray[istep])

totalsphericalAberration = 0 #Initialize varialbe for storing sum of spherical aberration contributed by each surface
for istep in range(0,len(sphericalaberrationArray)):
    totalsphericalAberration = totalsphericalAberration + sphericalaberrationArray[istep]
    print("The spherical aberration contributed by surface ",istep+1, " is ",sphericalaberrationArray[istep])
    
print("The total spherical aberration of the system is " ,totalsphericalAberration)

# Calculates where/if the light ray crosses the optical axis after the last user defined surface
axisCross = -rayHeightArray[len(rayHeightArray)-1]/slopeArray[len(slopeArray)-1]
print("The light ray crosses the optical axis at a distance of ",axisCross, " mm after the last surface in the optical system")

