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
max_send_seq = -1

def add_node(mote_id):
	new_node = {}
	new_node['id'] = mote_id
	new_node['send_time'] = {}
	new_node['receive_time'] = {}
	new_node['delays'] = {}
	nodes[mote_id] = new_node

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


	if not(mote_id in nodes.keys()):
		add_node(mote_id)

	if dbg == DBGS_SEND_DATA:
		data_seq = d1
		data_dest = d2
		if data_dest > testbed_conf.max_node_id:
			print line
			continue

		nodes[mote_id]['send_time'][data_seq] = timestamp

		if max_send_seq < data_seq:
			max_send_seq = data_seq


	if dbg == DBGS_RECEIVE_DATA:
		data_seq = d1
		data_from = d2

		if max_send_seq == -1:
			max_send_seq = data_seq

		if data_from > testbed_conf.max_node_id:
			print "Drop 1 " + line
			continue

		if data_seq > max_send_seq + 1:
			print "Drop 2 " + line
			continue

		if data_from not in nodes.keys():
			add_node(data_from)

		nodes[data_from]['receive_time'][data_seq] = timestamp

		if max_send_seq < data_seq:
			max_send_seq = data_seq


for mote_id in nodes.keys():
	for data_seq in nodes[mote_id]['send_time'].keys():
		if data_seq not in nodes[mote_id]['receive_time'].keys():
			continue
		nodes[mote_id]['delays'][data_seq] = nodes[mote_id]['receive_time'][data_seq] - nodes[mote_id]['send_time'][data_seq]


seqs = {}

# for each node sending to destination 
for mote_id in nodes.keys():
	for data_seq in nodes[mote_id]['send_time'].keys():
		if data_seq not in seqs.keys():
			seqs[data_seq] = {}
			seqs[data_seq]['all_delays'] = []
		if data_seq not in nodes[mote_id]['delays'].keys():
			continue
		seqs[data_seq]['all_delays'].append(nodes[mote_id]['delays'][data_seq])

for data_seq in seqs.keys():
	#seqs[data_seq]['min'] = min(seqs[data_seq]['all_delays'])
	seqs[data_seq]['max'] = max(seqs[data_seq]['all_delays'])
	seqs[data_seq]['all_delays'] = sorted(seqs[data_seq]['all_delays'])
	#seqs[data_seq]['avg'] = sum(seqs[data_seq]['all_delays']) * 1.0 / len(seqs[data_seq]['all_delays'])

for data_seq in seqs.keys():
	print "Seq: %3d \t -> %8d" % (data_seq, seqs[data_seq]['max'])

# save as json
with open(sys.argv[2], 'wb') as fp:
	#json.dump(nodes, fp, sort_keys=True, indent=4)
	json.dump(seqs, fp, sort_keys=True, indent=4)

