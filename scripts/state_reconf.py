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
	print "usage %s <result.txt> <state.json> <testbed_conf>"
	sys.exit(1)


f = open(sys.argv[1], "r")

testbed_conf_module = sys.argv[3].split("/")[-1].split(".")[0]
path_to_testbed_conf_module = "/".join(sys.argv[3].split("/")[:-1])
sys.path.append(path_to_testbed_conf_module)

try:
	testbed_conf = __import__(testbed_conf_module)
except:
	print "failed to import %s\n" % (testbed_conf_module)
	exit()


states = {}
motes_ids = []


for line in f.readlines():
	l = line.split()

	if len(l) != 9:
		continue

	if not l[0].isdigit():
		continue

	timestamp = int(l[0]) * 1000.0 + int(l[1]) 
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

	if dbg != DBGS_START:
		continue

	state_id = d1
	state_seq = d2

	if state_seq not in states.keys():
		new_state = {"id": state_id, "seq": state_seq, "nodes": {} }
		states[state_seq] = new_state

	states[state_seq]["nodes"][mote_id] = timestamp

	if mote_id not in motes_ids:
		motes_ids.append(mote_id)


for state_seq in states.keys():
	first_timestamp = 9999999999999
	last_timestamp = 0
	number_of_nodes = len(states[state_seq]["nodes"].keys())

	for mote_id in states[state_seq]["nodes"].keys():
		timestamp = states[state_seq]["nodes"][mote_id]
		if timestamp < first_timestamp:
			first_timestamp = timestamp

		if timestamp > last_timestamp:
			last_timestamp = timestamp

	states[state_seq]['start_time_ms'] = first_timestamp
	states[state_seq]['stop_time_ms'] = last_timestamp
	states[state_seq]['reconf_time_ms'] = last_timestamp - first_timestamp
	states[state_seq]['number_of_nodes'] = number_of_nodes
	states[state_seq]['reconf_success'] = number_of_nodes * 100.0 / len(motes_ids)


# save as json
with open(sys.argv[2], 'wb') as fp:
	json.dump(states, fp, sort_keys=True, indent=4)

