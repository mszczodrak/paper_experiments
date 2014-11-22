#!/usr/bin/python
# Create graph for rssi vs delivery ratio vs acks
# Author: Marcin K Szczodrak
# Updated: 5/01/2014

import sys
import os
import json
import yaml

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

if len(sys.argv) != 4:
	print "usage %s <data_to_import> <radio_conf> <title>\n" % (sys.argv[0])
	exit()

data_module = sys.argv[1]
fig_title = sys.argv[3]
file_name = "_".join(fig_title.split())

conf_module = sys.argv[2].split(".")[0]

try:
	conf = __import__(conf_module)
except:
	print "failed to import %s\n" % (conf_module)
	exit()

with open(data_module) as jin:
	content = jin.read()
#all_rssi_data = json.loads(content)
all_rssi_data = yaml.load(content)

fix_edge_weight = 0.5

max_neighborhood_size = 0

G_template = nx.Graph()

os.mkdir("digraph_%s" % (file_name))

for power_tx in sorted(all_rssi_data.keys()):
	rssi_data = all_rssi_data[power_tx]
	#print "Nodes: %d\n" % (len( rssi_data.keys()))
	for node_id in rssi_data.keys():
		n = rssi_data[node_id]['number_of_neighbors']
		if n > max_neighborhood_size:
			max_neighborhood_size = n

		if node_id not in G_template.nodes():
			G_template.add_node(node_id)

		for neighbor_id in nodes[node_id]['neighbors'].keys():
			if (node_id, neighbor_id) not in G_template.edges():
				G_template.add_edge(node_id, neighbor_id)

position = nx.spring_layout(G_template)
position = nx.random_layout(G_template)

print "Max Size: %d" % (max_neighborhood_size)

for power_tx in sorted(all_rssi_data.keys(), reverse=True):

	print "power " + power_tx

	fig = plt.figure()
	ax = fig.add_subplot(111)

	rssi_data = all_rssi_data[power_tx]

	# data preprocessing

	G = G_template.copy()
	G.remove_edges_from( G.edges() )

	for node_id in rssi_data.keys():
		node_record = rssi_data[node_id]
		#G.add_node(node_id)
		for neighbor_id in node_record['neighbors'].keys():
			G.add_edge(node_id, neighbor_id, weight=fix_edge_weight, alpha=0.5)


	# data plotting

	node_neighbor_size = []

	for node_id in G.nodes():
		if node_id not in rssi_data.keys():
			node_neighbor_size.append( 0 )
		else:
			node_neighbor_size.append( rssi_data[node_id]['number_of_neighbors'] )

	nodes_colors = node_neighbor_size


	nodes = nx.draw_networkx_nodes(G, position, cmap = plt.get_cmap('Blues'),
		node_color = nodes_colors, with_labels=False,
		node_size=100,
		vmin = 0, vmax = max_neighborhood_size)

	edges = nx.draw_networkx_edges(G, position, alpha=0.4)

	cbar = plt.colorbar(nodes)
	cbar.ax.tick_params(labelsize=20)

	plt.axis('off')
	db_val = conf.radio_power_levels[power_tx]
	#plt.title("%s %d db" % (fig_title, db_val), y=1.12)

	fig.subplots_adjust(top=0.99)
	fig.subplots_adjust(hspace=0.5)
	#fig.set_size_inches(11, 5)

	for t in ["eps", "pdf", "svg", "png"]:
		filename = "./digraph_%s/%s_%s.%s" % (file_name, file_name, power_tx, t)
		plt.savefig(filename, bbox_inches='tight')

	plt.close(fig)

