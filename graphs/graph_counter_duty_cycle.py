#!/usr/bin/python
# Create graph for rssi vs delivery ratio vs acks
# Author: Marcin K Szczodrak
# Updated: 5/01/2014

import sys
import os
import numpy as np
import json
import operator
from pylab import *
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.mlab import bivariate_normal

if len(sys.argv) != 6:
	print "usage %s <counter_data_to_import> <duty_cycle_data_to_import> <radio_conf> <title> <shorter>\n" % (sys.argv[0])
	exit()

counter_data_module = sys.argv[1]
duty_cycle_data_module = sys.argv[2]

conf_module = sys.argv[3].split(".")[0]
fig_title = sys.argv[4]
file_name = "_".join(fig_title.split())
shorter = int(sys.argv[5])

try:
	conf = __import__(conf_module)
except:
	print "failed to import %s\n" % (conf_module)
	exit()


with open(counter_data_module) as jin:
	content = jin.read()
counter_data = json.loads(content)

with open(duty_cycle_data_module) as jin:
	content = jin.read()
duty_cycle_data = json.loads(content)


# data preprocessing

# Counter part
network_all_sent = []
network_all_received = []
network_all_delivered = []
network_all_lost_motes = []
network_all_delivered_std = []
network_all_delivered_mean = []
network_all_delivered_min = []

power_txs = []

for power_tx in conf.radio_tx_powers_confs:
	power_txs.append(conf.radio_power_levels[power_tx])

	mote_ids = []
	mote_send = []
	mote_receive = []
	mote_delivered = []
	mote_lost = 0

	for mote_id in counter_data[power_tx].keys():
		mote_ids.append(mote_id)
		mote_send.append(counter_data[power_tx][mote_id]["total_sent_data"])
		mote_receive.append(counter_data[power_tx][mote_id]["total_delivered_data"])
		mote_delivered.append(100.0 * counter_data[power_tx][mote_id]["total_delivered_data"] / \
						counter_data[power_tx][mote_id]["total_sent_data"]) 
		if counter_data[power_tx][mote_id]["total_delivered_data"] == 0:
			mote_lost += 1

	sent = sum(mote_send)
	received = sum(mote_receive)

	network_all_sent.append(sent)
	network_all_received.append(received)
	network_all_delivered.append(100.0 * received / sent)
	network_all_lost_motes.append(mote_lost)
	
	mote_delivered_array = np.array( mote_delivered )
	network_all_delivered_std.append( mote_delivered_array.std() )
	network_all_delivered_mean.append( mote_delivered_array.mean() )
	network_all_delivered_min.append( mote_delivered_array.min() )


print "Number of lost motes"
print network_all_lost_motes

print "Delivered Means"
print network_all_delivered_mean

print "Delivered Std"
print network_all_delivered_std

print "Delivered Min"
print network_all_delivered_min

print


# Duty-Cycle part
network_all_mean_off = []
network_all_mean_on = []
network_all_sum_off = []
network_all_sum_on = []
network_all_std_on = []
network_all_std_off = []
network_all_duty_cycle = []

for power_tx in conf.radio_tx_powers_confs:
	mote_ids = []
	mote_mean_off_time_ms = []
	mote_mean_on_time_ms = []
	mote_sum_off_time_ms = []
	mote_sum_on_time_ms = []

	for mote_id in duty_cycle_data[power_tx].keys():
		mote_ids.append(mote_id)
		mote_mean_off_time_ms.append(duty_cycle_data[power_tx][mote_id]["mean_off_time_ms"])
		mote_mean_on_time_ms.append(duty_cycle_data[power_tx][mote_id]["mean_on_time_ms"])
		mote_sum_off_time_ms.append(duty_cycle_data[power_tx][mote_id]["sum_off_time_ms"])
		mote_sum_on_time_ms.append(duty_cycle_data[power_tx][mote_id]["sum_on_time_ms"])

	mote_mean_off_time_ms_array = np.array(mote_mean_off_time_ms)
	mote_mean_on_time_ms_array = np.array(mote_mean_on_time_ms)

	mean_off_time_ms = mote_mean_off_time_ms_array.mean()
	mean_on_time_ms = mote_mean_on_time_ms_array.mean()
	sum_off_time_ms = mote_mean_off_time_ms_array.sum()
	sum_on_time_ms = mote_mean_on_time_ms_array.sum()

	network_all_mean_off.append( mote_mean_off_time_ms_array.mean() )
	network_all_mean_on.append( mote_mean_on_time_ms_array.mean() )
	network_all_sum_off.append( mote_mean_off_time_ms_array.sum() )
	network_all_sum_on.append( mote_mean_on_time_ms_array.sum() )
	network_all_std_off.append( mote_mean_off_time_ms_array.std() )
	network_all_std_on.append( mote_mean_on_time_ms_array.std() )

	network_all_duty_cycle.append(100.0 * sum_on_time_ms / (sum_on_time_ms + sum_off_time_ms))


