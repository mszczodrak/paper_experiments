#!/usr/bin/python
# Processing dbgs messages from Counter test application
# Author: Marcin K Szczodrak
# Updated; 4/24/2014

import sys
import os
sys.path.append("%s/support/sdk/python" % (os.environ["FENNEC_FOX_LIB"]))
from dbgs_h import *
import numpy as np
import json

# usage script logs

if len(sys.argv) != 4:
	print "usage %s <result.txt> <data.json> <testbed_conf>"
	sys.exit(1)

f = open(sys.argv[1], "r")


testbed_conf_module = sys.argv[3].split("/")[-1].split(".")[0]
path_to_testbed_conf_module = "/".join(sys.argv[3].split("/")[:-1])
sys.path.append(path_to_testbed_conf_module)

nodes = {}

try:
	testbed_conf = __import__(testbed_conf_module)
except:
	print "failed to import %s\n" % (testbed_conf_module)
	exit()

stop_delays = []

def add_period():
	stop_delays.append({})
	stop_delays[-1]["data"] = []
	stop_delays[-1]["motes"] = []
		
add_period()

for line in f.readlines():
	l = line.split()

	if len(l) != 9:
		continue

	if not l[0].isdigit():
		continue

	timestamp = int(l[0]) + (float(l[1]) / 1000.0)
	mote_id = int(l[2])
	version = int(l[3])
	did = int(l[4])
	dbg = int(l[5])
	d0 = int(l[6])
	d1 = int(l[7])
	d2 = int(l[8])

	if mote_id > testbed_conf.max_node_id:
		print line
		continue

	if mote_id not in nodes.keys():
		nodes[mote_id] = {}

	if dbg == DBGS_SIGNAL_FINISH_PERIOD:
		if len(stop_delays[-1]["data"]) > 0  and \
			timestamp - stop_delays[-1]["data"][-1] > 3:
			add_period()

		stop_delays[-1]["data"].append(timestamp)	
		stop_delays[-1]["motes"].append(mote_id)

number_of_motes = len(nodes.keys())
results = {}
results["delays"] = []
results["percentage_of_reconfs"] = []
results["number_of_reconfs"] = []
results["number_of_nodes"] = len(nodes.keys())

for i in range(len(stop_delays)):
	first = min(stop_delays[i]["data"])
	last = max(stop_delays[i]["data"])
	num = len(stop_delays[i]["data"])
	results["number_of_reconfs"].append(num)
	results["percentage_of_reconfs"].append(num * 100.0 / results["number_of_nodes"])
	stop_delays[i]["first"] = first
	stop_delays[i]["last"] = last
	stop_delays[i]["delay"] = last - first
	if stop_delays[i]["delay"] < 1:
		print "%d (%d, %02.2f)  %.3f - %.3f = %.3f" % (i, num, num * 100.0 / number_of_motes,  last, first, stop_delays[i]["delay"])
		results["delays"].append(stop_delays[i]["delay"])


results["min_delay"] = min(results["delays"])
results["max_delay"] = max(results["delays"])
results["avg_delay"] = sum(results["delays"]) * 1.0 / len(results["delays"])
results["median_delay"] = sorted(results["delays"])[len(results["delays"]) / 2]
results["avg_num_reconfs"] = sum(results["percentage_of_reconfs"]) * 1.0 / len(results["percentage_of_reconfs"])
results["stop_delays"] = stop_delays

# save as json
with open(sys.argv[2], 'wb') as fp:
	json.dump(results, fp, sort_keys=True, indent=4)

print "\nEstimate Dissemination End Time Final Results "
print "Min     %.4f" % (results["min_delay"])
print "Average %.4f" % (results["avg_delay"])
print "Median  %.4f" % (results["median_delay"])
print "Max     %.4f" % (results["max_delay"])
print "Reconf  %.4f" % (results["avg_num_reconfs"])
print

del results["delays"]
del results["stop_delays"]
del results["number_of_reconfs"]
del results["percentage_of_reconfs"]

# save as json
with open("summary_%s" % (sys.argv[2]), 'wb') as fp:
	json.dump(results, fp, sort_keys=True, indent=4)


