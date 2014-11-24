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

skip = True

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
		skip = False
		millic = d1 * pow(2,16) + d2
		nodes[mote_id]['start_done_t'].append(millic)

	if dbg == DBGS_RADIO_STOP_DONE:
		skip = False
		millic = d1 * pow(2,16) + d2
		nodes[mote_id]['stop_done_t'].append(millic)

if skip:
	sys.exit(0)

all_percent_on = []
all_percent_on_last_75 = []

# for each node sending to destination 
for mote_id in nodes.keys():
	nodes[mote_id]['start_done_t'] = nodes[mote_id]['start_done_t'][4:]
	nodes[mote_id]['stop_done_t'] = nodes[mote_id]['stop_done_t'][4:]

	nodes[mote_id]['sum_on_time_ms'] = sum( nodes[mote_id]['start_done_t'] )
	nodes[mote_id]['sum_off_time_ms'] = sum( nodes[mote_id]['stop_done_t'] )
	nodes[mote_id]['sum_on_time_ms_last_75'] = sum( nodes[mote_id]['start_done_t'][(50 * len(nodes[mote_id]['start_done_t']) / 100):] )
	nodes[mote_id]['sum_off_time_ms_last_75'] = sum( nodes[mote_id]['stop_done_t'][(50 * len(nodes[mote_id]['stop_done_t']) / 100):] )

	nodes[mote_id]['percent_on_time_ms'] = (100.0 * nodes[mote_id]['sum_on_time_ms']) / \
		( nodes[mote_id]['sum_on_time_ms'] + nodes[mote_id]['sum_off_time_ms'] )
	nodes[mote_id]['percent_on_time_ms_last_75'] = (100.0 * nodes[mote_id]['sum_on_time_ms_last_75']) / \
		( nodes[mote_id]['sum_on_time_ms_last_75'] + nodes[mote_id]['sum_off_time_ms_last_75'] )

	print "Node %d:  Time On %.3f     Last 75%% %.3f" % (mote_id, nodes[mote_id]['percent_on_time_ms'],
				nodes[mote_id]['percent_on_time_ms_last_75'])
	#if mote_id != root and nodes[mote_id]['percent_on_time_ms'] < 10:
	if mote_id != root:
		all_percent_on.append(nodes[mote_id]['percent_on_time_ms'])
		all_percent_on_last_75.append(nodes[mote_id]['percent_on_time_ms_last_75'])


data_summary = {}
data_summary['all'] = all_percent_on
data_summary['min'] = min(all_percent_on)
data_summary['max'] = max(all_percent_on)
data_summary['median'] = sorted(all_percent_on)[len(all_percent_on)/2]
data_summary['avg'] = np.array(all_percent_on).mean()
data_summary['std'] = np.array(all_percent_on).std()

data_summary['all_75'] = all_percent_on_last_75
data_summary['min_75'] = min(all_percent_on_last_75)
data_summary['max_75'] = max(all_percent_on_last_75)
data_summary['median_75'] = sorted(all_percent_on_last_75)[len(all_percent_on_last_75)/2]
data_summary['avg_75'] = np.array(all_percent_on_last_75).mean()
data_summary['std_75'] = np.array(all_percent_on_last_75).std()


print "\n\nAll Data:  \tMedian: %.3f  Mean: %.3f  Std: %.3f \t\t Min: %.3f  Max: %.3f\n" % ( data_summary["median"],
	data_summary['avg'], data_summary['std'], data_summary['min'], data_summary['max'])
print "Last 75%%:   \tMedian: %.3f  Mean: %.3f  Std: %.3f \t\t Min: %.3f  Max: %.3f\n\n" % ( data_summary["median_75"],
	data_summary['avg_75'], data_summary['std_75'], data_summary['min_75'], data_summary['max_75'])

# delete detailed logs from the memory
for mote_id in nodes.keys():
#	nodes[mote_id].pop('start_done_t', None)
	nodes[mote_id].pop('stop_done_t', None)
	nodes[mote_id].pop('last_start_done', None)
	nodes[mote_id].pop('last_stop_done', None)

# save as json
with open(sys.argv[2], 'wb') as fp:
	json.dump(nodes, fp, sort_keys=True, indent=4)


# save as json
with open("summary_%s" % (sys.argv[2]), 'wb') as fp:
	json.dump(data_summary, fp, sort_keys=True, indent=4)


