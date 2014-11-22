#!/usr/bin/python

import sys
from numpy import *



class Indriya:
	def __init__(self, log_file):
		self.log_file = log_file
		self.radio = "radio_log.txt"
		self.skip_nodes = []
		self.base = 40000

		self.radio_logs = {}
		self.mac_logs = {}

		self.nodes = {}


	def collect_logs(self):

		f = open(self.log_file, "r")
	
		for line in f.readlines():
			l = line.split()

			if len(l) < 12:
				continue

			testbed_time = int("%s%s"%(l[0], l[1]))
			node_id = int(l[2][1:-2]) - self.base
			layer = l[4]
			state = "%s" % (l[6])
			action = "%s %s"%(l[8],l[9])
			data = [int(l[-3]), int(l[-2])]

			if node_id in self.skip_nodes:
				continue
	
			if not(node_id in self.radio_logs.keys()):
				new_node = {}
				new_node['testbed_time'] = []
				new_node['state'] = []
				new_node['action'] = []
				new_node['data'] = []

				self.radio_logs[node_id] = new_node.copy()
				self.mac_logs[node_id] = new_node.copy()
			
				
			if layer == "Radio":
				self.radio_logs[node_id]['testbed_time'].append(testbed_time)
				self.radio_logs[node_id]['state'].append(state)
				self.radio_logs[node_id]['action'].append(action)
				self.radio_logs[node_id]['data'].append(data[:])



		f.close()



	def process_radio(self):
		power_logs = {}

		for node_id in self.radio_logs.keys():
			print "Loading node %d" % node_id
			power_logs[node_id] = {}
			power_logs[node_id]['t_time'] = []
			power_logs[node_id]['m_time'] = []
			power_logs[node_id]['action'] = []
			


			for i in range(len(self.radio_logs[node_id]['action'])):
				action = self.radio_logs[node_id]['action'][i]
				power_logs[node_id]['action'].append(action)

				m_time = int(self.radio_logs[node_id]['data'][i][0]) * pow(2,16) + int(self.radio_logs[node_id]['data'][i][1])

				power_logs[node_id]['t_time'].append(self.radio_logs[node_id]['testbed_time'][i])
				power_logs[node_id]['m_time'].append(m_time)
		

		total_t_off = 0
		total_t_on = 0
		total_m_off = 0
		total_m_on = 0

		rw = open(self.radio, 'w')

		for node_id in self.radio_logs.keys():
			print "Processing node %d" % node_id

			power_logs[node_id]['t_off'] = 0
			power_logs[node_id]['t_on'] = 0
			power_logs[node_id]['m_off'] = 0
			power_logs[node_id]['m_on'] = 0

			first_action = power_logs[node_id]['action'][0]
			last_action = power_logs[node_id]['action'][0]
			for i in range(1, len(power_logs[node_id]['action'])):
				pow_log_action = power_logs[node_id]['action'][i]
				
				if pow_log_action == last_action:
					print "Error at node %d" % node_id

				if pow_log_action == 'Start VReg':
					power_logs[node_id]['t_off'] += \
						power_logs[node_id]['t_time'][i] - \
						power_logs[node_id]['t_time'][i-1]
					power_logs[node_id]['m_off'] += \
						power_logs[node_id]['m_time'][i] - \
						power_logs[node_id]['m_time'][i-1]		
				if pow_log_action == 'Stop VReg':
					power_logs[node_id]['t_on'] += \
						power_logs[node_id]['t_time'][i] - \
						power_logs[node_id]['t_time'][i-1]
					power_logs[node_id]['m_on'] += \
						power_logs[node_id]['m_time'][i] - \
						power_logs[node_id]['m_time'][i-1]		

				last_action = pow_log_action


			total_t_off += power_logs[node_id]['t_off']
			total_t_on += power_logs[node_id]['t_on']
			total_m_off += power_logs[node_id]['m_off']
			total_m_on += power_logs[node_id]['m_on']

			power_logs[node_id]['t_proc_off'] = \
				(power_logs[node_id]['t_off'] * 100.0) / \
				(power_logs[node_id]['t_off'] + power_logs[node_id]['t_on'])
			power_logs[node_id]['m_proc_off'] = \
				(power_logs[node_id]['m_off'] * 100.0) / \
				(power_logs[node_id]['m_off'] + power_logs[node_id]['m_on'])
		
			print power_logs[node_id]['t_proc_off']
			print power_logs[node_id]['m_proc_off']

			rw.write("Node %d off testbed %.3f mote %.3f\n" % (node_id, power_logs[node_id]['t_proc_off'], power_logs[node_id]['m_proc_off']))
	


		t_network_off = (total_t_off * 100.0) / ( total_t_off + total_t_on )
		m_network_off = (total_m_off * 100.0) / ( total_m_off + total_m_on )

		print "Network off %.2f %.2f " % (t_network_off, m_network_off)
		rw.write("Network off testbed %.2f motes %.2f\n" % (t_network_off, m_network_off))

		rw.close()
		


if __name__ == "__main__":
	i = Indriya(sys.argv[1])
	i.collect_logs()
	i.process_radio()
