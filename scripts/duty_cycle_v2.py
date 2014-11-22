#!/usr/bin/python
# Processing dbgs messages from Counter test application
# Author: Marcin K Szczodrak
# Updated; 5/02/2014

import sys
import os
sys.path.append("%s/support/sdk/python" % (os.environ["FENNEC_FOX_LIB"]))
from dbgs_h import *
import numpy as np
import json

# usage script logs

if len(sys.argv) != 5:
	print "usage %s <result.txt> <data.json> <testbed_conf> <root>"
	sys.exit(1)

f = open(sys.argv[1], "r")

nodes = {}

total_send = 0
total_receive = 0

testbed_conf_module = sys.argv[3].split("/")[-1].split(".")[0]
path_to_testbed_conf_module = "/".join(sys.argv[3].split("/")[:-1])
sys.path.append(path_to_testbed_conf_module)
root = int(float(sys.argv[4]))

try:
	testbed_conf = __import__(testbed_conf_module)
except:
	print "failed to import %s\n" % (testbed_conf_module)
	exit()


for line in f.readlines():
	l = line.split()

	if len(l) != 9:
		continue

	if not l[0].isdigit():
		continue

	timestamp = int(l[0]) * 1000 + int(l[1])
	mote_id = int(l[2])
	version = int(l[3])
	did = int(l[4])
	dbg = int(l[5])
	d0 = int(l[6])
	d1 = int(l[7])
	d2 = int(l[8])

	if mote_id > testbed_conf.max_node_id:
		print line
		continue

	if mote_id == root:
		continue

	if not(mote_id in nodes.keys()):
		new_node = {}
		new_node['start_done_t'] = []
		new_node['stop_done_t'] = []
		nodes[mote_id] = new_node

	if dbg == DBGS_RADIO_START_DONE:
		millic = d1 * pow(2,16) + d2
		nodes[mote_id]['start_done_t'].append(millic)

	if dbg == DBGS_RADIO_STOP_DONE:
		millic = d1 * pow(2,16) + d2
		nodes[mote_id]['stop_done_t'].append(millic)


total_on = 0.0
total_off = 0.0
all_on = []
all_off = []
all_percent_on = []
all_percent_on_75 = []

# for each node sending to destination 
for mote_id in nodes.keys():
	on = np.array(nodes[mote_id]['start_done_t'][1:])
	off = np.array(nodes[mote_id]['stop_done_t'][1:])

	len_on = len(nodes[mote_id]['start_done_t'])
	len_off = len(nodes[mote_id]['stop_done_t'])

	on_75 = np.array(nodes[mote_id]['start_done_t'][(25 * len_on / 100):])
	off_75 = np.array(nodes[mote_id]['stop_done_t'][(25 * len_off / 100):])

	nodes[mote_id]['sum_on_time_ms'] = on.sum()
	nodes[mote_id]['sum_off_time_ms'] = off.sum()

	nodes[mote_id]['sum_on_time_ms_last_75'] = on_75.sum()
	nodes[mote_id]['sum_off_time_ms_last_75'] = off_75.sum()

#	if ( nodes[mote_id]['sum_on_time_ms'] + nodes[mote_id]['sum_off_time_ms'] ) > 0:
	nodes[mote_id]['percent_on_time_ms'] = (100.0 * nodes[mote_id]['sum_on_time_ms']) / \
			( nodes[mote_id]['sum_on_time_ms'] + nodes[mote_id]['sum_off_time_ms'] )


	nodes[mote_id]['percent_on_time_ms_last_75'] = (100.0 * nodes[mote_id]['sum_on_time_ms_last_75']) / \
			( nodes[mote_id]['sum_on_time_ms_last_75'] + nodes[mote_id]['sum_off_time_ms_last_75'] )

	nodes[mote_id]['mean_on_time_ms'] = on.mean()
	nodes[mote_id]['mean_off_time_ms'] = off.mean()
	nodes[mote_id]['std_on_time_ms'] = on.std()
	nodes[mote_id]['std_off_time_ms'] = off.std()

	print "Node %d:  Time On %.3f   Mean: %.3f   Std: %.3f" % (mote_id,
			nodes[mote_id]['percent_on_time_ms'],
			nodes[mote_id]['mean_on_time_ms'], 
			nodes[mote_id]['std_on_time_ms'])

	total_on += nodes[mote_id]['sum_on_time_ms']
	total_off += nodes[mote_id]['sum_off_time_ms']

	all_on += nodes[mote_id]['start_done_t']
	all_off += nodes[mote_id]['stop_done_t']

	all_percent_on.append(nodes[mote_id]['percent_on_time_ms'])
	all_percent_on_75.append(nodes[mote_id]['percent_on_time_ms_last_75'])


