#!/usr/bin/python
# Combines all twonet logs into a single file
# Author: Marcin K Szczodrak
# Updated 4/24/2014

import sys
import os

def combine_logs(logs_dir, combined_log):
	fin = open(combined_log, "w")

	for f in os.listdir(logs_dir):
		if f[0:4] != "node":
			print "Skipping: %s" % (f)
			continue
		mote_id = f.split("_")[1]
		file_path = "%s/%s" % (logs_dir,f)
		fout = open(file_path, "r")
		for line in fout.readlines():
			fin.write("%s %s" % (mote_id, line))

		fout.close() 

	fin.close()
			

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print "usage %d <logs_dir> <combined_log_file>\n"
		sys.exit(1)

	combine_logs(sys.argv[1], sys.argv[2])


