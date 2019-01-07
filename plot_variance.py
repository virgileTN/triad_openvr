#! /usr/bien/env python3
import pandas as pd
import pprint
import matplotlib.pyplot as plt
import os
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--directory', help='directory to read', type=str,
                    default='data/')
args = parser.parse_args()
pp = pprint.PrettyPrinter(indent=4)

data = {'ref_roll': [], 'x': [], 'y': [], 'z': [], 'roll': [], 'pitch': [],
        'yaw': []}
path = Path(os.getcwd()+'/'+args.directory)
os.chdir(path)
files = [f for f in os.listdir() if os.path.isfile(f) and f.endswith('.csv')]
files.sort()
print(files)
for f in files:
    df = pd.read_csv(f)
    stdevs = df['stdev']
    if stdevs[3] < 1:
        data['ref_roll'].append(df['mean'][3])
        data['x'].append(stdevs[0])
        data['y'].append(stdevs[1])
        data['z'].append(stdevs[2])
        data['roll'].append(stdevs[3])
        data['pitch'].append(stdevs[4])
        data['yaw'].append(stdevs[5])

df = pd.DataFrame(data)
df.sort_values(by='ref_roll', inplace=True)
# for i in range(0, 91, 15):
#     df = pd.read_csv('{}.csv'.format(i))
#     stdevs = df['stdev']
#     data['ref_roll'].append(i)
#     data['x'].append(stdevs[0])
#     data['y'].append(stdevs[1])
#     data['z'].append(stdevs[2])
#     data['roll'].append(stdevs[3])
#     data['pitch'].append(stdevs[4])
#     data['yaw'].append(stdevs[5])

pp.pprint(data)
pos_mean = [(df['x'][i]+df['y'][i]+df['z'][i]) for i in range(0, len(df))]
rot_mean = [(df['roll'][i]+df['pitch'][i]+df['yaw'][i]) for i in range(len(df))]
print(pos_mean)
# Two subplots, the axes array is 1-d
f, axarr = plt.subplots(2, sharex=True)
axarr[0].plot(df['ref_roll'], df['x'], label='x')
axarr[0].plot(df['ref_roll'], df['y'], label='y')
axarr[0].plot(df['ref_roll'], df['z'], label='z')
# axarr[0].plot(df['ref_roll'], pos_mean, label='mean')
axarr[0].set_title('stdev position variations over Roll')
axarr[0].legend()
axarr[0].set_ylabel('stdev (m)')
axarr[1].plot(df['ref_roll'], df['roll'], label='roll')
axarr[1].plot(df['ref_roll'], df['pitch'], label='pitch')
axarr[1].plot(df['ref_roll'], df['yaw'], label='yaw')
# axarr[1].plot(df['ref_roll'], rot_mean, label='mean')
axarr[1].legend()
axarr[1].set_ylabel('stdev (m)')
axarr[1].set_title('stdev orientation variations over Roll')
plt.xlabel('roll (deg)')
plt.show()
