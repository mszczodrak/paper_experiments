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
tx_problem_data = json.loads(content)

# data preprocessing

network_all_congested = []
network_all_not_acked = []

power_txs = []

for power_tx in conf.radio_tx_powers_confs:
	power_txs.append(conf.radio_power_levels[power_tx])

	mote_ids = []
	mote_congested = []
	mote_not_acked = []

	for mote_id in tx_problem_data[power_tx].keys():
		mote_ids.append(mote_id)
		mote_congested.append(len(tx_problem_data[power_tx][mote_id]["congestion_time"]))
		mote_not_acked.append(len(tx_problem_data[power_tx][mote_id]["not_acked_time"]))

	congested = sum(mote_congested)
	not_acked = sum(mote_not_acked)

	network_all_congested.append(congested)
	network_all_not_acked.append(not_acked)


# data plotting

os.mkdir("graph_%s" % (file_name))

for tp in ["full", "short"]:
	data_congested = []
	data_not_acked = []

	if tp == "full":
		x_ticks = range(len(power_txs))
		data_congested = network_all_congested
		data_not_acked = network_all_not_acked
	else:
		x_ticks = range(len(power_txs) - shorter)
		data_congested = network_all_congested[:-shorter]
		data_not_acked = network_all_not_acked[:-shorter]

		
	fig, ax1 = plt.subplots()
	ax1.plot(x_ticks[:len(data_congested)], data_congested, 'k-', label="Congestions")
	ax1.set_ylabel("Detected Congestions")

	ax2 = ax1.twinx()
	ax2.plot(x_ticks[:len(data_not_acked)], data_not_acked, 'b.-', label="Not Acked")
	ax2.set_ylabel("Missed Acknowledgements")

	h1, l1 = ax1.get_legend_handles_labels()
	h2, l2 = ax2.get_legend_handles_labels()

	ax1.legend(h1+h2, l1+l2, loc=2)

	plt.xticks(x_ticks, power_txs)
	plt.xlim(x_ticks[0], x_ticks[-1])
	plt.xlabel("dBm")

	fig.set_size_inches(11, 5)
	fig.subplots_adjust(top=0.99)
	fig.subplots_adjust(hspace=0.5)

	plt.title(fig_title, y=1.12)
	
	for t in ["eps", "pdf", "svg", "png"]:
		filename = "./graph_%s/%s_%s.%s"%(file_name, file_name, tp, t)
		plt.savefig(filename, bbox_inches='tight')


