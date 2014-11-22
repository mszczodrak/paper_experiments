#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import sys

from indriya_results import *

# Small packets


all_tx_delays = [20, 30, 40, 50, 100]

sec_send = []
pic_send = []

pkts = 768.0
tot_time = 4.0 * 60 * 1000.0

for delay in all_tx_delays:
	sec_send.append( pkts * delay / 1000.0)
	pic_send.append((tot_time / delay) / pkts)

#title = "Evaluating Possibiltiy of Image Transmission"


N = len(all_tx_delays)
ind = np.arange(N)  # the x locations for the groups

fig = plt.figure()
fig.set_size_inches(10, 4)
#fig.suptitle(title)


print sec_send
print pic_send

ax = fig.add_subplot(121)
l1 = ax.plot(ind, sec_send, 'k-', markersize=12)
ax.set_ylabel('One Picture Transmission (sec)')
ax.set_xlabel('Transmission Delay (ms)')
ax.set_xticks(ind)
ax.set_xticklabels( all_tx_delays )

#ymin, ymax = plt.ylim()
#ylim_scale = (ymax - ymin) / 20
#plt.ylim(ymin - ylim_scale, ymax + ylim_scale)

ax1 = fig.add_subplot(122)
l1 = ax1.plot(ind, pic_send, 'k-', markersize=12)
ax1.set_ylabel('Number of Pictures within 4 mins')
ax1.set_xlabel('Transmission Delay (ms)')
ax1.set_xticks(ind)
ax1.set_xticklabels( all_tx_delays )



#plt.show()

for t in ["eps", "pdf", "svg"]:
        #filename = "../fig/%s.%s"%(sys.argv[0][:-3], t)
        filename = "./%s.%s"%(sys.argv[0][:-3], t)
        plt.savefig(filename)

