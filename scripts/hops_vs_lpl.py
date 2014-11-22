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
	print "usage %s <ctp_data.json> <lpl_data.json> <hops_data.json>"
	sys.exit(1)

with open(sys.argv[1], 'r') as fp:
	lpl = json.load(fp)

with open(sys.argv[2], 'r') as fp:
	nodes = json.load(fp)

# Sorting nodes by final_hop
nodes_list = []
for key, value in nodes.iteritems():
	temp = value.copy()
	temp["id"] = key
	nodes_list.append(temp)

sorted_nodes = sorted(nodes_list, key=lambda k: k['final_hop']) 

sorted_hops = {}

for node in sorted_nodes:
	nid = int(node['id'])
	unid = unicode(nid)
	if not unid in lpl.keys():
		continue
	#print "%d %d %f\n" % (nid, node['final_hop'], lpl[unid]['percent_on_time_ms'])
	if node['final_hop'] not in sorted_hops.keys():
		sorted_hops[node['final_hop']] = {'hop': node['final_hop'], 'data':[] }
	sorted_hops[node['final_hop']]['data'].append(float(lpl[unid]['percent_on_time_ms']))

hops = sorted(sorted_hops.keys())

for h in hops:
	data_array = np.array(sorted_hops[h]['data'])
	sorted_hops[h]['num'] = len(sorted_hops[h]['data'])
	sorted_hops[h]['mean'] = data_array.mean()
	sorted_hops[h]['std'] = data_array.std()


for key in ["mean", "std", "num", "hop"]:
	print "%10s\t" % (key),
	for h in hops:
		print "{:10.4f}".format(sorted_hops[h][key]),
	print


saved_hops = {}
for h in hops:
	saved_hops[h] = {}
	saved_hops[h]['num'] = sorted_hops[h]['num']
	saved_hops[h]['mean'] = sorted_hops[h]['mean']
	saved_hops[h]['std'] = sorted_hops[h]['std']
	saved_hops[h]['data'] = sorted_hops[h]['data']

# save as json
with open(sys.argv[3], 'wb') as fp:
	json.dump(sorted_hops, fp, sort_keys=True, indent=4)


