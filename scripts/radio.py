#!/usr/bin/python
# Combine RSSI logs from different TX powers
# into a single JSON file
#
# Author: Marcin K Szczodrak
# Updated: 5/3/2014

import sys
import os
import json

rssi_json = "rssi.json"
counter_json = "counter.json"
tx_problem_json = "tx_problems.json"
duty_cycle_json = "duty_cycle.json"
ctp_routing_json = "ctp_routing.json"

def rssi(channel, data_file, pwd, radio_conf):
	rssi_data = {}
	rssi_calibrate_params = ["avg_rssi", "std_rssi", "max_rssi", "min_rssi"]

	for txpower in radio_conf.radio_tx_powers_confs:
		print "Processing results for tx-power: %s\n" % (txpower)
		folder_name = "%s/rssi_ch%d_p%s" % (radio_conf.data_directory, channel, txpower)
		os.chdir(folder_name)
		os.system("make")

		with open(rssi_json) as jin:
			content = jin.read()
		jdata = json.loads(content)
		for mote_id in jdata.keys():
			for calparam in rssi_calibrate_params:
				if jdata[mote_id][calparam] != None:
					jdata[mote_id][calparam] = jdata[mote_id][calparam] * \
					radio_conf.radio_rssi_scale + radio_conf.radio_rssi_offset

			for neighbor in jdata[mote_id]['neighbors']:
				for calparam in rssi_calibrate_params:
					jdata[mote_id]['neighbors'][neighbor][calparam] = \
					jdata[mote_id]['neighbors'][neighbor][calparam] * \
					radio_conf.radio_rssi_scale + radio_conf.radio_rssi_offset
				

		rssi_data[txpower] = jdata

	os.chdir(pwd)

	# save as json
	with open("data_rssi_%s" % (data_file), 'wb') as fp:
		json.dump(rssi_data, fp, sort_keys=True, indent=4)


def counter(channel, data_file, pwd, radio_conf, duty_cycle, destination, delay):
	counter_data = {}
	tx_problem_data = {}
	duty_cycle_data = {}
	ctp_routing_data = {}

	for txpower in radio_conf.radio_tx_powers_confs:
		print "Processing results for tx-power: %s\n" % (txpower)
		folder_name = "%s/counter_ch%d_lpl%d_r%d_d%d_p%s" % (radio_conf.data_directory,
				channel, duty_cycle, destination, delay, txpower)
		os.chdir(folder_name)
		os.system("make")

		with open(counter_json) as jin:
			content = jin.read()
		counter_data[txpower] = json.loads(content)

		with open(ctp_routing_json) as jin:
			content = jin.read()
		ctp_routing_data[txpower] = json.loads(content)

		if duty_cycle:
			with open(duty_cycle_json) as jin:
				content = jin.read()
			duty_cycle_data[txpower] = json.loads(content)
		else:
			with open(tx_problem_json) as jin:
				content = jin.read()
			tx_problem_data[txpower] = json.loads(content)



	os.chdir(pwd)

	# save as json
	with open("data_counter_%s" % (data_file), 'wb') as fp:
		json.dump(counter_data, fp, sort_keys=True, indent=4)

	with open("data_ctp_routing_%s" % (data_file), 'wb') as fp:
		json.dump(ctp_routing_data, fp, sort_keys=True, indent=4)

	if duty_cycle:
		with open("data_duty_cycle_%s" % (data_file), 'wb') as fp:
			json.dump(duty_cycle_data, fp, sort_keys=True, indent=4)
	else:
		with open("data_tx_problem_%s" % (data_file), 'wb') as fp:
			json.dump(tx_problem_data, fp, sort_keys=True, indent=4)




