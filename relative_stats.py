import triad_openvr as vr
import statistics
import matplotlib.pyplot as plt
import argparse
from transform import Transform

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--device', help='device to read', type=str,
                    default='tracker_0')
parser.add_argument('-r', '--reference', help='ref lighthouse', type=str,
                    default='tracking_reference_1')
parser.add_argument('-f', '--frequency', help='read frequency', type=float,
                    default=250)
parser.add_argument('-s', '--samples', help='number of samples to read',
                    type=int, default=1000)
args = parser.parse_args()


v = vr.triad_openvr()
v.print_discovered_objects()
v.add_rel_dev('tracking_reference_1', 'tracker_0')
data = v.rel_devices['tracking_reference_1-tracker_0'].sample(args.samples, args.frequency)
for k, v in enumerate(v.rel_devices):
    print (k, v)
def common_stats(data):
    data_mean = statistics.mean(data)
    data_min = min(data)
    data_max = max(data)
    data_stdev = statistics.stdev(data)
    return data_mean, data_min, data_max, data_stdev


# data = v.devices[args.device].sample_matrix(args.samples, args.frequency)
# print(data)

# Two subplots, the axes array is 1-d
f, axarr = plt.subplots(6, sharex=True)

x_mean, x_min, x_max, x_stdev = common_stats(data.x)
print('stdev x : {}'.format(x_stdev))
axarr[0].set_title('variations around x')
axarr[0].plot(data.time, data.x)
axarr[0].plot(data.time, [x_mean]*len(data.x), linestyle='--')
axarr[0].plot(data.time, [x_min]*len(data.x), linestyle='-', color='red',
              alpha=0.4)
axarr[0].plot(data.time, [x_max]*len(data.x), linestyle='-', color='red',
              alpha=0.4)
axarr[0].fill_between(data.time, x_mean + x_stdev, x_mean - x_stdev,
                      color='#539caf', alpha=0.4, label='95% CI')

plt.xlabel('Time (seconds)')
plt.show()
