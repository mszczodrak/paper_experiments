#!/usr/bin/python

import sys
import os

# usage script sink_id logs

if len(sys.argv) != 3:
	print "usage %s <sink_node_id> <result.txt>"
	sys.exit()

sink_id = int(sys.argv[1])

f = open(sys.argv[2], "r")
base = 40000

node_id = -1

nodes = {}

total_send = 0
total_receive = 0

for line in f.readlines():
	l = line.split()

	if len(l) < 2:
		continue

	layer = l[8]
	process = l[6]
	action = "%s %s" % (l[10], l[11])

	if layer != 'Application':
		continue

	if action != 'Send Data' and action != 'Receive Data':
		continue

	node_id = int(l[3]) - base
	d0 = int(l[-3])
	d1 = int(l[-2])

	if not(node_id in nodes.keys()):
		new_node = {}
		new_node['send_data'] = {}
		new_node['receive_data'] = {}
		nodes[node_id] = new_node


	if action == 'Send Data':
		# key for send destination
		d1 = sink_id
		if not(d1 in nodes[node_id]['send_data']):
			data = []
			nodes[node_id]['send_data'][d1] = data

		while(len (nodes[node_id]['send_data'][d1]) <= d0):
			nodes[node_id]['send_data'][d1].append('-')

		if nodes[node_id]['send_data'][d1][d0] == '-':
			nodes[node_id]['send_data'][d1][d0] = d0
			total_send += 1


	if action == 'Receive Data':
                # key for receive source 
                if not(d1 in nodes[node_id]['receive_data']):
                        data = []
                        nodes[node_id]['receive_data'][d1] = data

                while(len (nodes[node_id]['receive_data'][d1]) <= d0):
                        nodes[node_id]['receive_data'][d1].append('-')

		if nodes[node_id]['receive_data'][d1][d0] == '-':
	                nodes[node_id]['receive_data'][d1][d0] = d0
			total_receive += 1
#


# for each node sending to destination 
for src_id in nodes.keys():
	src = nodes[src_id]

	for dst_id in src['send_data'].keys():
		ok = 0
		fail = 0
		dst = nodes[dst_id]

		print "\n\n"
		print "Node %d send to %d :" % (src_id, dst_id),
		print src['send_data'][dst_id]

		# Check if receiver dst got anything from src
		if src_id in dst['receive_data'].keys():
			print 'Receiver got: ',
			print dst['receive_data'][src_id]
		else:
			print '\t\tAll lost'


print "\n\nTotal: %.3f\n\n" % (total_receive * 100.0 / total_send)


