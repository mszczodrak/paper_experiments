#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import sys

from indriya_results import *

this_pkt_size = 104
this_init_delay = 15000
this_backoff = 10
this_min_backoff = 10

all_tx_delays = [100, 50, 40, 30, 20, 15, 10, 5]

all_send = []
all_receive = []

#title = "Testing Throughput of CTP with 104 Bytes Payload"


for i in range(len(all_tx_delays)):
	all_send.append(0)
	all_receive.append(0)


print "Using experiments: ",

for record in all_records:
	if record['pkt_size'] != this_pkt_size:
		continue


	if record['init_delay'] != this_init_delay:
		continue

	if record['backoff'] != this_backoff:
		continue

	if record['min_backoff'] != this_min_backoff:
		continue

	this_tx_delay = record['tx_delay']

	if all_tx_delays.count(this_tx_delay) == 0:
		continue

	print record['name'],
	print " ",

	this_index = all_tx_delays.index(this_tx_delay)

	all_send[this_index] = (100.0 * record['send']) / (record['total'] * 1.0)
	all_receive[this_index] = (100.0 * record['receive']) / (record['total'] * 1.0)

print

N = len(all_tx_delays)

ind = np.arange(N)  # the x locations for the groups

fig = plt.figure()
ax = fig.add_subplot(111)
fig.set_size_inches(10, 4)

l1 = ax.plot(ind, all_send, 'k-', markersize=12)
l2 = ax.plot(ind, all_receive, 'k*', markersize=12)

ax.set_ylabel('Percentage of Packets Sent/Received (%)')
ax.set_xlabel('Transmission Delay (ms)')
#ax.set_title(title)
ax.set_xticks(ind)
ax.set_xticklabels( all_tx_delays )

ax.legend((l1, l2), ('Sent', 'Received'))

ymin, ymax = plt.ylim()
ylim_scale = (ymax - ymin) / 20
plt.ylim(ymin - ylim_scale, ymax + ylim_scale)


#plt.show()

for t in ["eps", "pdf", "svg"]:
        #filename = "../fig/%s.%s"%(sys.argv[0][:-3], t)
        filename = "./%s.%s"%(sys.argv[0][:-3], t)
        plt.savefig(filename)

