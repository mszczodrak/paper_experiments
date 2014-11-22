#!/usr/bin/python
# Create graph for rssi vs delivery ratio vs acks
# Author: Marcin K Szczodrak
# Updated: 5/01/2014

import sys
import os
import numpy as np
import operator
from pylab import *
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.mlab import bivariate_normal

if len(sys.argv) != 2:
	print "usage %s <path_to_data_to_import>\n" % (sys.argv[0])
	exit()

try:
	parts = sys.argv[1].split("/")
	new_sys_path = "/".join(parts[:-1])
	new_module = parts[-1].split(".")[0]
except:
	print "failed to parse %d\n" % (sys.argv[1])
	exit()

try:
	sys.path.append(new_sys_path)
except:
	print "failed to add system path %d\n" % ( new_sys_path )
	exit()

try:
	data = __import__(new_module)
except:
	print "failed to import %s\n" % (new_module)
	exit()

dbms = []
counter = []
percentage_on = []
on_mean = []
on_std = []
off_mean = []
off_std = []
rssi_hood = []

x_ticks = range(len(data.results))
x_min = x_ticks[0] - 0.5
x_max = x_ticks[-1] + 0.5
y_min = 29
y_max = 101

for d in data.results:
	dbms.append(d['dbm'])
	counter.append(d['counter'])
	percentage_on.append(d['percentage_on'])
	on_mean.append(d['on_mean'])
	on_std.append(d['on_std'])
	off_mean.append(d['off_mean'])
	off_std.append(d['off_std'])
	rssi_hood.append(d['rssi_hood'])

max_counter_index, max_counter_value = max(enumerate(counter), key=operator.itemgetter(1))
min_duty_index, min_duty_value = min(enumerate(percentage_on), key=operator.itemgetter(1))

fig, ax1 = plt.subplots()

ax1.plot(x_ticks, counter, 'k--', label='Delivery Ratio')
ax1.set_ylabel("Delivery Radio (%)")
ax1.set_ylim(y_min, y_max)
ax1.set_xlim(x_min, x_max)

# mark best result
ax1.plot(x_ticks[max_counter_index], max_counter_value, marker=(5,1), markersize=14, color='k')

plt.xticks(x_ticks, dbms)
plt.xlim(x_min, x_max)
plt.xlabel("dBm")

X = arange(x_min, x_max + 1, 1)
Y = arange(y_min, y_max + 1, 1)
X1,Y1 = meshgrid(X, Y)
Z1 = array([rssi_hood] * (y_max - y_min))
cimg = plt.pcolor(X1, Y1, Z1, cmap='bone_r', alpha=0.3)

ax2 = ax1.twinx()
ax2.plot(x_ticks, percentage_on, 'k:', label='Duty-Cycle (%)')
ax2.set_ylabel("Duty-Cycle (%)");

# mark best result
ax2.plot(x_ticks[min_duty_index], min_duty_value, marker=(5,1), markersize=14, color='k')

ax3 = ax1.twiny()
plt.xticks(x_ticks, ["%.1f"%(x) for x in rssi_hood])
plt.xlim(x_min, x_max)
plt.xlabel("Average Neighborhood Size")

h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
	
ax3.legend(h1+h2, l1+l2, loc=6)

fig.set_size_inches(11, 5)
fig.subplots_adjust(top=0.99)
fig.subplots_adjust(hspace=0.5)

plt.title(data.title, y=1.12)

for t in ["eps", "pdf", "svg", "png"]:
	filename = "./%s.%s"%(sys.argv[0][:-3], t)
	plt.savefig(filename, bbox_inches='tight')


