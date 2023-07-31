import fastf1 as ff1
from fastf1 import plotting
from fastf1 import utils

from matplotlib import pyplot as plt
from matplotlib.pyplot import figure

import numpy as np
import pandas as pd

# Enable the cache by providing the name of the cache folder
ff1.Cache.enable_cache('cache') 

year, grand_prix, session = 2023, 'Belgium', 'R'

session = ff1.get_session(year, grand_prix, session)
session.load()
laps = session.laps

fig, ax = plt.subplots()

for drv in session.drivers:
    drv_laps = session.laps.pick_driver(drv)

    abb = drv_laps['Driver'].iloc[0]
    color = ''
    if abb == 'RIC':
        color = ff1.plotting.driver_color('DEV')
    else:
        color = ff1.plotting.driver_color(abb)
    
    
    ax.plot(drv_laps['LapNumber'], drv_laps['Position'], label=abb, color=color)
    
ax.set_ylim([20.5, 0.5])
ax.set_yticks([1, 5, 10, 15, 20])
ax.set_xlabel('Lap')
ax.set_ylabel('Position')

ax.legend(bbox_to_anchor=(1.0, 1.02))
plt.tight_layout()
#plt.suptitle("Position Changes: " + grand_prix)

plot_filename = f"PositionChanges2023Spa.png"
plt.savefig(plot_filename)
plt.show()