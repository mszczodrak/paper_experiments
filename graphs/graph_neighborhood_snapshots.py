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

if len(sys.argv) != 4:
	print "usage %s <data_to_import> <radio_conf> <title>\n" % (sys.argv[0])
	exit()

data_module = sys.argv[1]
fig_title = sys.argv[3]
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

all_max = []
all_min = []
all_std = []
all_avg = []

N = range(len(snapshots))

for snapshot_id in N:
	snapshot = snapshots[snapshot_id]
	all_max.append(snapshot['max_number_of_neighbors'])
	all_min.append(snapshot['min_number_of_neighbors'])
	all_std.append(snapshot['std_number_of_neighbors'])
	all_avg.append(snapshot['avg_number_of_neighbors'])

# data plotting

fig = plt.figure()
ax = fig.add_subplot(111)

ax.plot(N, all_max, label='Max')
ax.plot(N, all_min, label='Min')
ax.plot(N, all_std, label='Std')
ax.plot(N, all_avg, label='Avg')

ax.legend()

ax.set_ylabel('Number of Neighbors')

#fig, ax1 = plt.subplots()
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

#ax2 = ax1.twiny()
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

plt.title(fig_title, y=1.12)

os.mkdir("graph_%s" % (file_name))

for t in ["eps", "pdf", "svg", "png"]:
	filename = "./graph_%s/%s.%s" % (file_name, file_name, t)
	plt.savefig(filename, bbox_inches='tight')


