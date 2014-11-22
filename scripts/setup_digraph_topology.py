#!/usr/bin/python
# Create graph for 
# Author: Marcin K Szczodrak
# Updated: 5/01/2014

import sys
import os
import json
import yaml

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

if len(sys.argv) != 3:
	print "usage %s <data_to_import> <output.json>\n" % (sys.argv[0])
	exit()

data_module = sys.argv[1]



with open(data_module) as jin:
	content = jin.read()
snapshots = json.loads(content)

print "Loaded snapshots"

G_template = nx.Graph()

for snapshot_id in range(len(snapshots)):
	nodes = snapshots[snapshot_id]['nodes']

	for node_id in snapshots[snapshot_id]['nodes'].keys():
		if node_id not in G_template.nodes():
			G_template.add_node(node_id)

		for neighbor_id in nodes[node_id]['neighborhood'].keys():
			if (node_id, neighbor_id) not in G_template.edges():
				G_template.add_edge(node_id, neighbor_id)

			if neighbor_id not in G_template.nodes():
				G_template.add_node(neighbor_id)

graph_data = {}
graph_data['edges'] = G_template.edges()
graph_data['nodes'] = G_template.nodes()

# save as json
with open(sys.argv[2], 'wb') as fp:
        json.dump(graph_data, fp, sort_keys=True, indent=4)


