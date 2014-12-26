#!/usr/bin/python
# Marcin K Szczodrak
# Updated on 4/24/2014

import sys
import csv
import os
sys.path.append("%s/support/sdk/python" % (os.environ["FENNEC_FOX_LIB"]))
from dbgs_h import *
import numpy as np
import json

flocklab_log_length = 5

if len(sys.argv) < 5:
	print("\nusage: %s <gpiotracing.csv> <testbed_conf> [<LED#> <output_name> ] ... \n\n");
	sys.exit(1)

f = open(sys.argv[1], "r")
gpio_duty_cycle = sys.argv[2]

testbed_conf_module = sys.argv[2].split("/")[-1].split(".")[0]
path_to_testbed_conf_module = "/".join(sys.argv[2].split("/")[:-1])
sys.path.append(path_to_testbed_conf_module)

try:
	testbed_conf = __import__(testbed_conf_module)
except:
	print "failed to import %s\n" % (testbed_conf_module)
	exit()


LEDS = {}
nodes = {}

for i in xrange(3, len(sys.argv), 2):
	LEDS[sys.argv[i]] = {}
	LEDS[sys.argv[i]]['id'] = sys.argv[i]
	LEDS[sys.argv[i]]['name'] = sys.argv[i+1]
	LEDS[sys.argv[i]]['data'] = []


all_lines = [line.split(",") for line in f.readlines()]

for l in all_lines:
	if len(l) != flocklab_log_length:
		continue

	if not l[0][0].isdigit():
		continue

	try:
		timestamp = float(l[0])
		mote_id = int(float(l[1]))
		gpio = l[3]
		gpio_state = int(float(l[4]))

	except:
		continue

	if mote_id > testbed_conf.max_node_id:
		print line
		continue


	if not(mote_id in nodes.keys()):
		new_node = {}
		for led_id in LEDS.keys():
			new_node[led_id] = {}
			new_node[led_id]['id'] = led_id
			new_node[led_id]['name'] = LEDS[led_id]['name']
			new_node[led_id]['data'] = []

		nodes[mote_id] = new_node
	LEDS[gpio]['data'].append((timestamp, mote_id, gpio_state))

	nodes[mote_id][gpio]['data'].append((timestamp, gpio_state))


for led_id in LEDS.keys():
	LEDS[led_id]['data'].sort(key=lambda x: x[0] )
	
	# save as json
	with open("%s_%s_%s.json" % (sys.argv[1].split(".")[0], LEDS[led_id]['id'], LEDS[led_id]['name']), 'wb') as fp:
		json.dump(LEDS[led_id]['data'], fp, sort_keys=True, indent=4)

	# save as json
	with open("%s_%s_%s.txt" % (sys.argv[1].split(".")[0], LEDS[led_id]['id'], LEDS[led_id]['name']), 'wb') as fp:
		for d in LEDS[led_id]['data']:
			t = "\t".join(str(e) for e in d) + "\n"
			fp.write(t)

for mote_id in nodes.keys():
	for led_id in LEDS.keys():
		nodes[mote_id][led_id]['data'].sort(key=lambda x: x[0])

# save as json
with open("%s_nodes_%s.json" % (sys.argv[1].split(".")[0], "_".join(LEDS.keys())), 'wb') as fp:
	json.dump(nodes, fp, sort_keys=True, indent=4)


