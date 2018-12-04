import triad_openvr as vr
import statistics
import matplotlib.pyplot as plt
import argparse
from transform import Transform
import pprint
import pandas as pd

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

pp = pprint.PrettyPrinter(indent=4)

v = vr.triad_openvr()
v.print_discovered_objects()
v.add_rel_dev('tracking_reference_1', 'tracker_0')

for key, value in enumerate(v.rel_devices):
    print (key, value)

def create_dict(data_raw, time):
    data_mean = statistics.mean(data_raw)
    data_min = min(data_raw)
    data_max = max(data_raw)
    data_stdev = statistics.stdev(data_raw)
    return {'stats': {'mean': data_mean, 'min': data_min,
                      'max': data_max, 'stdev': data_stdev},
            'raw': {'data': data_raw, 'time': time}}


data = v.rel_devices['tracking_reference_1-tracker_0'].sample(args.samples,
                                                              args.frequency)
stats = {}
# data = v.devices[args.device].sample_matrix(args.samples, args.frequency)
# print(data)


def add_plot(axarr, i, data_dict, name):
    title = 'variations around {}'.format(name)
    axarr[i].set_title(title)
    time = data_dict['raw']['time']
    raw = data_dict['raw']['data']
    axarr[i].plot(time, raw)
    axarr[i].plot(time, [data_dict['stats']['mean']]*len(raw), linestyle='--')
    axarr[i].plot(time, [data_dict['stats']['min']]*len(raw), linestyle='-', color='red',
                  alpha=0.4)
    axarr[i].plot(time, [data_dict['stats']['max']]*len(raw), linestyle='-', color='red',
                  alpha=0.4)
    axarr[i].fill_between(time, data_dict['stats']['mean'] + data_dict['stats']['stdev'], data_dict['stats']['mean'] - data_dict['stats']['stdev'],
                          color='#539caf', alpha=0.4, label='95% CI')

# Two subplots, the axes array is 1-d
f, axarr = plt.subplots(6, sharex=True)
# mean, min, max, stdev = common_stats(data.x)
stats['x'] = create_dict(data.x, data.time)
pp.pprint(stats['x']['stats'])
add_plot(axarr, 0, stats['x'], 'x')

stats['y'] = create_dict(data.y, data.time)
pp.pprint(stats['y']['stats'])
add_plot(axarr, 1, stats['y'], 'y')

stats['z'] = create_dict(data.z, data.time)
pp.pprint(stats['z']['stats'])
add_plot(axarr, 2, stats['z'], 'z')

stats['roll'] = create_dict(data.roll, data.time)
pp.pprint(stats['roll']['stats'])
add_plot(axarr, 3, stats['roll'], 'roll')

stats['pitch'] = create_dict(data.pitch, data.time)
pp.pprint(stats['pitch']['stats'])
add_plot(axarr, 4, stats['pitch'], 'pitch')

stats['yaw'] = create_dict(data.yaw, data.time)
pp.pprint(stats['yaw']['stats'])
add_plot(axarr, 5, stats['yaw'], 'yaw')

# print(stats)
save = {'name': [], 'min': [], 'mean': [], 'max': [], 'stdev': []}
for key, value in stats.items():
    save['name'].append(key)
    save['min'].append(value['stats']['min'])
    save['mean'].append(value['stats']['mean'])
    save['max'].append(value['stats']['max'])
    save['stdev'].append(value['stats']['stdev'])
plt.xlabel('Time (seconds)')

if args.file:
    df = pd.DataFrame(data=save)
    df.to_csv(args.file)
pp.pprint(save)
# pp.pprint(stats)
plt.show()
