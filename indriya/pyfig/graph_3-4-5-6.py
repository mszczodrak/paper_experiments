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

all_tx_delays = [100, 50, 40, 30]

line_marker = ['k-', 'k--', 'k-.', 'k:']
point_marker = ['k*', 'ko', 'kx', 'k.']


#title = "Testing Throughput of CTP with different Backoff parameters"

N = len(all_backoffs)
ind = np.arange(N)  # the x locations for the groups

fig = plt.figure()
ax = fig.add_subplot(111)
fig.set_size_inches(10, 5)

legends = []
legends_names = []

for in_ptr in range(len(all_tx_delays)):

	this_tx_delay = all_tx_delays[in_ptr]

	all_send = []
	all_receive = []

	for i in range(len(all_backoffs)):
		all_send.append(0)
		all_receive.append(0)

	print this_tx_delay
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

	l1 = ax.plot(ind, all_send, line_marker[in_ptr], markersize=12)
	l2 = ax.plot(ind, all_receive, point_marker[in_ptr], markersize=12)

	legends.append(l1)
	legends_names.append('Send at %d'%(this_tx_delay))

	legends.append(l2)
	legends_names.append('Receive %d'%(this_tx_delay))

ax.set_ylabel('Percentage of Packets Sent/Received (%)')
ax.set_xlabel('CSMA Backoff and Minimum Backoff Value (ms)')
#ax.set_title(title)
ax.set_xticks(ind)
ax.set_xticklabels( all_backoffs )
ax.legend(legends, legends_names, loc=3, ncol=4, mode="expand")

ymin, ymax = plt.ylim()
ylim_scale = (ymax - ymin) / 20
plt.ylim(ymin - 10, ymax + ylim_scale)

#plt.show()

for t in ["eps", "pdf", "svg"]:
        #filename = "../fig/%s.%s"%(sys.argv[0][:-3], t)
        filename = "./%s.%s"%(sys.argv[0][:-3], t)
        plt.savefig(filename)

