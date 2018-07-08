"""
The following program calculates the spectral radiance emitted by a black body, for a user defined wavelength
and temperature.

To run this code, download the Anaconda Python distribution, and copy this code in the Syder editor. No external
libraries need to be imported (as of July 2018).
"""

import math

#Parameters to calculate spectral radiance
c1 = 3.74e-16 # Wm^2 (first radiation constant)
c2 = 1.44e-2 # m-K (second radiation constant)
n = 1.0028 # index of refraction, assumes air

# User inputs
wavelength = float(input('Enter the wavelength at which you want to calculate the spectral radiance (in microns):'))
temperature = float(input('Enter the temperature at which you want to calculate the spectral radiance (in Kelvin):'))

#Spectral radiance calculation
wavelengthMeters = wavelength*1e-6 #Covert wavelength from microns to meters
spectralRadiance = (c1/(math.pi*math.pow(n,2)*math.pow(wavelengthMeters,5)))*(1/((math.exp(c2/(n*wavelengthMeters*temperature)))-1))

#Print output
print("The Spectral Radiance is ",spectralRadiance," W/(m^2-sr-m)")