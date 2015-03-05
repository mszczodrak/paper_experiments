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
		nodes[mote_id]['hist'].append( [timestamp, [d1,d2]] )
		nodes[mote_id]['last'] = [d1, d2]
		#print timestamp
		pass


# find start diff
start_diff = -1
merge_vars = []
if len(starts) == 2:
	s1 = starts[0]['timestamp']
	s2 = starts[1]['timestamp']

	if s1 > s2:
		start_diff = s1 - s2
	else:
		start_diff = s2 - s1

	d1 = starts[0]['num']
	d2 = starts[1]['num']

	if d1 > d2:
		merge_vars = [d1, d2]
	else:
		merge_vars = [d2, d1]
		

print "Starting difference: %.3f sec" % (start_diff)
print merge_vars

none = 0
mixed = 0
match = 0

for mote in nodes.keys():
	n = nodes[mote]
	if n['last'] == merge_vars:
		match = match + 1
		continue
	
	if n['last'] == []:
		none = none + 1
		continue

	print n["hist"]
	mixed = mixed + 1

print "Merge Stats: Match %d   Mixed %d   None %d" % (match, mixed, none)

results = {}
results["mixed_merge"] = mixed
results["none_merge"] = none
results["match_merge"] = match
results["num_nodes"] = len(nodes.keys())
results["start_diff"] = start_diff

# save as json
with open("summary_%s" % (sys.argv[2]), 'wb') as fp:
	json.dump(results, fp, sort_keys=True, indent=4)

results["nodes"] = nodes

# save as json
with open("%s" % (sys.argv[2]), 'wb') as fp:
	json.dump(results, fp, sort_keys=True, indent=4)


