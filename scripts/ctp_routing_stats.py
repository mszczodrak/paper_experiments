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

if len(sys.argv) != 5:
	print "usage %s <result.txt> <data.json> <testbed_conf> <root>"
	sys.exit(1)

f = open(sys.argv[1], "r")

nodes = {}

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

	parentChanges = d0
	parent = d1
	etx = d2

	if mote_id > testbed_conf.max_node_id:
		print line
		continue

	if not(mote_id in nodes.keys()):
		new_node = {}
		new_node['update_time'] = []
		new_node['parentChanges'] = 0
		new_node['parent'] = []
		new_node['etx'] = []
		new_node['final_hop'] = -1
		nodes[mote_id] = new_node

	if dbg == DBGS_NETWORK_ROUTING_UPDATE:
		print line
		if nodes[mote_id]['parent'] == [] or \
			nodes[mote_id]['parent'][-1] != parent or \
			nodes[mote_id]['etx'][-1] != etx:
			nodes[mote_id]['update_time'].append(timestamp)
			nodes[mote_id]['parentChanges'] = parentChanges
			nodes[mote_id]['parent'].append(parent)
			nodes[mote_id]['etx'].append(etx)
		continue

if root in nodes.keys():
	nodes[root]['final_hop'] = 0

def assign_hop(node_id, list_of_parents):
	if nodes[node_id]['final_hop'] != -1:
		return nodes[node_id]['final_hop']

	parent = nodes[node_id]['parent'][-1]

	if (parent in list_of_parents) or (parent not in nodes.keys()):
		nodes[node_id]['final_hop'] = float("inf")
		return nodes[node_id]['final_hop']

	if nodes[parent]['final_hop'] == -1:
		list_of_parents.append(parent)
		nodes[parent]['final_hop'] = assign_hop(parent, list_of_parents)

	return nodes[parent]['final_hop'] + 1


for node_id in nodes.keys():
	nodes[node_id]['final_hop'] = assign_hop(node_id, [])

# save as json
with open(sys.argv[2], 'wb') as fp:
	json.dump(nodes, fp, sort_keys=True, indent=4)



