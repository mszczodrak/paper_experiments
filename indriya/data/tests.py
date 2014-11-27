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




def data_sync(root_dir, pwd, title):
	sync_data = []

	for i in os.listdir(root_dir):
		if not i.startswith("data_sync"):
			continue
		full_path = "%s/%s" % (root_dir, i)

		summary = {}
	
		with open("%s/NUM" % (full_path), "r") as fp:
			summary["NUM"] = int(fp.read().rstrip())
		
		with open("%s/DELAY" % (full_path), "r") as fp:
			summary["DELAY"] = int(fp.read().rstrip())
	
		with open("%s/TEST_DELAY" % (full_path), "r") as fp:
			summary["TEST_DELAY"] = int(fp.read().rstrip())
	
		with open("%s/LPL" % (full_path), "r") as fp:
			summary["LPL"] = int(fp.read().rstrip())
	
		summary["NUMBER"] = "-1"

		for f in os.listdir(full_path):
			if f.endswith(".zip"):
				summary["NUMBER"] = int(f.split("-")[1].split(".")[0])
				break

		try:	
			with open("%s/summary_data_sync.json" % (full_path), "r") as fp:	
				content = fp.read()
				data = yaml.load(content)
		except:
			print "Error: missing %s\n" % ("%s/summary_data_sync.json" % (full_path))
			continue
			#sys.exit(1)

		summary["avg_delay"] = data["avg_delay"]
		summary["avg_lost"] = data["avg_lost"]
		summary["avg_lost_75"] = data["avg_lost_75"]
		summary["avg_lost_95"] = data["avg_lost_95"]
		summary["avg_lost_99"] = data["avg_lost_99"]
		summary["avg_new_var_delay"] = data["avg_new_var_delay"]
		summary["chance_of_lost"] = data["chance_of_lost"]
		summary["experiment_length"] = data["experiment_length"]
		summary["max_delay"] = data["max_delay"]
		summary["max_lost"] = data["max_lost"]
		summary["min_delay"] = data["min_delay"]
		summary["min_lost"] = data["min_lost"]
		summary["num_of_globals"] = data["num_of_globals"]
		summary["num_of_nodes"] = data["num_of_nodes"]

		sync_data.append(summary)

	with open(title, 'wb') as fp:
		json.dump(sync_data, fp, sort_keys=True, indent=4)



def sync_delay(root_dir, pwd, title):
	sync_data = []

	for i in os.listdir(root_dir):
		if not i.startswith("sync_delay"):
			continue
		full_path = "%s/%s" % (root_dir, i)

		summary = {}
	
		with open("%s/NUM" % (full_path), "r") as fp:
			summary["NUM"] = int(fp.read().rstrip())
		
		with open("%s/DELAY" % (full_path), "r") as fp:
			summary["DELAY"] = int(fp.read().rstrip())
	
		with open("%s/REPEAT" % (full_path), "r") as fp:
			summary["REPEAT"] = int(fp.read().rstrip())
	
		with open("%s/TEST_DELAY" % (full_path), "r") as fp:
			summary["TEST_DELAY"] = int(fp.read().rstrip())
	
		with open("%s/LPL" % (full_path), "r") as fp:
			summary["LPL"] = int(fp.read().rstrip())
	
		summary["NUMBER"] = "-1"

		for f in os.listdir(full_path):
			if f.endswith(".zip"):
				summary["NUMBER"] = int(f.split("-")[1].split(".")[0])
				break

		try:	
			with open("%s/summary_data_sync.json" % (full_path), "r") as fp:	
				content = fp.read()
				data = yaml.load(content)
		except:
			print "Error: missing %s\n" % ("%s/summary_data_sync.json" % (full_path))
			continue
			#sys.exit(1)

		summary["avg_delay"] = data["avg_delay"]
		summary["avg_lost"] = data["avg_lost"]
		summary["avg_new_var_delay"] = data["avg_new_var_delay"]
		summary["chance_of_lost"] = data["chance_of_lost"]
		summary["experiment_length"] = data["experiment_length"]
		summary["max_delay"] = data["max_delay"]
		summary["max_lost"] = data["max_lost"]
		summary["min_delay"] = data["min_delay"]
		summary["min_lost"] = data["min_lost"]
		summary["num_of_globals"] = data["num_of_globals"]
		summary["num_of_nodes"] = data["num_of_nodes"]

		sync_data.append(summary)

	with open(title, 'wb') as fp:
		json.dump(sync_data, fp, sort_keys=True, indent=4)



