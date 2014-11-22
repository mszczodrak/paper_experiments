import os
import sys
import json
import yaml


def ccl(root_dir, pwd, title):
	ccl_data = []

	for i in os.listdir(root_dir):
		if not i.startswith("ccl"):
			continue
		full_path = "%s/%s" % (root_dir, i)

		summary = {}
	
		with open("%s/ROOT" % (full_path), "r") as fp:
			summary["ROOT"] = fp.read().rstrip()
		
		with open("%s/POWER" % (full_path), "r") as fp:
			summary["POWER"] = fp.read().rstrip()
		
		with open("%s/START" % (full_path), "r") as fp:
			summary["START"] = fp.read().rstrip()
			summary["START_DAY"] = summary["START"].split()[0]
			summary["START_HOUR"] = summary["START"].split()[1]
		
		with open("%s/STOP" % (full_path), "r") as fp:
			summary["STOP"] = fp.read().rstrip()
			summary["STOP_DAY"] = summary["STOP"].split()[0]
			summary["STOP_HOUR"] = summary["STOP"].split()[1]

		if summary["START"] == summary["STOP"]:
			print "Error: wrong start/stop time in %d\n" % (full_path)
			sys.exit(1)

		summary["NUMBER"] = "-1"

		for f in os.listdir(full_path):
			if f.endswith(".zip"):
				summary["NUMBER"] = f.split("-")[1].split(".")[0]
				break
		try:	
			with open("%s/summary_counter.json" % (full_path), "r") as fp:	
				content = fp.read()
				counter_data = yaml.load(content)
		except:
			print "Error: missing %s\n" % ("%s/summary_counter.json" % (full_path))
			sys.exit(1)


		try:	
			with open("%s/summary_duty_cycle.json" % (full_path), "r") as fp:	
				content = fp.read()
				duty_cycle_data = yaml.load(content)
		except:
			print "Error: missing %s\n" % ("%s/summary_counter.json" % (full_path))
			sys.exit(1)

		summary["counter_receive"] = counter_data["stats"]["receive"]

		summary["duty_cycle_avg"] = duty_cycle_data["avg"]
		summary["duty_cycle_avg_75"] = duty_cycle_data["avg_75"]
		summary["duty_cycle_max"] = duty_cycle_data["max"]
		summary["duty_cycle_max_75"] = duty_cycle_data["max_75"]
		summary["duty_cycle_median"] = duty_cycle_data["median"]
		summary["duty_cycle_median_75"] = duty_cycle_data["median_75"]
		summary["duty_cycle_min"] = duty_cycle_data["min"]
		summary["duty_cycle_min_75"] = duty_cycle_data["min_75"]
		summary["duty_cycle_std"] = duty_cycle_data["std"]
		summary["duty_cycle_std_75"] = duty_cycle_data["std_75"]

		ccl_data.append(summary)

	with open(title, 'wb') as fp:
		json.dump(ccl_data, fp, sort_keys=True, indent=4)


	
