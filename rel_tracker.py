import triad_openvr
import time
import sys

v = triad_openvr.triad_openvr()
v.print_discovered_objects()
v.add_rel_dev('tracking_reference_1', 'tracker_0')

if len(sys.argv) == 1:
    interval = 1/250
elif len(sys.argv) == 2:
    interval = 1/float(sys.argv[0])
else:
    print("Invalid number of arguments")
    interval = False

if interval:
    while(True):
        start = time.time()
        txt = ""
        for each in v.rel_devices["tracking_reference_1-tracker_0"].get_pose_euler():
            txt += "%.4f" % each
            txt += " "
        print("\r" + txt, end="")
        sleep_time = interval-(time.time()-start)
        if sleep_time>0:
            time.sleep(sleep_time)
