#import fastf1 as ff1
#from fastf1 import plotting
#from fastf1 import utils

from matplotlib import pyplot as plt
from matplotlib.pyplot import figure


import numpy as np
import pandas as pd


from scipy.optimize import curve_fit
from scipy.interpolate import UnivariateSpline

#-------------------------------------

traction  = np.array([4,2,2,5,3,5,3,5,2,3,4,4,4,3,4,3])
track_evolution = np.array([4,4,4,5,5,5,3,5,3,2,4,3,4,3,4,3])
braking = np.array([4,2,2,4,3,2,3,5,3,2,3,4,3,4,5,2])
asphalt_grip = np.array([3,3,3,1,3,1,3,1,3,3,3,3,2,2,3,3])
lateral = np.array([3,3,3,1,3,1,5,1,3,5,3,5,4,2,2,5])
asphalt_abrasion = np.array([5,2,2,1,2,1,4,2,4,3,2,4,3,3,3,4])
tire_stress = np.array([3,3,3,3,3,1,5,3,3,5,3,5,5,3,2,5])
downforce = np.array([3,2,3,1,2,5,4,1,3,4,5,2,4,1,5,4])
tires = np.array([1,2,2,3,2,3,1,3,3,1,3,2,1,3,3,1])


LECgap = np.array([0.292, 0.155, 0.637, 0, 1.02, 0.106, 0.464, 1.523, 0.048, 0.416, 0.383, 0.82, 2.098, 0.067, 0.079, 0.665])
LECfin = np.array([-1, 7, -1, 3,7,6,11,4,2,9,7,3,-1,4,4,4])

#tire_stress_LECgap = np.column_stack([])

plt.plot(lateral, LECfin, 'o')
#plt.plot(downforce, LECfin, 'o')
plt.show()


