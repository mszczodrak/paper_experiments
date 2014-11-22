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

if len(sys.argv) != 4:
	print "usage %s <data_to_import> <radio_conf> <title>\n" % (sys.argv[0])
	exit()

data_module = sys.argv[1]
conf_module = sys.argv[2].split(".")[0]
fig_title = sys.argv[3]
file_name = "_".join(fig_title.split())

try:
	conf = __import__(conf_module)
except:
	print "failed to import %s\n" % (conf_module)
	exit()


with open(data_module) as jin:
	content = jin.read()
rssi_data = json.loads(content)

# data preprocessing

network_all_rssi = []
network_all_neighborhood = []
network_5best_rssi = []
network_10best_rssi = []
network_15best_rssi = []

all_rssi_per_power = []
all_neighborhood_per_power = []
best_5_rssi_per_power = []
best_10_rssi_per_power = []
best_15_rssi_per_power = []

power_txs = []

for power_tx in conf.radio_tx_powers_confs:
	power_txs.append(conf.radio_power_levels[power_tx])

	avg_rssi = []
	best_5_rssi = []
	best_10_rssi = []
	best_15_rssi = []
	number_of_neighbors = []
	for mote_id in rssi_data[power_tx].keys():
		if rssi_data[power_tx][mote_id]["avg_rssi"] != None:
			avg_rssi.append(rssi_data[power_tx][mote_id]["avg_rssi"])
		number_of_neighbors.append(len(rssi_data[power_tx][mote_id]["neighbors"]))
		rssi_neighborhood = []
		for neighbor in rssi_data[power_tx][mote_id]["neighbors"].keys():
			if rssi_data[power_tx][mote_id]["neighbors"][neighbor]["avg_rssi"] != None:
				rssi_neighborhood.append(rssi_data[power_tx][mote_id]["neighbors"][neighbor]["avg_rssi"])

		rssi_neighborhood = sorted(rssi_neighborhood, reverse=True)
		if len(rssi_neighborhood) >= 15:
			best_15_rssi.append(rssi_neighborhood[:15])

		if len(rssi_neighborhood) >= 10:
			best_10_rssi.append(rssi_neighborhood[:10])

		if len(rssi_neighborhood) >= 5:
			best_5_rssi.append(rssi_neighborhood[:5])
		
	network_all_rssi.append(avg_rssi)
	network_all_neighborhood.append(number_of_neighbors)
	network_5best_rssi.append(best_5_rssi)
	network_10best_rssi.append(best_10_rssi)
	network_15best_rssi.append(best_15_rssi)

	if avg_rssi != []:
		all_rssi_per_power.append(np.array(avg_rssi).mean())

	if number_of_neighbors != []:
		all_neighborhood_per_power.append(np.array(number_of_neighbors).mean())

	if best_5_rssi != []:
		best_5_rssi_per_power.append(np.array(best_5_rssi).mean())

	if best_10_rssi != []:
		best_10_rssi_per_power.append(np.array(best_10_rssi).mean())

	if best_15_rssi != []:
		best_15_rssi_per_power.append(np.array(best_15_rssi).mean())
	
		

# data plotting

fig, ax1 = plt.subplots()
x_ticks = range(len(power_txs))
ax1.plot(x_ticks[:len(all_rssi_per_power)], all_rssi_per_power, '-', label='All')
ax1.plot(x_ticks[:len(best_5_rssi_per_power)], best_5_rssi_per_power, '-', label='Best 5')
ax1.plot(x_ticks[:len(best_10_rssi_per_power)], best_10_rssi_per_power, '-', label='Best 10')
ax1.plot(x_ticks[:len(best_15_rssi_per_power)], best_15_rssi_per_power, '-', label='Best 15')
ax1.set_ylabel("RSSI")
ax1.legend()

plt.xticks(x_ticks, power_txs)
plt.xlim(x_ticks[0], x_ticks[-1])
plt.xlabel("dBm")

ax2 = ax1.twiny()
plt.xticks(x_ticks[0:len(all_neighborhood_per_power)], ["%.1f"%(x) for x in all_neighborhood_per_power])
plt.xlim(x_ticks[0], x_ticks[-1])
#ymax = max(all_rssi_per_power) + 5
#ymin = max(all_rssi_per_power) - 10
#plt.ylim(ymin, ymax)
plt.xlabel("Average Neighborhood Size")

fig.set_size_inches(11, 5)
fig.subplots_adjust(top=0.99)
fig.subplots_adjust(hspace=0.5)

plt.title(fig_title, y=1.12)

os.mkdir("graph_%s" % (file_name))

for t in ["eps", "pdf", "svg", "png"]:
	filename = "./graph_%s/%s.%s"%(file_name, file_name, t)
	plt.savefig(filename, bbox_inches='tight')


