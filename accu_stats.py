import triad_openvr as vr
import statistics
import matplotlib.pyplot as plt
import argparse
from transform import Transform

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--device', help='device to read', type=str,
                    default='tracker_0')
parser.add_argument('-f', '--frequency', help='read frequency', type=float,
                    default=250)
parser.add_argument('-s', '--samples', help='number of samples to read',
                    type=int, default=1000)
args = parser.parse_args()


v = vr.triad_openvr()
v.print_discovered_objects()

def common_stats(data):
    data_mean = statistics.mean(data)
    data_min = min(data)
    data_max = max(data)
    data_stdev = statistics.stdev(data)
    return data_mean, data_min, data_max, data_stdev


data = v.devices[args.device].sample(args.samples, args.frequency)

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

y_mean, y_min, y_max, y_stdev = common_stats(data.y)
print('stdev y : {}'.format(y_stdev))
axarr[1].set_title('variations around y')
axarr[1].plot(data.time, data.y)
axarr[1].plot(data.time, [y_mean]*len(data.y), linestyle='--')
axarr[1].plot(data.time, [y_min]*len(data.y), linestyle='-', color='red',
              alpha=0.4)
axarr[1].plot(data.time, [y_max]*len(data.y), linestyle='-', color='red',
              alpha=0.4)
axarr[1].fill_between(data.time, y_mean + y_stdev, y_mean - y_stdev,
                      color='#539caf', alpha=0.4, label='95% CI')

z_mean, z_min, z_max, z_stdev = common_stats(data.z)
print('stdev z : {}'.format(z_stdev))
axarr[2].set_title('variations around z')
axarr[2].plot(data.time, data.z)
axarr[2].plot(data.time, [z_mean]*len(data.z), linestyle='--')
axarr[2].plot(data.time, [z_min]*len(data.z), linestyle='-', color='red',
              alpha=0.4)
axarr[2].plot(data.time, [z_max]*len(data.z), linestyle='-', color='red',
              alpha=0.4)
axarr[2].fill_between(data.time, z_mean + z_stdev, z_mean - z_stdev,
                      color='#539caf', alpha=0.4, label='95% CI')

yaw_mean, yaw_min, yaw_max, yaw_stdev = common_stats(data.yaw)
print('stdev yaw : {}'.format(yaw_stdev))
axarr[3].set_title('variations around yaw')
axarr[3].plot(data.time, data.yaw)
axarr[3].plot(data.time, [yaw_mean]*len(data.yaw), linestyle='--')
axarr[3].plot(data.time, [yaw_min]*len(data.yaw), linestyle='-', color='red',
              alpha=0.4)
axarr[3].plot(data.time, [yaw_max]*len(data.yaw), linestyle='-', color='red',
              alpha=0.4)
axarr[3].fill_between(data.time, yaw_mean + yaw_stdev, yaw_mean - yaw_stdev,
                      color='#539caf', alpha=0.4, label='95% CI')

roll_mean, roll_min, roll_max, roll_stdev = common_stats(data.roll)
print('stdev roll : {}'.format(roll_stdev))
axarr[4].set_title('variations around roll')
axarr[4].plot(data.time, data.roll)
axarr[4].plot(data.time, [roll_mean]*len(data.roll), linestyle='--')
axarr[4].plot(data.time, [roll_min]*len(data.roll), linestyle='-', color='red',
              alpha=0.4)
axarr[4].plot(data.time, [roll_max]*len(data.roll), linestyle='-', color='red',
              alpha=0.4)
axarr[4].fill_between(data.time, roll_mean + roll_stdev, roll_mean - roll_stdev,
                      color='#539caf', alpha=0.4, label='95% CI')

pitch_mean, pitch_min, pitch_max, pitch_stdev = common_stats(data.pitch)
print('stdev pitch : {}'.format(pitch_stdev))
axarr[5].set_title('variations around pitch')
axarr[5].plot(data.time, data.pitch)
axarr[5].plot(data.time, [pitch_mean]*len(data.pitch), linestyle='--')
axarr[5].plot(data.time, [pitch_min]*len(data.pitch), linestyle='-', color='red',
              alpha=0.4)
axarr[5].plot(data.time, [pitch_max]*len(data.pitch), linestyle='-', color='red',
              alpha=0.4)
axarr[5].fill_between(data.time, pitch_mean + pitch_stdev, pitch_mean - pitch_stdev,
                      color='#539caf', alpha=0.4, label='95% CI')





plt.xlabel('Time (seconds)')
plt.show()
