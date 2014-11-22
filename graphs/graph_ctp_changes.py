#!/usr/bin/python
# Create graph for rssi vs delivery ratio vs acks
# Author: Marcin K Szczodrak
# Updated: 5/01/2014

import sys
import os
import numpy as np
import json
import operator
from pylab import *
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.mlab import bivariate_normal

if len(sys.argv) != 5:
	print "usage %s <data_to_import> <radio_conf> <title> <shorter>\n" % (sys.argv[0])
	exit()

data_module = sys.argv[1]
conf_module = sys.argv[2].split(".")[0]
fig_title = sys.argv[3]
file_name = "_".join(fig_title.split())
shorter = int(sys.argv[4])

try:
	conf = __import__(conf_module)
except:
	print "failed to import %s\n" % (conf_module)
	exit()


with open(data_module) as jin:
	content = jin.read()
ctp_data = json.loads(content)

# data preprocessing

network_all_parent_changes = []
network_all_number_of_parents = []

power_txs = []

for power_tx in conf.radio_tx_powers_confs:
	power_txs.append(conf.radio_power_levels[power_tx])

	mote_ids = []
	mote_parent_changes = []
	mote_num_of_parents = []

	for mote_id in ctp_data[power_tx].keys():
		mote_ids.append(mote_id)
		mote_parent_changes.append(ctp_data[power_tx][mote_id]["parentChanges"])
		mote_num_of_parents.append(len(set(ctp_data[power_tx][mote_id]["parent"])))

	network_all_parent_changes.append(np.array(mote_parent_changes).mean())
	network_all_number_of_parents.append(np.array(mote_num_of_parents).mean())


# data plotting
os.mkdir("graph_%s" % (file_name))

for tp in ["full", "short"]:

	data_parent_changes = []

	if tp == "full":
		x_ticks = range(len(power_txs))
		data_parent_changes = network_all_parent_changes
		data_number_of_parents = network_all_number_of_parents
	else:
		x_ticks = range(len(power_txs) - shorter)
		data_parent_changes = network_all_parent_changes[:-shorter]
		data_number_of_parents = network_all_number_of_parents[:-shorter]

	fig, ax1 = plt.subplots()
	ax1.plot(x_ticks[:len(data_parent_changes)], data_parent_changes, 'k-', label="Parent Changes")
	ax1.set_ylabel("Number of Parent Changes")

	ax2 = ax1.twinx()
	ax2.plot(x_ticks[:len(data_number_of_parents)], data_number_of_parents, 'b.-', label="Number of Parents")
	ax2.set_ylabel("Number of all Parents")

	h1, l1 = ax1.get_legend_handles_labels()
	h2, l2 = ax2.get_legend_handles_labels()

	ax1.legend(h1+h2, l1+l2, loc=2)


	plt.xticks(x_ticks, power_txs)
	plt.xlim(x_ticks[0], x_ticks[-1])
	plt.xlabel("dBm")

	# mark the best result
	max_counter_index, max_counter_value = max(enumerate(data_parent_changes), key=operator.itemgetter(1))
	ax1.plot(x_ticks[max_counter_index], max_counter_value, marker=(5,1), markersize=14, color='k')

	# mark the worst result
	min_counter_index, min_counter_value = min(enumerate(data_parent_changes), key=operator.itemgetter(1))
	ax1.plot(x_ticks[min_counter_index], min_counter_value, marker=(5,1), markersize=14, color='k')

	#plt.ylim(max_counter_value - 15, max_counter_value + 5)
	#plt.ylim(min(network_all_delivered) -2, max(network_all_delivered) + 2)

	fig.set_size_inches(11, 5)
	fig.subplots_adjust(top=0.99)
	fig.subplots_adjust(hspace=0.5)

	plt.title(fig_title, y=1.12)

	for t in ["eps", "pdf", "svg", "png"]:
		filename = "./graph_%s/%s_%s.%s"%(file_name, file_name, tp, t)
		plt.savefig(filename, bbox_inches='tight')


