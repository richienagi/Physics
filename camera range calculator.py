# -*- coding: utf-8 -*-
"""
The following program calculates how far a scene can be from a pocket camera and still be sufficiently illuminated
for nighttime photos in a dark room.

Notes:
    - Assumes a square FOI (Field of Illumination) by the camera flash. For example for a 5 by 5 degrees FOI,
    enter 5 degrees for the FOI user input.
    - Assumes square pixels for the camera sensor chip.
    - Assumes operation in the camera in the visible band. If using calculator for other bands, adjust appropriate
    user inputs accordingly (scene reflectivity, transmission of camera optics, pixel sensitivity - depending on
    component specifications).
"""
import math

#User inputs
sourcePower = float(input('Enter the optical output power of the camera flash (Watts): '))
fieldOfIllumination =  float(input('Enter the angle of the field of illumination of the camera flash in degrees (see notes section in program for details): '))
averageSceneReflectivity = float(input('Enter the average reflectivity of the scene over the visible band (0 to 1): '))
transmissionofOptics = float(input('Enter the transmission of the optics before the camera sensor for the visible band (0 to 1): '))
fNumberOptics = float(input('Enter the f/# of the camera sensor optics: '))
pixelSize = float(input('Enter the size of the pixel, assuming square geometry (microns): '))
pixelSensitivity = float(input('Enter the smallest detectable power from the scene by the pixels (Watts): '))

#Calculating solid angle of the camera sensor optics
omegaF = math.pi*math.pow(math.sin(math.atan(1/(fNumberOptics*2))),2)

#Caculating the pixel area, assuming a square pixel
pixelArea = math.pow(pixelSize/(math.pow(10,6)),2) #aquare meters

#Calculation of the range of the camera
areaOfIllumination = (transmissionofOptics*(averageSceneReflectivity/(math.pi))*sourcePower*pixelArea*omegaF)/pixelSensitivity #square meters
#The assumption in the notes states a square FOI
sideOfIlluminatedSquare = math.pow(areaOfIllumination,0.5)
cameraRange = (sideOfIlluminatedSquare/2)/math.tan(math.radians(fieldOfIllumination))

#Print output
print("The target scene can be as far as ",cameraRange," meters from the camera and still be sufficiently illuminated for taking photos.")