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
pretty_printer = pprint.PrettyPrinter(indent=4)

# Setting path to read
path = Path(os.getcwd()+'/'+args.directory)
os.chdir(path)

# Create sorted list of files to read
files = [f for f in os.listdir() if os.path.isfile(f) and f.endswith('_raw')]
files.sort()
print(files)

# Creating stack dataframe to populate with measurements
d = {'x': [], 'y': [], 'z': [],
     'r_x': [], 'r_y': [], 'r_z': [], 'r_w': [],
     'roll': [], 'pitch': [], 'yaw': [],
     'ref_roll': []}
stack_dataframe = pd.DataFrame(data=d)

# Adding all measurements from fils to one stack of dataframes
for f in files:
    measurement_dataframe = pd.read_csv(f)
    ref_values = measurement_dataframe.get(args.ref)
    measurement_dataframe = measurement_dataframe.assign(
        ref=pd.Series([np.round(np.mean(ref_values))]*len(ref_values)).values)
    pretty_printer.pprint(measurement_dataframe)
    stack_dataframe = stack_dataframe.append(measurement_dataframe)

pretty_printer.pprint(stack_dataframe)

# Creating plot according to type
if args.type == 'boxen':
    ax = sns.boxenplot(x='ref', y=args.var, data=stack_dataframe)
elif args.type == 'violin':
    ax = sns.violinplot(x='ref', y='z', data=stack_dataframe)
else:
    ax = sns.boxplot(x='ref', y='z', data=stack_dataframe)

ax.set_ylabel(args.var)
ax.set_xlabel(args.ref)
plt.show()
