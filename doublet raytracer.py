# -*- coding: utf-8 -*-
"""
The following program traces a ray of light through a doublet lens in air using the paraxial approximation model. The user defines 
height of the image at the first surface of the doublet lens, as well as the slope at which the the ray is incident on the first 
surface. To get an idea of the how the surfaces in a doublet are laid out, please see the following website:
https://en.wikipedia.org/wiki/Doublet_(lens)
    
To run this code, download the Anaconda Python distribution, and copy this code in the Syder editor. No external libraries 
need to be imported (as of October 2017).
"""
import numpy as np
import math
import matplotlib.pyplot as plt 

# Set initial parameters for the doublet. Remember to keep the distance units consistent.
r1 = float(input('Enter the radius of the first surface: ')) # mm
r2 = float(input('Enter the radius of the second surface: ')) # mm
r3 = float(input('Enter the radius of the third surface: ')) # mm
t1 = float(input('Enter the thickness from the first to the second surface: ')) # mm
t2 = float(input('Enter the thickness from the second to the third surface: ')) # mm
n1 = float(input('Enter the index of refraction from the first to the second surface: '))
n2 = float(input('Enter the index of refraction from the second to the third surface: '))
nair = 1 # refractive index of air. Should be changed if doublet is in a medium other than air

# Caluclates curvature of each surface from the user defined radius
c1 = 1/r1
c2 = 1/r2
c3 = 1/r3

# Calculates power of each surface. Assumes the doublet lens is in air
p1 = (n1 - nair)*c1
p2 = (n2 - n1)*c2
p3 = (nair - n2)*c3

# Calculates the reduced thicknesses of the two parts of the doublet lens, each of which has a different index of refraction
tau1 = t1/n1
tau2 = t2/n2

# Asks for user input regarding the height and entrance angle of the ray to be traced
y0 = float(input('Enter the height of the ray of light at the first surface: '))
w0 = float(input('Enter the slope at which the light ray is incident of the first surface: ')) # slope can be positive or negative 

# Ray tracing physics engine (paraxial approximation)

w1 = w0 - (y0*p1) # Ray refracts, but does not change height at surface 1
y1 = y0 + (w1*tau1) # New height at surface 2. Ray changes height, but does not change direction while propagating between surface 1 
# and 2
w2 = w1 - (y1*p2) # Ray refracts, but does not change height at surface 2
y2 = y1 + (w2*tau2) # New height at surface 3. Ray changes height, but does not change direction while propagating between surface 2 
# and 3
w3 = w2 - (y2*p3) # Ray refracts, but does not change height at surface 3
t3 = -(y2/w3)*nair # Distance after surface 3 that the ray crosses the optical axis (assumes lens is in air)

# Print outputs
print("Image height at surface 1 is: ", y0, " mm")
print("Ray slope just after surface 1 is: ", w1, " degrees")
print("Image height at surface 2 is: ", y1, " mm")
print("Ray slope just after surface 2 is: ", w2, " degrees")
print("Image height at surface 3 is: ", y2, " mm")
print("Ray slope just after surface 3 is: ", w3, " degrees")
print("Distance after surface 3 that the light ray crosses the optical axis: ", t3, " mm")







