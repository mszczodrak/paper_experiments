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
global_records = []

def add_node(mote_id):
	new_node = {}
	new_node['vars'] = {}
	new_node['hist'] = []
	new_node['delay'] = []
	nodes[mote_id] = new_node

experiment_lenght = 0

def find_record(var_id, data):
	for i in reversed(range(len(global_records))): 
		r = global_records[i]

		if r["var_id"] == var_id and r["data"] == data:
			return r

	return {}


def add_record(mote_id, var_id, data, timestamp):
	new_record = {}
	new_record["data"] = data
	new_record["var_id"] = var_id
	new_record["mote_id"] = mote_id
	new_record["timestamp"] = timestamp
	new_record["receivers"] = []
	new_record["receivers_timestamps"] = []

	global_records.append(new_record)


def add_to_receivers(data, var_id, mote_id, timestamp):
	new_receiver = {}
	new_receiver["mote_id"] = mote_id
	new_receiver["timestamp"] = timestamp

	for i in reversed(range(len(global_records))):
		if global_records[i]["data"] == data and global_records[i]["var_id"] == var_id:
			for rec_record in global_records[i]["receivers"]:
				if rec_record["mote_id"] == mote_id:
					return

			global_records[i]["receivers"].append(new_receiver)
			global_records[i]["receivers_timestamps"].append(timestamp)
			return

	print "Nothing??"


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
		continue

	if not(mote_id in nodes.keys()):
		add_node(mote_id)

	experiment_lenght = timestamp

	if dbg == DBGS_NEW_LOCAL_PAYLOAD:
		var_id = d0
		data = d2

		r = find_record(var_id, data)
		if r == {}:
			add_record(mote_id, var_id, data, timestamp)
		else:
			r["mote_id"] = mote_id


	if dbg == DBGS_NEW_REMOTE_PAYLOAD:
		var_id = d0
		conflict = d1
		data = d2

		nodes[mote_id]['hist'].append( (var_id, data) )

		r = find_record(var_id, data)
		if r == {}:
			add_record(0, var_id, data, timestamp)
			r = find_record(var_id, data)

		add_to_receivers(data, var_id, mote_id, timestamp)


network_delays = []
network_losts = []
network_overwrote = []

num_of_nodes = len(nodes.keys())

for r in global_records:
	r["receivers"] = sorted(r["receivers"], key=lambda k: k["mote_id"])
	r["receivers_delay"] = sorted([x - r["timestamp"] for x in r["receivers_timestamps"]])
	delays = np.array( r["receivers_delay"] )
	r["delay_avg"] = delays.mean()
	r["delay_std"] = delays.std()
	r["delay_max"] = delays.max()
	lost = num_of_nodes - len(r["receivers_delay"])
	if lost == (num_of_nodes - 1):
		r["receivers_miss"] = 0 
		r["overwrote"] = lost
	else:
		r["receivers_miss"] = lost
		r["overwrote"] = 0

#	print "%d - %d" % (num_of_nodes, len(r["receivers_delay"]) )
#	print "Data %d \t Var %d \t Mote %d \t Timestamp %d\t Missed %d" % (r["data"],
#						r["var_id"],
#						r["mote_id"],
#						r["timestamp"],
#						r["receivers_miss"])

	network_delays +=  r["receivers_delay"] 
	network_losts.append( r["receivers_miss"] )
	network_overwrote.append( r["overwrote"] )


network_delays = sorted(network_delays)
network_losts = sorted(network_losts)

print network_losts

len_delay_75 = len(network_delays) * 75 / 100
len_delay_95 = len(network_delays) * 95 / 100
len_delay_99 = len(network_delays) * 99 / 100

len_lost_75 = len(network_losts) * 75 / 100
len_lost_95 = len(network_losts) * 95 / 100
len_lost_99 = len(network_losts) * 99 / 100


summary = {}
summary['all'] = nodes
summary['num_of_nodes'] = len(nodes.keys())
summary['num_of_globals'] = len(global_records)
summary['experiment_length'] = experiment_lenght
summary['min_delay'] = min(network_delays)
summary['avg_delay'] = np.array(network_delays).mean()
summary['avg_delay_75'] = np.array(network_delays[:len_delay_75]).mean()
summary['avg_delay_95'] = np.array(network_delays[:len_delay_95]).mean()
summary['avg_delay_99'] = np.array(network_delays[:len_delay_99]).mean()
summary['max_delay'] = max(network_delays)
summary['min_lost'] = min(network_losts)
summary['avg_lost'] = np.array(network_losts).mean()
summary['avg_lost_95'] = np.array(network_losts[:len_lost_95]).mean()
summary['avg_lost_99'] = np.array(network_losts[:len_lost_99]).mean()
summary['max_lost'] = max(network_losts)
summary['chance_of_lost'] = summary['avg_lost'] * 1.0 / summary['num_of_globals']
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


