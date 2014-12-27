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

try:
	testbed_conf = __import__(testbed_conf_module)
except:
	print "failed to import %s\n" % (testbed_conf_module)
	exit()

nodes = {}

max_seq_receive = 0
min_seq_receive = 99

roots = []

for line in f.readlines():
	l = line.split()

	if len(l) != 9:
		continue

	if not l[0].isdigit():
		continue


	timestamp = float("%s.%s" % (l[0], l[1]))
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
		new_node['receive_data'] = {}
		new_node['receive_time'] = {}
		new_node['total_delivered_data'] = 0
		nodes[mote_id] = new_node


	if dbg == DBGS_RECEIVE_DATA:
		if d2 > testbed_conf.max_node_id:
			print line
			continue

                # key for receive source 
		if d1 < 100 and d1 > max_seq_receive:
			max_seq_receive = d1

		if d1 > -1 and d1 < min_seq_receive:
			min_seq_receive = d1

		if d1 > max_seq_receive:
			print "skip"
			continue

                if not(d2 in nodes[mote_id]['receive_data']):
                        data = []
                        nodes[mote_id]['receive_data'][d2] = data
                        nodes[mote_id]['receive_time'][d2] = []

                while(len (nodes[mote_id]['receive_data'][d2]) <= d1):
                        nodes[mote_id]['receive_data'][d2].append('-')
                        nodes[mote_id]['receive_time'][d2].append(0)

		if nodes[mote_id]['receive_data'][d2][d1] == '-':
	                nodes[mote_id]['receive_data'][d2][d1] = d1
	                nodes[mote_id]['receive_time'][d2][d1] = timestamp

		if mote_id not in roots:
			roots.append(mote_id)

print roots


all_send = []
all_receive = []

# adjust min and max for offsets
if max_seq_receive > 3:
	max_seq_receive = max_seq_receive - 1
	min_seq_receive = min_seq_receive + 1

all_send_counter = 0
all_receive_counter = 0

summary = {}
summary["root"] = {}


for root in roots:
	summary["root"][root] = {}

	print "\nroot #%d" % (root)
	sorted_keys = sorted(nodes[root]['receive_data'].keys())

	print sorted_keys

	for src_id in sorted_keys:
		from_src_data = nodes[root]['receive_data'][src_id][min_seq_receive:max_seq_receive]
		print "Node %d :" % (src_id),
		print from_src_data

		summary["root"][root][src_id] = from_src_data
		all_send_counter += len(from_src_data)

		for v in from_src_data:
			if v != '-':
				nodes[root]['total_delivered_data'] = nodes[root]['total_delivered_data'] + 1
				all_receive_counter += 1

#all_receive_counter = nodes[root]['total_delivered_data']


print "\nNumber of nodes: %d\n" % len(nodes.keys())
print "Total: %.5f %%\n\n" % (all_receive_counter * 100.0 / all_send_counter)

# save as json
with open(sys.argv[2], 'wb') as fp:
	json.dump(nodes, fp, sort_keys=True, indent=4)


summary["stats"] = {}
summary["number_of_nodes"] = len(nodes.keys())
summary["stats"]["receive"] = all_receive_counter * 100.0 / all_send_counter

# save as json
with open("summary_%s" % (sys.argv[2]), 'wb') as fp:
	json.dump(summary, fp, sort_keys=True, indent=4)
