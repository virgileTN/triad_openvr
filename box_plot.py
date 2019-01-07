#! /usr/bien/env python3
import pandas as pd
import pprint
import matplotlib.pyplot as plt
import os
import argparse
from pathlib import Path
import numpy as np
import seaborn as sns

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--directory', help='directory to read', type=str,
                    default='data/')
args = parser.parse_args()
pp = pprint.PrettyPrinter(indent=4)

# data = {'ref_roll': [], 'x': [], 'y': [], 'z': [], 'roll': [], 'pitch': [],
#         'yaw': []}
datas = []
path = Path(os.getcwd()+'/'+args.directory)
os.chdir(path)
files = [f for f in os.listdir() if os.path.isfile(f) and f.endswith('_raw')]
files.sort()
print(files)
x = []
d = {'x': [], 'y': [], 'z': [], 'roll': [], 'pitch': [], 'yaw': [], 'r_x': [],
     'r_y': [], 'r_z': [], 'r_w': [], 'ref_roll': []}
full_df = pd.DataFrame(data=d)
for f in files:
    df = pd.read_csv(f)
    roll = df.get('roll')
    df = df.assign(ref_roll=pd.Series([np.mean(roll)]*len(roll)).values)
    pp.pprint(df)
    full_df = full_df.append(df)

pp.pprint(full_df)
sns.boxplot(x='ref_roll', y='x', data=full_df)
# sns.boxplot(y='roll', data=df)
plt.show()

# df = pd.DataFrame(data)
# df.sort_values(by='ref_roll', inplace=True)
# # Fixing random state for reproducibility
# np.random.seed(19680801)
#
# # fake up some data
# spread = np.random.rand(50) * 100
# center = np.ones(25) * 50
# flier_high = np.random.rand(10) * 100 + 100
# flier_low = np.random.rand(10) * -100
# data = np.concatenate((spread, center, flier_high, flier_low))
