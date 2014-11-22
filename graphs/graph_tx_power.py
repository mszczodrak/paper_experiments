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

all_power_max = []
all_power_min = []
all_power_std = []
all_power_avg = []

N = range(len(snapshots))

for snapshot_id in N:
	snapshot = snapshots[snapshot_id]
	nodes = snapshot['nodes']

	radio_tx_powers = []

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

	radio_tx_powers_array = np.array( radio_tx_powers )
	all_power_max.append( radio_tx_powers_array.max() )
	all_power_min.append( radio_tx_powers_array.min() )
	all_power_std.append( radio_tx_powers_array.std() )
	all_power_avg.append( radio_tx_powers_array.mean() )

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


