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
import copy

# usage script logs

if len(sys.argv) != 4:
	print "usage %s <result.txt> <data.json> <init_power>"
	sys.exit(1)

f = open(sys.argv[1], "r")

default_power = int(float(sys.argv[3]))

nodes = {}

snapshots = []

def setup_init_snapshot(new_snapshot):
	extra_snapshot = copy.deepcopy(new_snapshot)

	for node_id in extra_snapshot['nodes'].keys():
		extra_snapshot['nodes'][node_id]['seqno'] = 0
		extra_snapshot['nodes'][node_id]['radio_tx_power'] = default_power
		extra_snapshot['nodes'][node_id]['last_safe_tx_power'] = [default_power]

	snapshots.append(extra_snapshot)


def take_snapshot(trigger_node, radio_tx_power, neighborhood_count, radio_change):
	new_snapshot = {}
	new_snapshot['node_id'] = trigger_node
	new_snapshot['radio_tx_power'] = radio_tx_power
	new_snapshot['neighborhood_count'] = neighborhood_count
	new_snapshot['radio_change'] = radio_change
	nodes_copy = copy.deepcopy(nodes)

	number_of_neighbors = []
	number_of_poor_neighbors = []

	for node_id in nodes_copy.keys():
		number_of_neighbors.append( nodes_copy[node_id]['status_update']['neighborhood_count'] )
		number_of_poor_neighbors.append( nodes_copy[node_id]['status_update']['neighbors_in_need'] )

	number_of_neighbors_array = np.array( number_of_neighbors )
	number_of_poor_neighbors_array = np.array( number_of_poor_neighbors )

	new_snapshot['avg_number_of_neighbors'] = number_of_neighbors_array.mean()
	new_snapshot['std_number_of_neighbors'] = number_of_neighbors_array.std()
	new_snapshot['max_number_of_neighbors'] = number_of_neighbors_array.max()
	new_snapshot['min_number_of_neighbors'] = number_of_neighbors_array.min()

	new_snapshot['avg_number_of_poor_neighbors'] = number_of_poor_neighbors_array.mean()
	new_snapshot['std_number_of_poor_neighbors'] = number_of_poor_neighbors_array.std()
	new_snapshot['max_number_of_poor_neighbors'] = number_of_poor_neighbors_array.max()
	new_snapshot['min_number_of_poor_neighbors'] = number_of_poor_neighbors_array.min()

	new_snapshot['nodes'] = nodes_copy

	if snapshots == []:
		setup_init_snapshot(new_snapshot)

	snapshots.append(new_snapshot)

	

	print "Took snapshot %d\n" % (len(snapshots))


def add_node(mote_id):
	new_node = {}
	new_node['status_update'] = {
		'neighborhood_count': 0, 'neighbors_in_need': 0
	}
	new_node['seqno'] = 0
	new_node['radio_tx_power'] = None
	new_node['neighborhood'] = {}
	new_node['last_safe_tx_power'] = [default_power]
	nodes[mote_id] = new_node


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
		add_node(mote_id)


	if dbg == DBGS_REMOVE_NODE:
		node_id = d0
		node_id = d1
		node_id = d2

		if node_id in nodes[mote_id]['neighborhood'].keys():
			del nodes[mote_id]['neighborhood'][node_id]

		
	# while updating neighborhood
	if dbg == DBGS_STATUS_UPDATE:
		neighborhood_count = d0
		good_quality_neighbors = d1
		neighbors_in_need = d2

		status = {}
		status['neighborhood_count'] = neighborhood_count
		status['neighbors_in_need'] = neighbors_in_need

		# save all status updates
		#nodes[mote_id]['status_update'].append(status)

		# save old the last update
		nodes[mote_id]['status_update'] = status


	if dbg == DBGS_NEW_CHANNEL:
		process = d0
		neighborhood_count = d1
		last_safe_tx_power = d2
		nodes[mote_id]['last_safe_tx_power'].append(last_safe_tx_power)

	
	# changind radio tx power
	if dbg == DBGS_CHANNEL_RESET:
		proc = d0
		neighborhood_count = d1
		radio_tx_power = d2

		if 'radio_tx_power' not in nodes[mote_id].keys():
			print mote_id
			print line
			print nodes[mote_id]
			sys.exit()

		if radio_tx_power > nodes[mote_id]['radio_tx_power']:
			nodes[mote_id]['radio_tx_power'] = radio_tx_power
			take_snapshot(mote_id, radio_tx_power, neighborhood_count, 'up')
		else:
			nodes[mote_id]['radio_tx_power'] = radio_tx_power
			take_snapshot(mote_id, radio_tx_power, neighborhood_count, 'down')


	if dbg == DBGS_ADD_NODE:
		sender_src = d0
		tx = d1
		hears_us = d2


		if sender_src not in nodes[mote_id]['neighborhood'].keys():
			nodes[mote_id]['neighborhood'][sender_src] = {}

		nodes[mote_id]['neighborhood'][sender_src]['rec'] = 0
		nodes[mote_id]['neighborhood'][sender_src]['seq'] = 0
		nodes[mote_id]['neighborhood'][sender_src]['tx'] = tx
		nodes[mote_id]['neighborhood'][sender_src]['hears_us'] = hears_us



	# add receive node
	if dbg == DBGS_GOT_RECEIVE:
		sender_src = d0
		sender_rec = d1
		sender_sequence = d2

		if sender_src not in nodes[mote_id]['neighborhood'].keys():
			nodes[mote_id]['neighborhood'][sender_src] = {}

		nodes[mote_id]['neighborhood'][sender_src]['rec'] = sender_rec
		nodes[mote_id]['neighborhood'][sender_src]['seq'] = sender_sequence


	# braodcast test was sent
	if dbg == DBGS_SEND_DATA:
		error = d0
		seqno = d1
		radio_tx_power = d2

		nodes[mote_id]['radio_tx_power'] = radio_tx_power
		nodes[mote_id]['seqno'] = seqno


take_snapshot(None, None, None, None)

print "Number of snapshots: %d\n" % (len(snapshots))

# save as json
with open(sys.argv[2], 'wb') as fp:
	json.dump(snapshots, fp, sort_keys=True, indent=4)

