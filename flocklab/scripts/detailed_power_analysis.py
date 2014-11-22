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


flocklab_log_length = 4

if len(sys.argv) != 6:
	print("\nusage: %s <powerprofilingstats.csv> <data.json> <testbed_conf> <root> <SPS>\n\n");
	sys.exit(1)

f = open(sys.argv[1], "r")

testbed_conf_module = sys.argv[3].split("/")[-1].split(".")[0]
path_to_testbed_conf_module = "/".join(sys.argv[3].split("/")[:-1])
sys.path.append(path_to_testbed_conf_module)
root = int(float(sys.argv[4]))
SPS = float(sys.argv[5])

try:
	testbed_conf = __import__(testbed_conf_module)
except:
	print "failed to import %s\n" % (testbed_conf_module)
	exit()



all_lines = [line.split(",") for line in f.readlines()]
all_lines.sort(key=lambda x: x[0] )

nodes = {}
first_time = None
sum_mean_mA = 0.0

line_no = 0

for l in all_lines:
	line_no += 1
	if len(l) != flocklab_log_length:
		continue

	if not l[0][0].isdigit():
		continue

	try:
		timestamp = float(l[0])
		if first_time == None:
			first_time = timestamp
		timestamp = timestamp - first_time
		if timestamp < 0:
			print "Error: Negative Timestamp"
			sys.exit(1)

		mote_id = int(float(l[1]))
		value_mA = float(l[3])

	except:
		continue

	if mote_id > testbed_conf.max_node_id:
		print line
		continue

	if mote_id == root:
		continue

	if value_mA < 0.01:
		#print "[%d] Skip value %d " % (line_no, value_mA),
		#print l
		#continue
		pass

	if not(mote_id in nodes.keys()):
		new_node = {}
		new_node['timestamp'] = []
		new_node['value_mA'] = []
		nodes[mote_id] = new_node

	nodes[mote_id]['value_mA'].append(value_mA)
	nodes[mote_id]['timestamp'].append(timestamp)

print "\n\n"

network_sum_mean_mA = 0.0
network_sum_mean_mA_75 = 0.0
network_sum_mean_mA_90 = 0.0

network_sum_total_mA = 0.0
network_sum_total_mA_75 = 0.0
network_sum_total_mA_90 = 0.0

network_total_time = 0.0
network_total_time_75 = 0.0
network_total_time_90 = 0.0

for node_id in nodes.keys():
	nodes[node_id]['total_time'] = nodes[node_id]['timestamp'][-1] - nodes[node_id]['timestamp'][0]
	nodes[node_id]['total_mA'] = sum(nodes[node_id]['value_mA'])
	nodes[node_id]['mean_mA'] = nodes[node_id]['total_mA'] / nodes[node_id]['total_time'] / SPS
	
	print "Node %d   Total Time: %4.5f   Total mA:  %4.5f   Mean mA: %4.5f" % (node_id, 
			nodes[node_id]['total_time'], nodes[node_id]['total_mA'], nodes[node_id]['mean_mA'])

	len75 = 75 * len(nodes[node_id]['timestamp']) / 100
	len90 = 90 * len(nodes[node_id]['timestamp']) / 100

	nodes[node_id]['total_time_75'] = nodes[node_id]['timestamp'][-1] - nodes[node_id]['timestamp'][-len75]
	nodes[node_id]['total_mA_75'] = sum(nodes[node_id]['value_mA'][-len75:])
	nodes[node_id]['mean_mA_75'] = nodes[node_id]['total_mA_75'] / nodes[node_id]['total_time_75'] / SPS

	nodes[node_id]['total_time_90'] = nodes[node_id]['timestamp'][-1] - nodes[node_id]['timestamp'][-len90]
	nodes[node_id]['total_mA_90'] = sum(nodes[node_id]['value_mA'][-len90:])
	nodes[node_id]['mean_mA_90'] = nodes[node_id]['total_mA_90'] / nodes[node_id]['total_time_90'] / SPS

	print "  Last 75%%            %4.5f              %4.5f             %4.5f" % ( nodes[node_id]['total_time_75'], 
			nodes[node_id]['total_mA_75'], nodes[node_id]['mean_mA_75'])

	print "  Last 90%%            %4.5f              %4.5f             %4.5f" % ( nodes[node_id]['total_time_90'], 
			nodes[node_id]['total_mA_90'], nodes[node_id]['mean_mA_90'])

	network_sum_mean_mA = network_sum_mean_mA + nodes[node_id]['mean_mA']
	network_sum_mean_mA_75 = network_sum_mean_mA_75 + nodes[node_id]['mean_mA_75']
	network_sum_mean_mA_90 = network_sum_mean_mA_90 + nodes[node_id]['mean_mA_90']

	network_sum_total_mA = network_sum_total_mA + nodes[node_id]['total_mA']
	network_sum_total_mA_75 = network_sum_total_mA_75 + nodes[node_id]['total_mA_75']
	network_sum_total_mA_90 = network_sum_total_mA_90 + nodes[node_id]['total_mA_90']

	network_total_time = network_total_time + nodes[node_id]['total_time']
	network_total_time_75 = network_total_time_75 + nodes[node_id]['total_time_75']
	network_total_time_90 = network_total_time_90 + nodes[node_id]['total_time_90']

avg = {}
avg['sum_mean_mA'] = network_sum_mean_mA
avg['sum_mean_mA_75'] = network_sum_mean_mA_75
avg['sum_mean_mA_90'] = network_sum_mean_mA_90

avg['sum_total_mA'] = network_sum_total_mA
avg['sum_total_mA_75'] = network_sum_total_mA_75
avg['sum_total_mA_90'] = network_sum_total_mA_90

avg['total_time'] = network_total_time
avg['total_time_75'] = network_total_time_75
avg['total_time_90'] = network_total_time_90

avg['num_nodes'] = len(nodes.keys())
avg['SPS'] = SPS

print "Network sum_total_mA %4.5f:    75%%  %4.5f" % (avg['sum_total_mA'], avg['sum_total_mA_75'])
print "Network sum_mean_mA  %4.5f:    75%%  %4.5f" % (avg['sum_mean_mA'], avg['sum_mean_mA_75'])
print "Network sum_mean_mA  %4.5f:    90%%  %4.5f" % (avg['sum_mean_mA'], avg['sum_mean_mA_90'])
print "Avg %4.5f   90%%  %4.5f    75%%   %4.5f" % (avg['sum_mean_mA'] / avg['num_nodes'], 
					avg['sum_mean_mA_90'] / avg['num_nodes'],
					avg['sum_mean_mA_75'] / avg['num_nodes'])


with open(sys.argv[2], 'wb') as fp:
	json.dump(nodes, fp, sort_keys=True, indent=4)

# save as json
with open("average_%s" % (sys.argv[2]), 'wb') as fp:
	json.dump(avg, fp, sort_keys=True, indent=4)


