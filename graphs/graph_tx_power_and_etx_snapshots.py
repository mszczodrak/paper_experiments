#!/usr/bin/python
# Create graph for rssi vs delivery ratio vs acks
# Author: Marcin K Szczodrak
# Updated: 5/01/2014

import sys
import os
import numpy as np
import json
import yaml
import operator
from pylab import *
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.mlab import bivariate_normal

if len(sys.argv) != 5:
	print "usage %s <data_to_import> <radio_conf> <etx_threshold> <title>\n" % (sys.argv[0])
	exit()

data_module = sys.argv[1]
fig_title = sys.argv[4]
etx_threshold = int(float(sys.argv[3]))
file_name = "_".join(fig_title.split())

conf_module = sys.argv[2].split("/")[-1][:-3]
module_path = "/".join(sys.argv[2].split("/")[:-1])

sys.path.insert(0, module_path)

try:
	conf = __import__(conf_module)
except:
	print "failed to import %s\n" % (conf_module)
	exit()

if os.path.isdir("graph_%s" % (file_name)):
	sys.exit()

with open(data_module) as jin:
	content = jin.read()

snapshots = json.loads(content)
#snapshots = yaml.load(content)

# data preprocessing

all_power_max = []
all_power_min = []
all_power_std = []
all_power_avg = []

all_etx_max = []
all_etx_min = []
all_etx_std = []
all_etx_avg = []

all_good_etx_max = []
all_good_etx_min = []
all_good_etx_std = []
all_good_etx_avg = []

N = range(len(snapshots))

for snapshot_id in N:
	snapshot = snapshots[snapshot_id]
	nodes = snapshot['nodes']

	radio_tx_powers = []
	all_etx = []
	best_etx = []

	for node_id in nodes.keys():
		if 'radio_tx_power' in nodes[node_id].keys():
			rtp = nodes[node_id]['radio_tx_power']
			if rtp == None:
				radio_index = 0
			else:
				rtp_str = "%02d" % (rtp)
				radio_index = conf.radio_power_index[rtp_str]
		else:
			radio_index = 0

		radio_tx_powers.append( radio_index )


		if 'neighborhood' not in nodes[node_id].keys():
			continue

		per_node_all_etx = []
		per_node_best_etx = []

		for neighbor_id in nodes[node_id]['neighborhood'].keys():		
			e = int(float(nodes[node_id]['neighborhood'][neighbor_id]['etx']))
			per_node_all_etx.append(e)
			if e >= etx_threshold:
				per_node_best_etx.append(e)

		if len(per_node_all_etx) > 0:
			per_node_all_etx_array = np.array( per_node_all_etx )
			mean_all_etx = per_node_all_etx_array.mean()
			all_etx.append(mean_all_etx)

		if len(per_node_best_etx) > 0:
			per_node_all_best_array = np.array( per_node_best_etx )
			mean_best_etx = per_node_all_best_array.mean()
			best_etx.append(mean_best_etx)

	radio_tx_powers_array = np.array( radio_tx_powers )
	all_power_max.append( radio_tx_powers_array.max() )
	all_power_min.append( radio_tx_powers_array.min() )
	all_power_std.append( radio_tx_powers_array.std() )
	all_power_avg.append( radio_tx_powers_array.mean() )

	all_etx_array = np.array( all_etx )
	all_etx_max.append( all_etx_array.max() )
	all_etx_min.append( all_etx_array.min() )
	all_etx_std.append( all_etx_array.std() )
	all_etx_avg.append( all_etx_array.mean() )

	best_etx_array = np.array( best_etx )
	all_good_etx_max.append( best_etx_array.max() )
	all_good_etx_min.append( best_etx_array.min() )
	all_good_etx_std.append( best_etx_array.std() )
	all_good_etx_avg.append( best_etx_array.mean() )

# data plotting

os.mkdir("graph_%s" % (file_name))

# TX POWER

fig, ax1 = plt.subplots()
ax1.plot(N, all_power_max, '-', label='Max')
ax1.plot(N, all_power_min, '-', label='Min')
ax1.plot(N, all_power_std, '-', label='Std')
ax1.plot(N, all_power_avg, '-', label='Avg')
ax1.legend()
ax1.set_ylabel("TX Power Index (0->0dB  - 7->-25dB)")

plt.title('TX Power', y=1.12)

for t in ["eps", "pdf", "svg", "png"]:
	filename = "./graph_%s/TX_Power.%s" % (file_name, t)
	plt.savefig(filename, bbox_inches='tight')

plt.close(fig)

# ALL ETX

fig, ax1 = plt.subplots()
ax1.plot(N, all_etx_max, '-', label='Max')
ax1.plot(N, all_etx_min, '-', label='Min')
ax1.plot(N, all_etx_std, '-', label='Std')
ax1.plot(N, all_etx_avg, '-', label='Avg')
ax1.legend()
ax1.set_ylabel("All Avg ETX")

plt.title('All ETX', y=1.12)

for t in ["eps", "pdf", "svg", "png"]:
	filename = "./graph_%s/All_ETX.%s" % (file_name, t)
	plt.savefig(filename, bbox_inches='tight')

plt.close(fig)

# BEST ETX

fig, ax1 = plt.subplots()
ax1.plot(N, all_good_etx_max, '.', label='Max')
ax1.plot(N, all_good_etx_min, '.', label='Min')
ax1.plot(N, all_good_etx_std, '.', label='Std')
ax1.plot(N, all_good_etx_avg, '.', label='Avg')
ax1.legend()
ax1.set_ylabel("Best Avg ETX")

plt.title('Best ETX', y=1.12)

for t in ["eps", "pdf", "svg", "png"]:
	filename = "./graph_%s/Best_ETX.%s" % (file_name, t)
	plt.savefig(filename, bbox_inches='tight')

plt.close(fig)


#x_ticks = range(len(power_txs))
#ax1.plot(x_ticks[:len(all_rssi_per_power)], all_rssi_per_power, '-', label='All')
#ax1.plot(x_ticks[:len(best_5_rssi_per_power)], best_5_rssi_per_power, '-', label='Best 5')
#ax1.plot(x_ticks[:len(best_10_rssi_per_power)], best_10_rssi_per_power, '-', label='Best 10')
#ax1.plot(x_ticks[:len(best_15_rssi_per_power)], best_15_rssi_per_power, '-', label='Best 15')
#ax1.set_ylabel("RSSI")
#ax1.legend()

#plt.xticks(x_ticks, power_txs)
#plt.xlim(x_ticks[0], x_ticks[-1])
#plt.xlabel("dBm")

#plt.xticks(x_ticks[0:len(all_neighborhood_per_power)], ["%.1f"%(x) for x in all_neighborhood_per_power])
#plt.xlim(x_ticks[0], x_ticks[-1])
##ymax = max(all_rssi_per_power) + 5
##ymin = max(all_rssi_per_power) - 10
##plt.ylim(ymin, ymax)
#plt.xlabel("Average Neighborhood Size")

#fig.set_size_inches(11, 5)
#fig.subplots_adjust(top=0.99)
#fig.subplots_adjust(hspace=0.5)

#plt.show()



