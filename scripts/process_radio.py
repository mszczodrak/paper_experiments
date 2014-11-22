#!/usr/bin/python

import os.path
from subprocess import call

import numpy as np
import matplotlib.pyplot as plt

from radio_stats import *
from get_processed import *

lines = ['or-', 'sb--', 'dg-.', 'vk:', 'r--']

exps = {
		"nothing" 	: {
					"names"		:	["exp_2001", "exp_2002", "exp_2003", "exp_2004", "exp_2005", "exp_2006"],
					"sleep"		:	[100, 200, 300, 400, 500, 600],
					"results"	:	[],
					"means"		:	[],
					"stds"		:	[],
					},
		"ctp_on" 	: {
					"names"		:	["exp_2011", "exp_2012", "exp_2013", "exp_2014", "exp_2015", "exp_2016"],
					"sleep"		:	[100, 200, 300, 400, 500, 600],
					"results"	:	[],
					"means"		:	[],
					"stds"		:	[],
					},
		"ctp_60" 	: {
					"names"		:	["exp_2021", "exp_2022", "exp_2023", "exp_2024", "exp_2025", "exp_2026"],
					"sleep"		:	[100, 200, 300, 400, 500, 600],
					"results"	:	[],
					"means"		:	[],
					"stds"		:	[],
					},
		"ctp_300" 	: {
					"names"		:	["exp_2031", "exp_2032", "exp_2033", "exp_2034", "exp_2035", "exp_2036"],
					"sleep"		:	[100, 200, 300, 400, 500, 600],
					"results"	:	[],
					"means"		:	[],
					"stds"		:	[],
					},
		"ctp_600" 	: {
					"names"		:	["exp_2041", "exp_2042", "exp_2043", "exp_2044", "exp_2045", "exp_2046"],
					"sleep"		:	[100, 200, 300, 400, 500, 600],
					"results"	:	[],
					"means"		:	[],
					"stds"		:	[],
					},
	}


# unpack data and run radio_stats

for key in exps.keys():
	print "Processing Experiments %s\n"%(key)

	for exp_index in range(len(exps[key]["names"])):
		exp_name = exps[key]["names"][exp_index]
		exp_path = "../%s"%(exp_name)
		if not os.path.exists(exp_path):
			continue

		if os.path.isfile("%s/processed.txt"%(exp_path)):
			continue

		if not os.path.isfile("%s/result.txt"%(exp_path)):
			os.chdir(exp_path)
			call(["make"])
			call(["cp", "../scripts/radio_stats.py", "./"])
			os.chdir("../scripts")

		if os.path.isfile("%s/result.txt"%(exp_path)):
			radio_stats("%s/result.txt"%(exp_path), "%s/processed.txt"%(exp_path))


for key in exps.keys():
        print "%s\n"%(key)

        for exp_index in range(len(exps[key]["names"])):
                exp_name = exps[key]["names"][exp_index]
                exp_path = "../%s"%(exp_name)
		exp_processed = "%s/processed.txt"%(exp_path)
                if not os.path.exists(exp_processed):
			continue

		[m,s] = get_processed(exp_processed)


		while(len(exps[key]["results"]) <= exp_index):
			exps[key]["results"].append([])
			exps[key]["means"].append(0)
			exps[key]["stds"].append(0)

		exps[key]["results"][exp_index] = [m,s]
		exps[key]["means"][exp_index] = m
		exps[key]["stds"][exp_index] = s


# get_figure

fig = plt.figure()
fig.set_size_inches(12, 7)

x_labels = exps["nothing"]["sleep"]

N = len(x_labels)
ind = np.arange(N)  # the x locations for the groups
all_keys = exps.keys()

# FIRST GRAPH
ax1 = plt.subplot(211)

#ax1.set_title("Pkt Size %d Bytes"%(this_pkt_size))
ax1.set_ylabel('Radio turned on time (%)')
ax1.set_xticks(ind)
ax1.set_xticklabels( x_labels )
ax1.set_xlabel('Sleep Interval (ms)')
ax1.grid(True)

for i in range(len(all_keys)):
	key = all_keys[i]
	print "Plotting: %s"%(key)
	print ind
	print exps[key]["means"]
	ax1.plot(ind, exps[key]["means"], lines[i], markersize=8, label=key)

plt.legend(loc=2, ncol=2)


# SECOND GRAPH
ax2 = plt.subplot(212)

#ax1.set_title("Pkt Size %d Bytes"%(this_pkt_size))
ax2.set_ylabel('Radio turned on time (%)')
ax2.set_xticks(ind)
ax2.set_xticklabels( x_labels )
ax2.set_xlabel('Sleep Interval (ms)')
ax2.grid(True)

for i in range(len(all_keys)):
        key = all_keys[i]
        print "Plotting: %s"%(key)
        print ind
        print exps[key]["means"]
        ax2.plot(ind, exps[key]["means"], lines[i], markersize=8, label=key)

ymin, ymax = plt.ylim()
plt.ylim(ymin, 15)
plt.legend(loc=1, ncol=2)




#plt.show()
for t in ["eps", "pdf", "svg"]:
        #filename = "../fig/%s.%s"%(sys.argv[0][:-3], t)
        filename = "./%s.%s"%(sys.argv[0][:-3], t)
        plt.savefig(filename)

