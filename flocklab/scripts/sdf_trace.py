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

if len(sys.argv) != 4:
	print("\nusage: %s <gpiotracing.json> <data.json> <testbed_conf>\n\n");
	sys.exit(1)

sdf_trace_json = sys.argv[1]

testbed_conf_module = sys.argv[3].split("/")[-1].split(".")[0]
path_to_testbed_conf_module = "/".join(sys.argv[3].split("/")[:-1])
sys.path.append(path_to_testbed_conf_module)

try:
	testbed_conf = __import__(testbed_conf_module)
except:
	print "failed to import %s\n" % (testbed_conf_module)
	exit()


with open(sdf_trace_json) as jin:
	content = jin.read()
sdf = json.loads(content)

stop_delays = []

def add_period():
	stop_delays.append({})
	stop_delays[-1]["data"] = []
	stop_delays[-1]["motes"] = []

add_period()

nodes = {}

for trace in sdf:
	timestamp = trace[0]
	mote_id = trace[1]
	status = trace[2]

	if mote_id not in nodes.keys():
		nodes[mote_id] = {}

	if mote_id > testbed_conf.max_node_id:
		continue

	if status == 1:
		if len(stop_delays[-1]["data"]) > 0 and \
			timestamp - stop_delays[-1]["data"][-1] > 10:
			add_period()

		stop_delays[-1]["data"].append(timestamp)
		stop_delays[-1]["motes"].append(mote_id)

results = {}
results["delays"] = []
results["percentage_of_reconfs"] = []
results["number_of_reconfs"] = []
results["number_of_nodes"] = len(nodes.keys())

for i in range(len(stop_delays)):
	#stop_delays[i]["data"] = sorted(stop_delays[i]["data"])
	#stop_delays[i]["data"] = stop_delays[i]["data"][5:-5]
	first = min(stop_delays[i]["data"])
	last = max(stop_delays[i]["data"])
	num = len(stop_delays[i]["data"])
	results["number_of_reconfs"].append(num)	
	results["percentage_of_reconfs"].append(num * 100.0 / results["number_of_nodes"])
	stop_delays[i]["first"] = first
	stop_delays[i]["last"] = last
	stop_delays[i]["delay"] = last - first
	print "%d (%d)  %.3f - %.3f = %.3f" % (i, num, last, first, stop_delays[i]["delay"]) 
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

