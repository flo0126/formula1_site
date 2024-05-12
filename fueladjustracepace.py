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

lapnum = 44


session = ff1.get_session(year, grand_prix, session)

session.load()

laps = session.laps


results = session.results

results = results.iloc[:3, 2].to_numpy()

top3_laps = laps.loc[(laps['Driver'] == results[0]) | (laps['Driver'] == results[1]) | (laps['Driver'] == results[2])]

forlat = top3_laps

top3_laps['LapTimeSeconds'] = top3_laps['LapTime'].dt.total_seconds()
top3_laps['LapTimeFuel'] = top3_laps['LapTimeSeconds'] - ((lapnum - top3_laps['LapNumber'])*(((110/lapnum)*35)/1000))
top3_laps = top3_laps.loc[(top3_laps['PitOutTime'].isnull() & top3_laps['PitInTime'].isnull())]


stints = forlat[["Driver", "Stint", "Compound", "LapNumber"]]
stints = stints.groupby(["Driver", "Stint", "Compound"])
stints = stints.count().reset_index()
stints = stints.rename(columns={"LapNumber": "StintLength"})


fig, ax = plt.subplots(figsize = (6, 5))

for driver in results:
    driver_laps = top3_laps.pick_driver(driver)
    x = driver_laps['LapNumber']
    y = driver_laps['LapTimeFuel']
    colorD = ff1.plotting.driver_color(driver)
    ax.plot(x, y, label=driver, color=colorD)
    
ax.set_xlabel('Lap')
ax.set_ylabel('Lap Speed (s)')
ax.legend()

plt.suptitle("Fuel Adjusted Race Pace Comparison: " + grand_prix)

plt.savefig("photos/fueladjustracepagebelgium.png")


fig, ax = plt.subplots(figsize = (6, 2))

for driver in results:
    driver_stints = stints.loc[stints["Driver"] == driver]

    previous_stint_end = 0
    for idx, row in driver_stints.iterrows():
        # each row contains the compound name and stint length
        # we can use these information to draw horizontal bars
        plt.barh(
            y=" "+driver,
            width=row["StintLength"],
            left=previous_stint_end,
            color=ff1.plotting.COMPOUND_COLORS[row["Compound"]],
            edgecolor="black",
            fill=True
        )

        previous_stint_end += row["StintLength"]

plt.xlabel("Lap")
plt.ylabel("Driver")
plt.grid(False)
# invert the y-axis so drivers that finish higher are closer to the top
ax.invert_yaxis()
#plt.show()


plt.savefig("photos/tirestratbelgium.png")