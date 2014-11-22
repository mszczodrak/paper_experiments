#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import sys

from multi_channel import *

# Small packets

this_pkt_size = 104
this_init_delay = 15000
this_backoff = 10
this_min_backoff = 10

all_channels = [26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11]

all_send = []
all_receive = []

#title = "Testing Throughput of CTP with 4 Bytes Application Payload"


for i in range(len(all_channels)):
	all_send.append(0)
	all_receive.append(0)

print "Using experiments: ",

for record in all_records:
	if record['pkt_size'] != this_pkt_size:
		continue

	if record['init_delay'] != this_init_delay:
		continue

	this_channel = record['channel']

	if all_channels.count(this_channel) == 0:
		continue

        print record['name'],
        print " ",

	this_index = all_channels.index(this_channel)

	all_send[this_index] = (100.0 * record['send']) / (record['total'] * 1.0)
	all_receive[this_index] = (100.0 * record['receive']) / (record['total'] * 1.0)

print

N = len(all_channels)

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
ax.set_xticklabels( all_channels )

ax.legend((l1, l2), ('Sent', 'Received'))

ymin, ymax = plt.ylim()
ylim_scale = (ymax - ymin) / 20
plt.ylim(ymin - ylim_scale, ymax + ylim_scale)


#plt.show()

for t in ["eps", "pdf", "svg"]:
        #filename = "../fig/%s.%s"%(sys.argv[0][:-3], t)
        filename = "./%s.%s"%(sys.argv[0][:-3], t)
        plt.savefig(filename)

