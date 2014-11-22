#!/usr/bin/python
# Marcin K Szczodrak
# Updated on 4/24/2014

import sys
import csv
import os
sys.path.append("%s/support/sdk/python" % (os.environ["FENNEC_FOX_LIB"]))
from dbgs_h import *
import numpy as np
import json


flocklab_log_length = 3

if len(sys.argv) != 5:
	print("\nusage: %s <powerprofilingstats.csv> <data.json> <testbed_conf> <root>\n\n");
	sys.exit(1)

f = open(sys.argv[1], "r")

testbed_conf_module = sys.argv[3].split("/")[-1].split(".")[0]
path_to_testbed_conf_module = "/".join(sys.argv[3].split("/")[:-1])
sys.path.append(path_to_testbed_conf_module)
root = int(float(sys.argv[4]))

try:
	testbed_conf = __import__(testbed_conf_module)
except:
	print "failed to import %s\n" % (testbed_conf_module)
	exit()



all_lines = [line.split(",") for line in f.readlines()]
all_lines.sort(key=lambda x: x[0] )

nodes = {}
sum_mean_mA = 0.0
all_mean_mA = []

for l in all_lines:
	if len(l) != flocklab_log_length:
		continue

	if not l[0][0].isdigit():
		continue

	try:
		#timestamp = l[0].split(".")
		#timestamp_sec = int(float(timestamp[0]))
		#timestamp_micro = int(float(timestamp[1]))
		mote_id = int(float(l[0]))
		mean_mA = float(l[2])

	except:
		continue

	if mote_id > testbed_conf.max_node_id:
		print line
		continue

	if mote_id == root:
		continue

	if mean_mA < 0.1:
		continue

	if not(mote_id in nodes.keys()):
		new_node = {}
		new_node['mean_mA'] = None
		nodes[mote_id] = new_node

	nodes[mote_id]['mean_mA'] = mean_mA
	sum_mean_mA = sum_mean_mA + mean_mA
	all_mean_mA.append(mean_mA)

avg = {}
avg['all'] = nodes
avg['sum_mean_mA'] = sum_mean_mA
avg['min_mean_mA'] = min(all_mean_mA)
avg['max_mean_mA'] = max(all_mean_mA)
avg['num_nodes'] = len(nodes.keys())
avg['network_mean_mA'] = np.array(all_mean_mA).mean() 


print "\n\nTotal Power: %.5f mA\n" % ( avg['sum_mean_mA'] )
print "Number of Nodes: %d\n" % ( avg['num_nodes'] )
print "Average Power: %.5f mA\n\n" % ( avg['network_mean_mA'] )

# save as json
with open(sys.argv[2], 'wb') as fp:
	json.dump(avg, fp, sort_keys=True, indent=4)



