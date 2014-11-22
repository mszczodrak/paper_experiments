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

if len(sys.argv) != 6:
	print "usage %s <data_to_import> <radio_conf> <m> <n> <title>\n" % (sys.argv[0])
	exit()

data_module = sys.argv[1]
fig_title = sys.argv[5]
file_name = "_".join(fig_title.split())

m = int(float(sys.argv[3]))
n = int(float(sys.argv[4]))
y_height = 65

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

def autolabel(rects, ax):
	# attach some text labels
	for rect in rects:
		height = rect.get_height()
		ax.text(rect.get_x()+rect.get_width()/2., height + 1, '%d'%int(height),
				ha='center', va='bottom')

# data preprocessing

if len(snapshots) > 1:
	snapshot = snapshots[-2]
else:
	snapshot = snapshots[-1]

nodes = snapshot['nodes']

radio_levels = {}
all_neighbors = {}

sum_index = 0.0

for node_id in nodes.keys():
	# Collect radio levels

	if 'last_safe_tx_power' in nodes[node_id].keys():
		rtp = nodes[node_id]['last_safe_tx_power'][-1]
		if rtp == None:
			radio_index = 0
		else:
			rtp_str = "%02d" % (rtp)
			radio_index = int(conf.radio_power_index[rtp_str])
	else:
		radio_index = 0


	if radio_index not in radio_levels.keys():
		radio_levels[radio_index] = 0

	radio_levels[radio_index] = radio_levels[radio_index] + 1

	sum_index += radio_index

	# The number of good and all neighbors

	per_node_all_etx = []

	all_index = len(nodes[node_id]['neighborhood'].keys())


	if all_index not in all_neighbors.keys():
		all_neighbors[all_index] = 0

	all_neighbors[all_index] = all_neighbors[all_index] + 1


radio_levels_x = np.arange(len(conf.radio_tx_powers_sorted))
radio_levels_y = [] 

for k in range(len(conf.radio_tx_powers_sorted)):
	
	if k not in radio_levels.keys():
		radio_levels[k] = 0
	radio_levels_y.append(radio_levels[k])


print radio_levels

#print radio_levels_x
#print radio_levels

average_radio_index_level = sum_index / (len(nodes.keys()))

print 'Average Index: ',
print average_radio_index_level

the_x = max(all_neighbors.values()) + 1

x_data = np.arange(the_x)

all_neighbors_y = [0] * the_x

for k in sorted(all_neighbors.keys()):
	i = all_neighbors[k]
	all_neighbors_y[i] = k
	
width = 0.9

# data plotting

os.mkdir("graph_%s" % (file_name))

# TX POWER

fig, ax1 = plt.subplots()
ticks = np.arange(len(radio_levels))
n_ticks = []
for t in ticks:
	n_ticks.append(t + 0.45)
r = ax1.bar(radio_levels_x, radio_levels_y, width)
ax1.set_xticks(n_ticks)
ax1.set_xticklabels(conf.radio_tx_powers_sorted)
ax1.set_xlabel('dBm')
ax1.set_ylabel('Number of motes')
plt.xlim(0, n_ticks[-1] + width/2)

r2 = ax1.bar([average_radio_index_level-0.025],[y_height], 0.05, color='y')
ax1.set_ylim(0,y_height)
autolabel(r, ax1)

plt.title("Final Power Distribution (M:%d N:%d Simple)" % (m, n), y=1.12)

for t in ["eps", "pdf", "svg", "png"]:
        filename = "./graph_%s/Final_power.%s" % (file_name, t)
        plt.savefig(filename, bbox_inches='tight')

plt.close(fig)


width = 0.45

# Neighborhoods

fig, ax1 = plt.subplots()
ticks = x_data
n_ticks = []
for t in ticks:
	n_ticks.append(t + 0.45)

#print all_neighbors

r1 = ax1.bar(x_data, all_neighbors_y, width, color='b')
#ax1.set_xticks(n_ticks)
ax1.set_xlabel('Number of neighbors')
ax1.set_ylabel('Number of motes')

plt.title('Neighborhood Size Distribution', y=1.12)

for t in ["eps", "pdf", "svg", "png"]:
        filename = "./graph_%s/Final_neighborhood.%s" % (file_name, t)
        plt.savefig(filename, bbox_inches='tight')

plt.close(fig)



