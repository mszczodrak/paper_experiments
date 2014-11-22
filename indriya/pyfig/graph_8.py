#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import sys

from indriya_results import *


# Small packets

this_pkt_size = 104
this_init_delay = 15000
this_tx_delay = 60

all_backoffs = [10, 12, 14, 16, 18, 20, 22, 24, 26]

this_app_name = "push_data"

all_send = []
all_receive = []

#title = "Pushing Data As Soon As Possible"


for i in range(len(all_backoffs)):
	all_send.append(0)
	all_receive.append(0)

print "Using experiments: ",

for record in all_records:
	if not('app_name' in record):
		continue


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
fig.set_size_inches(10, 4)

l2 = ax.plot(ind, all_receive, 'k-', markersize=12)

ax.set_ylabel('Percentage of Packets Sent/Received (%)')
ax.set_xlabel('CSMA Backoff and Minimum Backoff Value (ms)')
#ax.set_title(title)
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

