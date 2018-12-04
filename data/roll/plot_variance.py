#! /usr/bien/env python3
import pandas as pd
import pprint
import matplotlib.pyplot as plt

pp = pprint.PrettyPrinter(indent=4)

data = {'ref_roll': [], 'x': [], 'y': [], 'z': [], 'roll': [], 'pitch': [],
        'yaw': []}
for i in range(0, 91, 15):
    df = pd.read_csv('{}.csv'.format(i))
    stdevs = df['stdev']
    data['ref_roll'].append(i)
    data['x'].append(stdevs[0])
    data['y'].append(stdevs[1])
    data['z'].append(stdevs[2])
    data['roll'].append(stdevs[3])
    data['pitch'].append(stdevs[4])
    data['yaw'].append(stdevs[5])

pp.pprint(data)

# Two subplots, the axes array is 1-d
f, axarr = plt.subplots(2, sharex=True)
axarr[0].plot(data['ref_roll'], data['x'], label='x')
axarr[0].plot(data['ref_roll'], data['y'], label='y')
axarr[0].plot(data['ref_roll'], data['z'], label='z')
axarr[0].set_title('stdev position variations over Roll')
axarr[0].legend()
axarr[0].set_ylabel('stdev (m)')
axarr[1].plot(data['ref_roll'], data['roll'], label='roll')
axarr[1].plot(data['ref_roll'], data['pitch'], label='pitch')
axarr[1].plot(data['ref_roll'], data['yaw'], label='yaw')
axarr[1].legend()
axarr[1].set_ylabel('stdev (m)')
axarr[1].set_title('stdev orientation variations over Roll')
plt.xlabel('roll (deg)')
plt.show()
