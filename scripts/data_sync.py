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
datas = {}
global_vars = {}
global_vars_time = {}
global_hist = []
global_index = []

def add_node(mote_id):
	new_node = {}
	new_node['vars'] = {}
	new_node['hist'] = []
	new_node['index'] = []
	new_node['delay'] = []
	nodes[mote_id] = new_node

experiment_lenght = 0

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
		#print line
		continue


	if not(mote_id in nodes.keys()):
		add_node(mote_id)

	experiment_lenght = timestamp

	if dbg == DBGS_NEW_LOCAL_PAYLOAD:
		var_id = d0
		v = d1
		d = d2

		global_vars[var_id] = {}
		if var_id not in global_vars_time:
			global_vars_time[var_id] = []
		global_vars[var_id]["value"] = d
		global_vars_time[var_id].append({"timestamp":timestamp, "value":d})
		global_hist.append( (var_id, d) )
		global_index.append(v)

		nodes[mote_id]['vars'][var_id] = d
		nodes[mote_id]['hist'].append( (var_id, d) )
		nodes[mote_id]['index'].append(v)


	if dbg == DBGS_NEW_REMOTE_PAYLOAD:
		var_id = d0
		v = d1
		d = d2

		if (var_id, d) not in global_hist:
			global_hist.append( (var_id, d) )
			if var_id not in global_vars_time.keys():
				global_vars_time[var_id] = []

			global_vars_time[var_id].append( {"timestamp":timestamp, "value":d} )

		if (var_id, d) in nodes[mote_id]['hist']:
			continue

		for i in reversed(range(len(global_vars_time[var_id]))):
			var_timestamp = global_vars_time[var_id][i]["timestamp"]
			if global_vars_time[var_id][i]["value"] == d:
				nodes[mote_id]['delay'].append( max(0, timestamp - var_timestamp) )
				break

		if nodes[mote_id]['delay'][-1] > 3:
			print timestamp

		nodes[mote_id]['vars'][var_id] = d
		nodes[mote_id]['hist'].append( (var_id, d) )
		nodes[mote_id]['index'].append(v)



print "Global Hist len %d\n" % (len(global_hist))

#for i in range(len( global_hist )):
#	print "%04d  ID %d  Data %d" % ( i, global_hist[i][0] , global_hist[i][1])

losts = []

for mote_id in nodes.keys():
	print "Mote %d" % (mote_id)
	print "\tLost: ",
	nodes[mote_id]['losts'] = []
	for t in global_hist:
		if t not in nodes[mote_id]['hist']:
			nodes[mote_id]['losts'].append(t)
			if t not in losts:
				losts.append(t)
			print t,

	nodes[mote_id]['lost_count'] = len(nodes[mote_id]['losts'])
	nodes[mote_id]['min_delay'] = min(  nodes[mote_id]['delay'] )
	nodes[mote_id]['avg_delay'] = np.array(  nodes[mote_id]['delay'] ).mean()
	nodes[mote_id]['max_delay'] = max(  nodes[mote_id]['delay'] )
	
	print "\n\tTotal Lost: %d" % ( nodes[mote_id]['lost_count'] )
	print "\tMin Delay: %f" % ( nodes[mote_id]['min_delay'] )
	print "\tAvg Delay: %f" % ( nodes[mote_id]['avg_delay'] )
	print "\tMax Delay: %f" % ( nodes[mote_id]['max_delay'] )
	

skip_loss = []

for lost in losts:
	var_id = lost[0]
	var_value = lost[1]

	last_timestamp = 0
	missing_timestamp = 0

	for i in range(len(global_vars_time[var_id])):
		timestamp = global_vars_time[var_id][i]["timestamp"]
		if global_vars_time[var_id][i]["value"] == var_value:
			missing_timestamp = timestamp
			if (i+1 >= len(global_vars_time[var_id])):
				skip_loss.append(lost) 
			else:
				next_timestamp = global_vars_time[var_id][i+1]["timestamp"]
			break

		last_timestamp = timestamp

	if lost not in skip_loss:		
		print lost,
		print "%f  %f  %f\n" % (last_timestamp, missing_timestamp, next_timestamp)


	for mote in nodes.keys():
		if lost in skip_loss:
			if lost in nodes[mote_id]['losts']:
				nodes[mote_id]['losts'].remove(lost)
				nodes[mote_id]['lost_count'] = len(nodes[mote_id]['losts'])

network_delays = []
network_losts = []

for mote in nodes.keys():
	network_losts.append( nodes[mote_id]['lost_count'] )
	network_delays += nodes[mote_id]['delay']


summary = {}
summary['all'] = nodes
summary['num_of_nodes'] = len(nodes.keys())
summary['num_of_globals'] = len(global_hist)
summary['experiment_length'] = experiment_lenght
summary['min_delay'] = min(network_delays)
summary['avg_delay'] = np.array(network_delays).mean()
summary['max_delay'] = max(network_delays)
summary['min_lost'] = min(network_losts)
summary['avg_lost'] = np.array(network_losts).mean()
summary['max_lost'] = max(network_losts)
summary['chance_of_lost'] = summary['avg_lost'] * 1.0 / (len(global_hist))
summary['avg_new_var_delay'] = summary['experiment_length'] * 1.0 / summary['num_of_globals']

# save as json
with open(sys.argv[2], 'wb') as fp:
	#json.dump(nodes, fp, sort_keys=True, indent=4)
	json.dump(summary, fp, sort_keys=True, indent=4)

del summary['all']

# save as json
with open("summary_%s" % sys.argv[2], 'wb') as fp:
	#json.dump(nodes, fp, sort_keys=True, indent=4)
	json.dump(summary, fp, sort_keys=True, indent=4)




set([x for x in l if l.count(global_hist) > 1])
