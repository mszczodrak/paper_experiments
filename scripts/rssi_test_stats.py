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

	mote_id = int(l[2])
	version = int(l[3])
	did = int(l[4])
	dbg = int(l[5])
	d0 = int(l[6])
	d1 = int(l[7])
	d2 = int(l[8])

	if not(mote_id in nodes.keys()):
		new_node = {}
		new_node['neighbors'] = {}
		new_node['seqno'] = []
		nodes[mote_id] = new_node

	if dbg == DBGS_RECEIVE_BEACON:
		src = d0
		rssi = d1
		lqi = d2

		if not(src in nodes[mote_id]['neighbors'].keys()):
			neighbor = {}
			neighbor['rssi'] = []
			neighbor['lqi'] = []
			nodes[mote_id]['neighbors'][src] = neighbor

		nodes[mote_id]['neighbors'][src]['rssi'].append(int(rssi))
		nodes[mote_id]['neighbors'][src]['lqi'].append(int(lqi))

	if dbg == DBGS_SEND_DATA:
		error = d0
		seqno = d1
		broadcast = d2
		nodes[mote_id]['seqno'].append(seqno)


# for each node sending to destination 
for mote_id in nodes.keys():
	for neighbor in nodes[mote_id]['neighbors'].keys():
		length = len(np.array(nodes[mote_id]['neighbors'][neighbor]["rssi"]))
		np_rssi = np.array(nodes[mote_id]['neighbors'][neighbor]["rssi"])
		np_lqi = np.array(nodes[mote_id]['neighbors'][neighbor]["lqi"])

		nodes[mote_id]['neighbors'][neighbor]["num"] = length
		nodes[mote_id]['neighbors'][neighbor]["max_rssi"] = np_rssi.max()
		nodes[mote_id]['neighbors'][neighbor]["min_rssi"] = np_rssi.min()
		nodes[mote_id]['neighbors'][neighbor]["avg_rssi"] = np_rssi.mean()
		nodes[mote_id]['neighbors'][neighbor]["std_rssi"] = np_rssi.std()
		nodes[mote_id]['neighbors'][neighbor]["max_lqi"] = np_lqi.max()
		nodes[mote_id]['neighbors'][neighbor]["min_lqi"] = np_lqi.min()
		nodes[mote_id]['neighbors'][neighbor]["avg_lqi"] = np_lqi.mean()
		nodes[mote_id]['neighbors'][neighbor]["std_lqi"] = np_lqi.std()

	nodes[mote_id]['sorted_neighbors_by_rssi'] = [x[0] for x in sorted(nodes[mote_id]['neighbors'].items(),key = lambda x: x[1]["avg_rssi"])]
	nodes[mote_id]['sorted_neighbors_by_rssi'].reverse()

	avg_rssi_array = np.array( [ nodes[mote_id]['neighbors'][x]["avg_rssi"] for x in nodes[mote_id]['neighbors'].keys() ] )
	std_rssi_array = np.array( [ nodes[mote_id]['neighbors'][x]["avg_rssi"] for x in nodes[mote_id]['neighbors'].keys() ] )
	max_rssi_array = np.array( [ nodes[mote_id]['neighbors'][x]["max_rssi"] for x in nodes[mote_id]['neighbors'].keys() ] )
	min_rssi_array = np.array( [ nodes[mote_id]['neighbors'][x]["min_rssi"] for x in nodes[mote_id]['neighbors'].keys() ] )

	if avg_rssi_array.size == 0:
		nodes[mote_id]['avg_rssi'] = None
		nodes[mote_id]['std_rssi'] = None
		nodes[mote_id]['max_rssi'] = None
		nodes[mote_id]['min_rssi'] = None
	else:
		nodes[mote_id]['avg_rssi'] = avg_rssi_array.mean()
		nodes[mote_id]['std_rssi'] = std_rssi_array.std()
		nodes[mote_id]['max_rssi'] = max_rssi_array.max()
		nodes[mote_id]['min_rssi'] = min_rssi_array.min()

	nodes[mote_id]['sorted_neighbors_by_lqi'] = [x[0] for x in sorted(nodes[mote_id]['neighbors'].items(),key = lambda x: x[1]["avg_lqi"])]
	nodes[mote_id]['sorted_neighbors_by_lqi'].reverse()


	avg_lqi_array = np.array( [ nodes[mote_id]['neighbors'][x]["avg_lqi"] for x in nodes[mote_id]['neighbors'].keys() ] )
	std_lqi_array = np.array( [ nodes[mote_id]['neighbors'][x]["avg_lqi"] for x in nodes[mote_id]['neighbors'].keys() ] )
	max_lqi_array = np.array( [ nodes[mote_id]['neighbors'][x]["max_lqi"] for x in nodes[mote_id]['neighbors'].keys() ] )
	min_lqi_array = np.array( [ nodes[mote_id]['neighbors'][x]["min_lqi"] for x in nodes[mote_id]['neighbors'].keys() ] )

	if avg_lqi_array.size == 0:
		nodes[mote_id]['avg_lqi'] = None
		nodes[mote_id]['std_lqi'] = None
		nodes[mote_id]['max_lqi'] = None
		nodes[mote_id]['min_lqi'] = None
	else:
		nodes[mote_id]['avg_lqi'] = avg_lqi_array.mean()
		nodes[mote_id]['std_lqi'] = std_lqi_array.std()
		nodes[mote_id]['max_lqi'] = max_lqi_array.max()
		nodes[mote_id]['min_lqi'] = min_lqi_array.min()

	nodes[mote_id]['number_of_neighbors'] = len(nodes[mote_id]['neighbors'].keys())


for mote_id in nodes.keys():
	print "\nMote %d received total of %d:\n" % (mote_id, nodes[mote_id]['number_of_neighbors'])
	print  "\t", nodes[mote_id]['sorted_neighbors_by_rssi']
	if nodes[mote_id]['avg_rssi'] != None:
		print "\tAvg RSSI %f, LQI %f" % (nodes[mote_id]['avg_rssi'], nodes[mote_id]['avg_lqi'])

	
print "\n\nNumber of nodes: %d\n" % len(nodes.keys())
print "\n\nNetwork Avg neighborhood: %f\n\n" % np.array ( [ len(nodes[x]['neighbors'].keys()) for x in nodes.keys()] ).mean()

# delete rssi and lqi data from memory
for mote_id in nodes.keys():
	for neighbor in nodes[mote_id]['neighbors'].keys():
		nodes[mote_id]['neighbors'][neighbor].pop('rssi', None)
		nodes[mote_id]['neighbors'][neighbor].pop('lqi', None)

# save as json
with open(sys.argv[2], 'wb') as fp:
	json.dump(nodes, fp, sort_keys=True, indent=4)


