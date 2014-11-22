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

if len(sys.argv) != 5:
	print "usage %s <data_to_import> <graph_data> <radio_conf> <title>\n" % (sys.argv[0])
	exit()

data_module = sys.argv[1]
graph_module = sys.argv[2]
fig_title = sys.argv[4]
file_name = "_".join(fig_title.split())

if os.path.isdir("graph_%s" % (file_name)):
	sys.exit()

conf_module = sys.argv[3].split("/")[-1][:-3]
module_path = "/".join(sys.argv[3].split("/")[:-1])
sys.path.insert(0, module_path)

try:
	conf = __import__(conf_module)
except:
	print "failed to import %s\n" % (conf_module)
	exit()

with open(graph_module) as jin:
	content = jin.read()
graph_data = json.loads(content)

with open(data_module) as jin:
	content = jin.read()
snapshots = json.loads(content)

print "Loaded snapshots"

fix_edge_weight = 0.5

max_neighborhood_size = 0

G_template = nx.Graph()
G_template.add_nodes_from( graph_data['nodes'] )
G_template.add_edges_from( graph_data['edges'] )

for snapshot_id in range(len(snapshots)):
	n = snapshots[snapshot_id]['max_number_of_neighbors']
	if n > max_neighborhood_size:
		max_neighborhood_size = n

#position = nx.spring_layout(G_template)
position = nx.random_layout(G_template)

print "Finished building graph template"

print "Max Size: %d" % (max_neighborhood_size)

os.mkdir("graph_%s" % (file_name))

for t in ["eps", "pdf", "svg", "png"]:
	os.mkdir("graph_%s/%s" % (file_name, t))

for snapshot_id in range(len(snapshots)):
	print "Snapshot %d" % (snapshot_id)

	fig = plt.figure()
	ax = fig.add_subplot(111)

	nodes = snapshots[snapshot_id]['nodes']

	# data preprocessing

	G = G_template.copy()
	G.remove_edges_from( G.edges() )

	for node_id in nodes.keys():
		node_record = nodes[node_id]
		#G.add_node(node_id)
		for neighbor_id in node_record['neighborhood'].keys():
			G.add_edge(node_id, neighbor_id, weight=fix_edge_weight, alpha=0.5)


	# data plotting
	node_neighbor_size = []

	for node_id in G.nodes():
		if node_id not in nodes.keys():
			node_neighbor_size.append( 0 )
		else:
			node_neighbor_size.append( len(nodes[node_id]['neighborhood'] ) )

	nodes_colors = node_neighbor_size


	nodes = nx.draw_networkx_nodes(G, position, cmap = plt.get_cmap('Blues'),
		node_color = nodes_colors, with_labels=False,
		node_size=100,
		vmin = 0, vmax = max_neighborhood_size)

	edges = nx.draw_networkx_edges(G, position, alpha=0.4)

	plt.colorbar(nodes)
	plt.axis('off')
	plt.title("%s # %d" % (fig_title, snapshot_id), y=1.12)

	fig.subplots_adjust(top=0.99)
	fig.subplots_adjust(hspace=0.5)
	#fig.set_size_inches(11, 5)

	for t in ["eps", "pdf", "svg", "png"]:
		filename = "./graph_%s/%s/%s_%05d.%s" % (file_name, t, file_name, snapshot_id, t)
		plt.savefig(filename, bbox_inches='tight')

	plt.close(fig)

