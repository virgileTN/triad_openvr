import triad_openvr as vr
import statistics
import matplotlib.pyplot as plt
import argparse
from transform import Transform
import pprint
import pandas as pd
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--device', help='device to read', type=str,
                    default='tracker_0')
parser.add_argument('-r', '--reference', help='ref lighthouse', type=str,
                    default='tracking_reference_1')
parser.add_argument('-f', '--frequency', help='read frequency', type=float,
                    default=250)
parser.add_argument('-s', '--samples', help='number of samples to read',
                    type=int, default=1000)
parser.add_argument('-fi', '--file', help='file to write',
                    type=str)
args = parser.parse_args()
pretty_printer = pprint.PrettyPrinter(indent=4)

v = vr.triad_openvr()
v.print_discovered_objects()
v.add_rel_dev(args.reference, args.device)
lighthouses_count = len(v.object_names['Tracking Reference'])
print(lighthouses_count)
for key, value in enumerate(v.rel_devices):
    print (key, value)

if args.file:
    data = v.rel_devices['{0}-{1}'.format(args.reference,
                                          args.device)].sample(args.samples,
                                                               args.frequency)
    pose_dataframe = pd.DataFrame(data=data)
    pose_dataframe = pose_dataframe.assign(lighthouses_count=pd.Series([lighthouses_count]*len(pose_dataframe)).values)
    pose_dataframe.to_csv('{}_raw'.format(args.file), index=False)
    pretty_printer.pprint(pose_dataframe)
    print("translation {} succefully written to {}".format('{0}-{1}'.format(args.reference, args.device),
                                                                           args.file))
else:
    while(1):
        data = v.rel_devices['{0}-{1}'.format(args.reference,
                                              args.device)].sample(args.samples,
                                                                   args.frequency)
        print('roll', np.mean(data['roll']))
        print('pitch', np.mean(data['pitch']))
        print('yaw', np.mean(data['yaw']))
        print('x', np.mean(data['x']))
        print('y', np.mean(data['y']))
        print('z', np.mean(data['z']))