on_array = np.array(all_on)
off_array = np.array(all_off)
on_sum = on_array.sum()
off_sum = off_array.sum()

if len(on_array) == 0:
	on_mean = 0
	on_std = 0
else:
	on_mean = on_array.mean()
	on_std = on_array.std()

if len(off_array) == 0:
	off_mean = 0
	off_std = 0
else:
	off_mean = off_array.mean()
	off_std = off_array.std()

if (on_sum + off_sum == 0):
	total = on_sum * 100.0
else:
	total = on_sum * 100.0 / (on_sum + off_sum)

print "\n\nTotal: %.3f\n" % (total)
print "MeanOn: %.3f  StdOn: %.3f \t\t MeanOff: %.3f  StdOff: %.3f\n\n" % (on_mean,
	on_std, off_mean, off_std)


all_percent_on = sorted(all_percent_on)
all_percent_on_75 = sorted(all_percent_on_75)
#print all_percent_on

avg_percent_on = sum(all_percent_on) * 1.0  / len(all_percent_on)
avg_percent_on_75 = sum(all_percent_on_75) * 1.0  / len(all_percent_on_75)

shorter_95 = 95 * len(all_percent_on) / 100
all_percent_on_95 = all_percent_on[:shorter_95]
avg_percent_on_95 = sum(all_percent_on_95) * 1.0  / len(all_percent_on_95)

shorter_80 = 80 * len(all_percent_on) / 100
all_percent_on_80 = all_percent_on[:shorter_80]
avg_percent_on_80 = sum(all_percent_on_80) * 1.0  / len(all_percent_on_80)

shorter_75 = 75 * len(all_percent_on) / 100
all_percent_on_75 = all_percent_on[:shorter_75]
avg_percent_on_75 = sum(all_percent_on_75) * 1.0  / len(all_percent_on_75)

shorter_50 = 50 * len(all_percent_on) / 100
all_percent_on_50 = all_percent_on[:shorter_50]
avg_percent_on_50 = sum(all_percent_on_50) * 1.0  / len(all_percent_on_50)

shorter_25 = 25 * len(all_percent_on) / 100
all_percent_on_25 = all_percent_on[:shorter_25]
avg_percent_on_25 = sum(all_percent_on_25) * 1.0  / len(all_percent_on_25)

print "Avg On %f    95%%: %f     80%%: %f     75%%: %f     50%%: %f     25%%: %f\n" % (avg_percent_on,
		avg_percent_on_95, avg_percent_on_80, avg_percent_on_75, avg_percent_on_50, avg_percent_on_25)

print "Last 75%% of experiments had duty-cycle: %f" % (avg_percent_on_75)

# delete detailed logs from the memory
for mote_id in nodes.keys():
	nodes[mote_id].pop('start_done_t', None)
	nodes[mote_id].pop('stop_done_t', None)
	nodes[mote_id].pop('last_start_done', None)
	nodes[mote_id].pop('last_stop_done', None)


data_summary = {}
data_summary['100'] = avg_percent_on
data_summary['95'] = avg_percent_on_95
data_summary['80'] = avg_percent_on_80
data_summary['75'] = avg_percent_on_75
data_summary['50'] = avg_percent_on_50
data_summary['25'] = avg_percent_on_25

# save as json
with open(sys.argv[2], 'wb') as fp:
	json.dump(nodes, fp, sort_keys=True, indent=4)


# save as json
with open("summary_%s" % (sys.argv[2]), 'wb') as fp:
	json.dump(data_summary, fp, sort_keys=True, indent=4)
