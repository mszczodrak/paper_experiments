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
		new_node['sending_seq'] = None
		nodes[mote_id] = new_node


	if dbg == DBGS_SEND_DATA:
		seq = d1
		nodes[mote_id]['sending_seq'] = seq
		continue
		

	if dbg == DBGS_RADIO_START_DONE:
		millic = d1 * pow(2,16) + d2
		entry = {}
		entry['millic'] = millic
		entry['sending'] = nodes[mote_id]['sending_seq']
		entry['sending'] = nodes[mote_id]['sending_seq']
		entry['timestamp'] = timestamp
		nodes[mote_id]['start_done_t'].append(entry)
		nodes[mote_id]['sending_seq'] = None


#	if dbg == DBGS_RADIO_STOP_DONE:
#		millic = d1 * pow(2,16) + d2
#		entry = {}
#		entry['millic'] = millic
#		entry['sending'] = nodes[mote_id]['sending_seq']
#		entry['timestamp'] = timestamp
#		nodes[mote_id]['stop_done_t'].append(entry)
#

# save as json
with open(sys.argv[2], 'wb') as fp:
	json.dump(nodes, fp, sort_keys=True, indent=4)


## save as json
#with open("summary_%s" % (sys.argv[2]), 'wb') as fp:
#	json.dump(data_summary, fp, sort_keys=True, indent=4)
