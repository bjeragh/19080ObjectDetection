#!/usr/bin/python3

import numpy as np
from scipy.optimize import fsolve
import math

g = 9.8 # m/s^2
y = 2 # meters
x=6

def equations(p):
    theta, t, v = p
    f1 = (-v * math.cos(math.radians(theta)) * math.tan(math.radians(45))) + (-v * math.sin(math.radians(theta))) + (g * t) 
    f2 = y - (v * math.sin(math.radians(theta)) * t) + (.5 * g * t ** 2)
    f3 = x - (v * math.cos(math.radians(theta)) * t)
    return (f1, f2, f3)

theta, t, v = fsolve(equations, (45,5,20))
print ("Shooting Angle = %f" %theta)
print("Time in the air = %f" %t)
print("Initial Velocity = %f" %v)



