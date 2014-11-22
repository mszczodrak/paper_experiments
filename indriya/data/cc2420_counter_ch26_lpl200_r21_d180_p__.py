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
sys.path.append("../../scripts")
import radio

if len(sys.argv) != 1:
	print "usage %s"
	exit()

channel = 26
lpl = 200
pwd = os.path.dirname(os.path.realpath(__file__))
radio.counter(channel, sys.argv[0], pwd, radio_conf, lpl, 21, 180)


