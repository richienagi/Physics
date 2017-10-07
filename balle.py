"""
The following program computes the trajectory of a baseball using the Euler method. This program is the Python
version of the balle.m (Matlab) program, taken from the book "Numerical Methods for Physics", published by 
Alejandro Garcia (Professor - San Jose State University Physics and Astronomy Department)

To run this code, download the Anaconda Python distribution, and copy this code in the Syder editor. No external
libraries need to be imported (as of August 2017).
"""
import numpy as np
import math
import matplotlib.pyplot as plt 

# Set initial position and velocity of baseball
y1 = int(input('Enter initial height (meters): '))
r1 = np.array([0,y1])
speed = int(input('Enter intial speed (m/s): '))
theta = int(input('Enter initial angle (degrees): '))
v1 = np.array([speed*math.cos((theta*math.pi)/180),speed*math.sin((theta*math.pi)/180)]) 
r = r1
v = v1

# Set physical parameters
Cd = 0.35 # Drag coefficient 
area = 4e-3 # Cross-sectional area of projectile (m^2)
grav = 9.81 # Gravitational acceleration (m/s^2)
mass = 0.145 # Mass of projectile (kg)
airFlag = int(input('Air resistance? (Yes:1, No:0): '))

if airFlag == 0:
    rho = 0 # No air resistance
else: 
    rho = 1.2 # Density of air (kg/m^3)
air_const = -0.5*Cd*rho*area/mass # Air resistance constant
        
tau = float(input('Enter timestep, tau (sec): '))
maxstep = 1000 # Maximum number of steps

# Array initializations (You should be able to skip this by dynamically allocating these arrays. This will most
# likely change some of the code in the for loop)
xplot = np.zeros((maxstep,1))
yplot = np.zeros((maxstep,1))
xNoAir = np.zeros((maxstep,1))
yNoAir = np.zeros((maxstep,1))

# Loop until ball hits ground or max steps completed
for istep in range(1,maxstep):
    # Record position (computed and theoretical) for plotting
    xplot[istep] = r[0] # Record trajectory for plot (x-direction)
    yplot[istep] = r[1] # Record trajectory for plot (y-direction)
    t = (istep-1)*tau # Curret time
    xNoAir[istep] = r1[0] + (v1[0]*t) #Theorectical calculation (x-direction)
    yNoAir[istep] = r1[1] + (v1[1]*t) - (0.5*grav*math.pow(t,2)) # Theoretical calculation (y-direction)
    # Calculate the acceleration of the ball
    accel = air_const*np.linalg.norm(v)*v # Air resistance
    accel[1] = accel[1] - grav # Gravity
    # Calculate the new position and velocity using Euler method
    r = r + (tau*v) # Euler step
    v = v + (tau*accel)
    # If ball reaches ground (y < 0), break out of loop
    if r[1] < 0:
        xplot[istep+1] = r[0] # Recoed last positions computed
        yplot[istep+1] = r[1]
        break # Break out of the loop

# Print outputs
print("Maximum range is: ", r[0], " meters")
print("Time of flight is: ", istep*tau, "seconds")

# Marks location of ground with a straight line
xgroud = [0,max(xNoAir)]
yground = [0,0]

# Trims the excess zeros at the end of the arrays. You should be able to avoid this by dynamic allocation
xplot = np.trim_zeros(xplot,'b')
yplot = np.trim_zeros(yplot,'b')
xNoAir = np.trim_zeros(xNoAir,'b')
yNoAir = np.trim_zeros(yNoAir,'b')

# Graph the trajectory of the baseball 
plt.figure
plt.plot(xplot,yplot,'+',xNoAir,yNoAir,'-',xgroud,yground,'-')
plt.xlabel('Range (m)')
plt.ylabel('Height (m)')
plt.title('Projectile motion')
plt.show()