print "Network All Mean On"
print network_all_mean_on

print "Network All Std On"
print network_all_std_on

print "Network Duty Cycle"
print network_all_duty_cycle

print

# data plotting

os.mkdir("graph_%s" % (file_name))

for tp in ["full", "short"]:

	# Counter part
	data_delivered = []

	if tp == "full":
		x_ticks = range(len(power_txs))
		data_delivered = network_all_delivered
	else:
		x_ticks = range(len(power_txs) - shorter)
		data_delivered = network_all_delivered[:-shorter]

	fig, ax1 = plt.subplots()
	ax1.plot(x_ticks[:len(data_delivered)], data_delivered, '-')
	ax1.set_ylabel("Delivery Ratio")
	#ax1.legend()

	plt.xticks(x_ticks, power_txs)
	plt.xlim(x_ticks[0], x_ticks[-1])
	plt.xlabel("dBm")

	# mark the best result
	max_counter_index, max_counter_value = max(enumerate(data_delivered), key=operator.itemgetter(1))
	ax1.plot(x_ticks[max_counter_index], max_counter_value, marker=(5,1), markersize=14, color='k')

	# mark the worst result
	min_counter_index, min_counter_value = min(enumerate(data_delivered), key=operator.itemgetter(1))
	ax1.plot(x_ticks[min_counter_index], min_counter_value, marker=(5,1), markersize=14, color='k')

	#plt.ylim(max_counter_value - 15, max_counter_value + 5)
	#plt.ylim(min(network_all_delivered) -2, max(network_all_delivered) + 2)


	# Duty cycle part

	data_duty_cycle = []

	if tp == "full":
		x_ticks = range(len(power_txs))
		data_duty_cycle = network_all_duty_cycle
	else:
		x_ticks = range(len(power_txs) - shorter)
		data_duty_cycle = network_all_duty_cycle[:-shorter]

		
	ax2 = ax1.twinx()
	ax2.plot(x_ticks[:len(data_duty_cycle)], data_duty_cycle, 'k-')
	ax2.set_ylabel("Duty Cycle (%)")


        # mark the best result
        max_duty_cycle_index, max_duty_cycle_value = max(enumerate(data_duty_cycle), key=operator.itemgetter(1))
        ax2.plot(x_ticks[max_duty_cycle_index], max_duty_cycle_value, marker=(5,1), markersize=14, color='k')

        # mark the worst result
        min_duty_cycle_index, min_duty_cycle_value = min(enumerate(data_duty_cycle), key=operator.itemgetter(1))
        ax2.plot(x_ticks[min_duty_cycle_index], min_duty_cycle_value, marker=(5,1), markersize=14, color='k')

        #plt.ylim(max_duty_cycle_value - 15, max_duty_cycle_value + 5)
        #plt.ylim(min(network_all_delivered) -2, max(network_all_delivered) + 2)


	fig.set_size_inches(11, 5)
	fig.subplots_adjust(top=0.99)
	fig.subplots_adjust(hspace=0.5)

	plt.title(fig_title, y=1.12)

	for t in ["eps", "pdf", "svg", "png"]:
		filename = "./graph_%s/%s_%s.%s"%(file_name, file_name, tp, t)
		plt.savefig(filename, bbox_inches='tight')


