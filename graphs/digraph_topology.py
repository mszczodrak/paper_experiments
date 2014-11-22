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
ctp_data = yaml.load(content)

fix_edge_weight = 0.5

max_etx = 0
min_etx = 9999999
default_etx = 100

G_template = nx.DiGraph()

for power_tx in sorted(ctp_data.keys()):
	ctp_d = ctp_data[power_tx]
	#print "Nodes: %d\n" % (len( ctp_d.keys()))
	for node_id in ctp_d.keys():
		if len(ctp_d[node_id]['etx']) > 0:
			etx = int(float(ctp_d[node_id]['etx'][-1]))
			if max_etx < etx:
				max_etx = etx

			if min_etx > etx:
				min_etx = etx
		else:
			etx = None

		if len(ctp_d[node_id]['parent']) > 0:
			parent = int(float(ctp_d[node_id]['parent'][-1]))
		else:
			parent = None
		
		if node_id not in G_template.nodes():
			G_template.add_node(int(float(node_id)))

		if parent != None:
			if parent not in G_template.nodes():
				G_template.add_node(int(float(parent)))

position = None

max_etx = default_etx
print "Max ETX: %d" % (max_etx)
print "Min ETX: %d" % (min_etx)

os.mkdir("digraph_%s" % (file_name))

for power_tx in sorted(ctp_data.keys()): #, reverse=True):

	print "power " + power_tx

	fig = plt.figure()
	ax = fig.add_subplot(111)

	ctp_d = ctp_data[power_tx]

	# data preprocessing

	G = G_template.copy()
	G.remove_edges_from( G.edges() )

	for node_id in ctp_d.keys():
		if len(ctp_d[node_id]['parent']) > 0:
			parent = int(float(ctp_d[node_id]['parent'][-1]))
			G.add_edge(int(float(node_id)), parent) #, weight=fix_edge_weight, alpha=0.5)
		else:
			parent = None

		node_record = ctp_d[node_id]
		#G.add_node(node_id)
#		for neighbor_id in node_record['neighbors'].keys():
#			G.add_edge(node_id, neighbor_id, weight=fix_edge_weight, alpha=0.5)
#
#
	# data plotting

	if position == None:
		#position = nx.spring_layout(G)
		position = nx.graphviz_layout(G)

	node_etx = []

	for node_id in G.nodes():
		if node_id not in ctp_d.keys():
			node_etx.append( default_etx )
		else:
			if len(ctp_d[node_id]['etx']) > 0:
				if ctp_d[node_id]['etx'][-1] > max_etx:
					node_etx.append( max_etx )
				else:
					node_etx.append( ctp_d[node_id]['etx'][-1] )
			else:
				node_etx.append( default_etx )

	nodes_colors = node_etx

	nodes = nx.draw_networkx_nodes(G, position, cmap = plt.get_cmap('Blues'),
		node_color = nodes_colors, with_labels=False,
		node_size=100,
		vmin = 0, vmax = max_etx)

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

