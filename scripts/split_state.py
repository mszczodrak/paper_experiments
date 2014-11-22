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

if len(sys.argv) != 3:
	print "usage %s <result.txt> <testbed_conf>"
	sys.exit(1)


f = open(sys.argv[1], "r")

nodes = {}

new_state_logs = {"id":0, "data":[]}
state_logs = {}
state_logs[0] = new_state_logs

testbed_conf_module = sys.argv[2].split("/")[-1].split(".")[0]
path_to_testbed_conf_module = "/".join(sys.argv[2].split("/")[:-1])
sys.path.append(path_to_testbed_conf_module)

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

	if not(mote_id in nodes.keys()):
		new_node = {}
		new_node['states'] = [ {"id":0, "seq":0} ]
		nodes[mote_id] = new_node

	if dbg == DBGS_START:
		new_state = {"id": d1, "seq": d2}
		nodes[mote_id]['states'].append(new_state)
		print "%10d,%03d  [%3d] switches to state %d sequence %d" % (int(l[0]), int(l[1]), mote_id, d1, d2)

		if new_state["seq"] not in state_logs.keys():
			new_state_logs = {"id":d1, "data":[]}
			state_logs[d2] = new_state_logs

		continue

	# get current mote state and seq
	mote_state_id = nodes[mote_id]['states'][-1]['id']
	mote_state_seq = nodes[mote_id]['states'][-1]['seq']


	# Check if state id and sequence match
	if state_logs[mote_state_seq]['id'] != mote_state_id:
		print "Node seq/state (%d/%d) does not match the same sequence global state (%d)" % \
					(mote_state_seq, mote_state_id, state_logs[mote_state_seq]['id'])
		continue
		
	state_logs[mote_state_seq]['data'].append(line)


for state_sequence in state_logs.keys():
	log_name = "state_%d_seq_%d_%s" % (state_logs[state_sequence]['id'], 
						state_sequence, sys.argv[1])	
		
	with open(log_name, 'wb') as fp:
		for line in state_logs[state_sequence]['data']:
			fp.write("%s" % (line))

