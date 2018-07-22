# -*- coding: utf-8 -*-
"""
The following program calculates the radiance emitted by a black body, for a user defined wavelength
range and temperature.

To run this code, download the Anaconda Python distribution, and copy this code in the Syder editor. No external
libraries need to be imported (as of July 2018).
"""

import math
from scipy.integrate import quad

#Parameters to calculate spectral radiance
c1 = 3.74e-16 # Wm^2 (first radiation constant)
c2 = 1.44e-2 # m-K (second radiation constant)
n = 1.0028 # index of refraction, assumes air

# User inputs
wavelengthStart  = float(input('Enter the start wavelength of the band over which you want to calculate the radiance (in microns):'))
wavelengthEnd  = float(input('Enter the end wavelength of the band over which you want to calculate the radiance (in microns):'))
temperature = float(input('Enter the temperature at which you want to calculate the spectral radiance (in Kelvin):'))

wavelengthStartMeters = wavelengthStart*1e-6 #Covert wavelength from microns to meters
wavelengthEndMeters = wavelengthEnd*1e-6 #Covert wavelength from microns to meters

#Radiance calculation
def f(x):
    return (c1/(math.pi*math.pow(n,2)*math.pow(x,5)))*(1/((math.exp(c2/(n*x*temperature)))-1))

result = quad(f,wavelengthStartMeters,wavelengthEndMeters)
radiance = result[0]

#print output
print("The Radiance emmited by the black body at a temperature of ",temperature," K in the wavelength range from ",wavelengthStart," to ",wavelengthEnd," microns is ",radiance," W/(m^2-sr-m)")