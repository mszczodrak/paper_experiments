#!/usr/bin/python
# Combine RSSI logs from different TX powers
# into a single JSON file
#
# Author: Marcin K Szczodrak
# Updated: 5/3/2014

import sys
import os
import json
import cc2420_conf as radio_conf
sys.path.append("../scripts")
import tests

if len(sys.argv) != 1:
	print "usage %s"
	exit()

channel = 26
lpl = 0
pwd = os.path.dirname(os.path.realpath(__file__))
tests.data_random("../cc2420", pwd, "data_random_indriya.json")


