#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import sys

from indriya_results import *


# Small packets

this_pkt_size = 104
this_init_delay = 15000
this_tx_delay = 100

all_backoffs = [10, 8, 6, 4, 2]


all_send = []
all_receive = []

title = "Percentage of packets with 104B of application payload successfully transmitted every 100 ms"


for i in range(len(all_backoffs)):
	all_send.append(0)
	all_receive.append(0)

print "Using experiments: ",

for record in all_records:
	if record['pkt_size'] != this_pkt_size:
		continue


	if record['init_delay'] != this_init_delay:
		continue

	if record['tx_delay'] != this_tx_delay:
		continue

	this_backoff = record['backoff']

	if all_backoffs.count(this_backoff) == 0:
		continue

        print record['name'],
        print " ",

	this_index = all_backoffs.index(this_backoff)

	all_send[this_index] = (100.0 * record['send']) / (record['total'] * 1.0)
	all_receive[this_index] = (100.0 * record['receive']) / (record['total'] * 1.0)
print

N = len(all_backoffs)

ind = np.arange(N)  # the x locations for the groups

fig = plt.figure()
ax = fig.add_subplot(111)

ax.plot(ind, all_send)
ax.plot(ind, all_receive)

ax.set_ylabel('Percentage of Packets Send/Received (%)')
ax.set_xlabel('CSMA Backoff and Minimum Backoff Value (ms)')
ax.set_title(title)
ax.set_xticks(ind)
ax.set_xticklabels( all_backoffs )


ymin, ymax = plt.ylim()
ylim_scale = (ymax - ymin) / 20
plt.ylim(ymin - ylim_scale, ymax + ylim_scale)

#plt.show()

for t in ["eps", "pdf", "svg"]:
        #filename = "../fig/%s.%s"%(sys.argv[0][:-3], t)
        filename = "./%s.%s"%(sys.argv[0][:-3], t)
        plt.savefig(filename)

