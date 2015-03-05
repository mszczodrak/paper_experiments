#!/usr/bin/python
# Processing dbgs messages from Counter test application
# Author: Marcin K Szczodrak
# Updated; 4/24/2014

import sys
import os
sys.path.append("%s/support/sdk/python" % (os.environ["FENNEC_FOX_LIB"]))
from dbgs_h import *
import numpy as np
import json

# usage script logs

if len(sys.argv) != 4:
	print "usage %s <result.txt> <data.json> <testbed_conf>"
	sys.exit(1)

f = open(sys.argv[1], "r")

testbed_conf_module = sys.argv[3].split("/")[-1].split(".")[0]
path_to_testbed_conf_module = "/".join(sys.argv[3].split("/")[:-1])
sys.path.append(path_to_testbed_conf_module)

nodes = {}
starts = []
sequences = {}

offset = 999999999999999999999

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

	timestamp = int(l[0]) + (float(l[1]) / 1000.0)
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

	if mote_id not in nodes.keys():
		nodes[mote_id] = {}
		nodes[mote_id]['hist'] = []
		nodes[mote_id]['last'] = []

	if dbg == DBGS_SIGNAL_FINISH_PERIOD:
		if len(stop_delays[-1]["data"]) > 0  and \
			timestamp - stop_delays[-1]["data"][-1] > 1:
			add_period()

		stop_delays[-1]["data"].append(timestamp)	
		stop_delays[-1]["motes"].append(mote_id)


	if dbg == DBGS_NEW_LOCAL_PAYLOAD:
		st = {}
		st['timestamp']	= timestamp
		st['src'] = mote_id
		st['num'] = d2
		starts.append( st )


	if dbg == DBGS_NEW_REMOTE_PAYLOAD:
		nodes[mote_id]['hist'].append( [timestamp, d1] )
		nodes[mote_id]['last'] = d1

		if timestamp < offset:
			offset = timestamp


	if dbg == DBGS_SEQUENCE_INCREASE:
		var_id = "var_%s" % (d1)
		new_seq = d2

		if var_id not in sequences.keys():
			sequences[var_id] = []
		entry = {}
		entry['new_seq'] = new_seq
		entry['timestamp'] = timestamp
		sequences[var_id].append(entry)
		

# find start diff
start_diff = -1
if len(starts) == 2:
	s1 = starts[0]['timestamp']
	s2 = starts[1]['timestamp']

	if s1 > s2:
		start_diff = s1 - s2
		total_time = timestamp - s2
	else:
		start_diff = s2 - s1
		total_time = timestamp - s1

	v1 = starts[0]['num']
	v2 = starts[1]['num']


print "Starting difference: %.3f sec" % (start_diff)
print "Values: %d & %d" % (v1, v2)

ends_lost = 0
ends_with_v1 = 0
ends_with_v2 = 0

motes_sync_delays = []

for mote in nodes.keys():
	n = nodes[mote]

	mote_delay = n["hist"][-1][0] - offset
	motes_sync_delays.append( mote_delay )

	if n['last'] == v1:
		ends_with_v1 = ends_with_v1 + 1
		continue
	
	if n['last'] == v2:
		ends_with_v2 = ends_with_v2 + 1
		continue

	print n["hist"]
	ends_lost = ends_lost + 1

print "Merge Stats"
print "Has value %d -> %d motes ( %.2f %%)" % (v1, ends_with_v1, 
			ends_with_v1 * 100.0 / len(nodes))
print "Has value %d -> %d motes ( %.2f %%)" % (v2, ends_with_v2, 
			ends_with_v2 * 100.0 / len(nodes))
print "Motes lost: %d ( %.2f %%)" % (ends_lost,
			ends_lost * 100.0 / len(nodes))

msd_array = np.array(motes_sync_delays)

results = {}
results["_values"] = [v1, v2]
results["_motes_with_v1"] = ends_with_v1
results["_motes_with_v1_percentage"] = ends_with_v1 * 100.0 / len(nodes)
results["_motes_with_v2"] = ends_with_v2
results["_motes_with_v2_percentage"] = ends_with_v2 * 100.0 / len(nodes)
results["_motes_lost"] = ends_lost
results["_motes_lost_percentage"] = ends_lost * 100.0 / len(nodes)
results["_num_nodes"] = len(nodes.keys())
results["_start_diff"] = start_diff
results["_sequences"] = sequences
results["_total_time"] = total_time
results["all_motes_delays"] = motes_sync_delays
results["_all_motes_delays_max"] = msd_array.max()
results["_all_motes_delays_min"] = msd_array.min()
results["_all_motes_delays_mean"] = msd_array.mean()
results["_all_motes_delays_std"] = msd_array.std()

# save as json
with open("summary_%s" % (sys.argv[2]), 'wb') as fp:
	json.dump(results, fp, sort_keys=True, indent=4)

results["nodes"] = nodes

# save as json
with open("%s" % (sys.argv[2]), 'wb') as fp:
	json.dump(results, fp, sort_keys=True, indent=4)


