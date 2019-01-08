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
parser.add_argument('directory', help='directory to read', type=str)
parser.add_argument('-v', '--var', help='variable to plot', type=str,
                    default='x')
parser.add_argument('-r', '--ref', help='reference variable', type=str,
                    default='roll')
parser.add_argument('-t', '--type', help='type of plot', type=str,
                    default='box', choices=['box', 'boxen', 'violin'])
args = parser.parse_args()
pp = pprint.PrettyPrinter(indent=4)
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
    ref = df.get(args.ref)
    df = df.assign(ref=pd.Series([np.round(np.mean(ref))]*len(ref)).values)
    pp.pprint(df)
    full_df = full_df.append(df)

pp.pprint(full_df)
if args.type == 'boxen':
    ax = sns.boxenplot(x='ref', y=args.var, data=full_df)
elif args.type == 'violin':
    ax = sns.violinplot(x='ref', y='z', data=full_df)
else:
    ax = sns.boxplot(x='ref', y='z', data=full_df)

ax.set_ylabel(args.var)
ax.set_xlabel(args.ref)
plt.show()
