# -*- coding: utf-8 -*-
"""
The following program traces the chief and marginal rays through an optical system in air using the paraxial approximation model. 
The user defines height of the marginal ray at the first lens surface, as well as the distance of the object from the first surface. 
The program calculates the coma introduced by each surface in the system, as well as the total coma of the given optical system 
configuration. 

Notes: 
- The program assumes that the aperture stop is located at the first lens surface.
- To simulate a planar surfaces, use a large (>500000) radius of curvature.

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
comaArray = np.zeros((surfaces,1)) # array to store the coma introduced at each surface

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

rayHeightArray = np.zeros((len(radiusArray),1)) # defines array to store ray height at each surface for marginal ray
slopeArray = np.zeros((len(radiusArray),1)) # defines array to store slope of ray incidence at each surface for marginal ray
rayHeightArrayC = np.zeros((len(radiusArray),1)) # defines array to store ray height at each surface for chief ray
slopeArrayC = np.zeros((len(radiusArray),1)) # defines array to store slope of ray incidence at each surface for chief ray


# Asks for user input regarding the height and the distance of the object from the first surface of the optical system
rayHeightArray[0] = float(input('Enter the height of the marginal ray at the first surface (mm): '))
objectDistance = float(input('Enter the distance of the object from the first surface (mm): '))

# Ray tracing physics engine for marginal ray (paraxial approximation) 
w0 = rayHeightArray[0]/objectDistance 
for istep in range(0,len(radiusArray)):
    if istep == 0:
        rayHeightArray[istep] = rayHeightArray[istep] # Height of ray on the first surface, as defined by the user
        slopeArray[istep] = w0 - (rayHeightArray[istep]*surfacePowerArray[istep])
    else:
        rayHeightArray[istep] = rayHeightArray[istep-1] + (slopeArray[istep-1]*reducedThicknessArray[istep-1])
        slopeArray[istep] = slopeArray[istep-1] - (rayHeightArray[istep]*surfacePowerArray[istep-1])

# Ray tracing physics engine for chief ray (paraxial approximation) 
w1 = -rayHeightArray[0]/objectDistance 
rayHeightArrayC[0] = 0
for istep in range(0,len(radiusArray)):
    if istep == 0:
        rayHeightArrayC[istep] = rayHeightArrayC[istep] # Height of ray on the first surface, as defined by the user
        slopeArrayC[istep] = w1 - (rayHeightArrayC[istep]*surfacePowerArray[istep])
    else:
        rayHeightArrayC[istep] = rayHeightArrayC[istep-1] + (slopeArrayC[istep-1]*reducedThicknessArray[istep-1])
        slopeArrayC[istep] = slopeArrayC[istep-1] - (rayHeightArrayC[istep]*surfacePowerArray[istep-1])

# Calculates spherical aberration introduced at each surface. Assumes medium before the first surface and after the last surface
# is air.  
for istep in range(0,len(radiusArray)):
    if istep == 0:
        incidenceAngle = math.atan(rayHeightArray[istep]/objectDistance) + math.asin(rayHeightArray[istep]/radiusArray[istep])
        sphericalaberrationArray[istep] = rayHeightArray[istep]*1*((1/indexArray[istep]) - 1)*((slopeArray[istep]/indexArray[istep]) + incidenceAngle)*math.pow(incidenceAngle,2)
    elif istep == len(radiusArray)-1:
        sphericalaberrationArray[istep] = rayHeightArray[istep]*indexArray[istep-1]*((indexArray[istep-1]/1)-1)*(slopeArray[istep] + (slopeArray[istep-1]/indexArray[istep-1]))*math.pow(slopeArray[istep-1]/indexArray[istep-1],2)
    else:
        sphericalaberrationArray[istep] = rayHeightArray[istep]*indexArray[istep-1]*((indexArray[istep-1]/indexArray[istep])-1)*(slopeArray[istep] + (slopeArray[istep-1]/indexArray[istep-1]))*math.pow(slopeArray[istep-1]/indexArray[istep-1],2)

# Calculates the coma introduced at each surface. Assumes medium before the first surface and after the last surface is air.
for istep in range(0,len(radiusArray)):
    if istep == 0:
        comaArray[istep] = (slopeArrayC[istep]/incidenceAngle)*sphericalaberrationArray[istep]
    else:
        comaArray[istep] = (slopeArrayC[istep-1]/indexArray[istep-1])/(slopeArray[istep-1]/indexArray[istep-1])*sphericalaberrationArray[istep]
            

# Print outputs (ray height and slope immediately after interaction with every user defined surface in the system)
for istep in range(0,len(rayHeightArray)):
    print("Image height at surface ",istep+1, " is ", rayHeightArray[istep], " mm")
    print("Slope of light ray at surface ",istep+1, " is ",slopeArray[istep])

totalComa = 0 #Initialize varialbe for storing sum of coma aberration contributed by each surface
for istep in range(0,len(comaArray)):
    totalComa = totalComa + comaArray[istep]
    print("The coma contributed by surface ",istep+1, " is ",comaArray[istep])
    
print("The total coma of the system is " ,totalComa)

# Calculates where/if the light ray crosses the optical axis after the last user defined surface
axisCross = -rayHeightArray[len(rayHeightArray)-1]/slopeArray[len(slopeArray)-1]
print("The light ray crosses the optical axis at a distance of ",axisCross, " mm after the last surface in the optical system")

