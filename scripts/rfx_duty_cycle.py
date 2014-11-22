#!/usr/bin/python
# Processing dbgs messages from Counter test application
# Author: Marcin K Szczodrak
# Updated; 5/02/2014

import sys
import os
sys.path.append("%s/support/sdk/python" % (os.environ["FENNEC_FOX_LIB"]))
from dbgs_h import *
import numpy as np

# usage script logs

if len(sys.argv) != 2:
	print "usage %s <result.txt>"
	sys.exit(1)

f = open(sys.argv[1], "r")

nodes = {}

total_send = 0
total_receive = 0

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

	time_period = (d1 * pow(2,16) + d2) / 1000

	if not(mote_id in nodes.keys()):
		new_node = {}
		new_node['turnon_period'] = []
		new_node['turnoff_period'] = []
		nodes[mote_id] = new_node


	if dbg == DBGS_RADIO_START_DONE:
		nodes[mote_id]['turnoff_period'].append( time_period )		
		

	if dbg == DBGS_RADIO_STOP_DONE:
		nodes[mote_id]['turnon_period'].append( time_period )		


print '\n\n'

total_on = 0.0
total_off = 0.0
all_on = []
all_off = []


# for each node sending to destination 
for mote_id in nodes.keys():
	on = np.array(nodes[mote_id]['turnon_period'])
	off = np.array(nodes[mote_id]['turnoff_period'])

	nodes[mote_id]['sum_on_time_ms'] = on.sum()
	nodes[mote_id]['sum_off_time_ms'] = off.sum()
	nodes[mote_id]['percent_on_time_ms'] = (100.0 * nodes[mote_id]['sum_on_time_ms']) / \
				( nodes[mote_id]['sum_on_time_ms'] + nodes[mote_id]['sum_off_time_ms'] )
	nodes[mote_id]['mean_on_time_ms'] = on.mean()
	nodes[mote_id]['mean_off_time_ms'] = off.mean()
	nodes[mote_id]['std_on_time_ms'] = on.std()
	nodes[mote_id]['std_off_time_ms'] = off.std()

	total_on += nodes[mote_id]['sum_on_time_ms']
	total_off += nodes[mote_id]['sum_off_time_ms']

	all_on += nodes[mote_id]['turnon_period']
	all_off += nodes[mote_id]['turnoff_period']

	print "\nNode %d:  Time On %.3f   Mean: %.3f   Std: %.3f" % (mote_id,
			nodes[mote_id]['percent_on_time_ms'],
			nodes[mote_id]['mean_on_time_ms'], 
			nodes[mote_id]['std_on_time_ms'])


on_array = np.array(all_on)
off_array = np.array(all_off)
on_sum = on_array.sum()
off_sum = off_array.sum()
on_mean = on_array.mean()
off_mean = off_array.mean()
on_std = on_array.std()
off_std = off_array.std()


print "\n\nTotal: %.3f\n" % (on_sum * 100.0 / (on_sum + off_sum))
print "MeanOn: %.3f  StdOn: %.3f \t\t MeanOff: %.3f  StdOff: %.3f\n\n" % (on_mean,
	on_std, off_mean, off_std)



