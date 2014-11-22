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
	print "usage %s <result.txt> <data.json>"
	sys.exit(1)

f = open(sys.argv[1], "r")

nodes = {}

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


	if not(mote_id in nodes.keys()):
		new_node = {}
		new_node['congestion_time'] = []
		new_node['not_acked_time'] = []
		nodes[mote_id] = new_node

	if dbg == DBGS_CONGESTION:
		nodes[mote_id]['congestion_time'].append(timestamp)
		continue

	if dbg == DBGS_NOT_ACKED:
		nodes[mote_id]['not_acked_time'].append(timestamp)
		continue


total_congestions = []
total_not_acks = []

# for each node sending to destination 
for mote_id in nodes.keys():
	print "Mote %d  Congestions: %d  Not Acked: %d" % (mote_id,
			len(nodes[mote_id]['congestion_time']),
			len(nodes[mote_id]['not_acked_time']))

	total_congestions.append(len(nodes[mote_id]['congestion_time']))
	total_not_acks.append(len(nodes[mote_id]['not_acked_time']))

total_congestions.sort()
total_not_acks.sort()
five_percent = len(nodes.keys()) * 5 / 100

array_congestions = np.array(total_congestions[five_percent:-five_percent])
array_not_acks = np.array(total_not_acks[five_percent:-five_percent])

print "\n\nNumber of nodes: %d\n" % len(nodes.keys())
print "\nNetwork Congestions: %d  Not Acked: %d\n" % (sum(total_congestions), sum(total_not_acks))
print "\nNetwork Total\nCongestions: mean: %f std: %f sum: %f\n\
Not Acked: mean: %f std: %f sum: %f\n\n" % (
array_congestions.mean(), array_congestions.std(), array_congestions.sum(),
array_not_acks.mean(), array_not_acks.std(), array_not_acks.sum())

# save as json
with open(sys.argv[2], 'wb') as fp:
	json.dump(nodes, fp, sort_keys=True, indent=4)

