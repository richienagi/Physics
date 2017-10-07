# -*- coding: utf-8 -*-
"""
The following program computes the time evolution of a simple pendulum using the Euler or Verlet method. This 
program is the Python version of the pendul.m (Matlab) program, taken from the book "Numerical Methods for 
Physics", published by Alejandro Garcia (Professor - San Jose State University Physics and Astronomy Department)

To run this code, download the Anaconda Python distribution, and copy this code in the Syder editor. No external
libraries need to be imported (as of August 2017).
"""
import numpy as np
import math
import matplotlib.pyplot as plt 

# Select the numerical method to use: Euler or Verlet
numericalMethod = int(input('Choose a numerical method -> For Euler, enter 1, For Verlet, enter 2: '))

# Set initial position and velocity of pendulum
theta0 = float(input('Enter initial angle (in degrees): '))
theta = (theta0*math.pi)/180 # convert angle to radians
omega = 0 # set the initial velocity

# Set physical constants and other variables
g_over_L = 1 # The constant g/L
time = 0 # Initial time
irev = 0 # Used to count the number of reversals
tau = float(input('Enter the time step: '))

# Take one backward step to start Verlet
accel = -g_over_L*math.sin(theta) # Gravitational acceleration
theta_old = theta - (omega*tau) + (0.5*math.pow(tau,2)*accel)

# Loop over desired number of steps with given time step and numerical method
nstep = int(input('Enter number of time steps: '))
# Array initializations (You should be able to skip this by dynamically allocating these arrays. This will most
# likely change some of the code in the for loop)
t_plot = np.zeros((nstep,1)) 
th_plot = np.zeros((nstep,1))
period = np.zeros((nstep,1))

for istep in range(1,nstep):
    # Record angle and time for plotting
    t_plot[istep] = time
    th_plot[istep] = (theta*180)/math.pi # Convert  angle to degrees
    time = time + tau
    # Compute new position and velocity using Euler or Verlet method
    accel = -g_over_L*math.sin(theta) # Gravitational acceleration
    if numericalMethod == 1:
        theta_old = theta # Save previous angle
        theta = theta + (tau*omega) # Euler method
        omega = omega +(tau*accel)
    else:
        theta_new = (2*theta) - theta_old + (math.pow(tau,2)*accel)
        theta_old = theta # Verlet method
        theta = theta_new
    # Test if the pendulum has passed through theta  = 0; if yes, use time to estimate period
    if theta*theta_old < 0: # Test position for sign change
        print("Turning point at time t = ", time, " seconds")
        if irev == 0: # If this is the first change, just record the time
            time_old = time
        else:
            period[irev] = 2*(time - time_old)
            time_old = time
        irev = irev + 1 # Increment the number of reversals

# Plot output
plt.figure
plt.plot(t_plot,th_plot,'+')
plt.xlabel('Time')
plt.ylabel('degrees')
plt.title('Pendulum motion')
plt.show()
            