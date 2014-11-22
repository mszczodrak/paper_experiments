#!/usr/bin/env python

# $Id: evalClockDrift.py 2384 2013-04-25 11:24:13Z walserc $

import tarfile, sys
from struct import *

def usage():
	print "Usage: evalClockDrift <flocklab_results_archive.tar.gz>\n"

##############################################################################
#
# Main
#
##############################################################################
def main(argv):

	if len(argv)<>1:
		usage()
		exit()

	tar = tarfile.open(argv[0])
	nodelist = []
	ftsproot = -1
	for member in tar.getmembers():
			if member.name[-15:] == "gpiotracing.csv":
				f = tar.extractfile(member)
				gpio = []
				content = f.read()
				lines = content.split("\n")
				for line in lines:
					if len(line)==0 or line[0]=='#':
						continue
					val = line.split(',')
					del val[3]
					val = map(float, val)
					gpio.append(val)
				# gpio = sorted(gpio, key = lambda time: time[0])
				
			# process serial packets
			if member.name[-16:] == "serialreader.csv":
				f = tar.extractfile(member)
				serial = []
				line = f.readline()
				while line != '':
					if line[0]=='#':
						line = f.readline()
						continue
					val = line[0:-1].split(',')
					#typedef nx_struct test_ftsp_msg
					#{
						#nx_uint16_t counter;
						#nx_uint32_t local_rx_timestamp;
						#nx_uint32_t global_rx_timestamp;
						#float nx_int32_t  skew;
						#nx_uint8_t  is_synced;
						#nx_uint16_t ftsp_root_addr;
						#nx_uint8_t  ftsp_seq;
						#nx_uint8_t  ftsp_table_entries;
						#nx_uint16_t temp;
					#} test_ftsp_msg_t;
					pck = val[3]
					val.pop()
					val = map(float, val)
					pckval = list(unpack('!8xHIIfBHBBHH', pck.decode('hex')))
					# pckval[3] > swap endianess
					tmp = pack('!f', pckval[3])
					tmp = unpack('<f', tmp)
					pckval[3] = tmp[0]
					val.extend(pckval)
					serial.append(val)
					if not val[1] in nodelist:
						nodelist.append(val[1])
						if val[2] == 0:
							ftsproot = val[1]
					line = f.readline()
				# serial = sorted(serial, key = lambda time: time[0])
			
	tar.close()

	nodelist = sorted(map(int, nodelist), key=lambda root:ftsproot<>root)

	# process data, use minute average
	t0=gpio[0][0]
	win=60
	steps=int((gpio[-1][0]-gpio[0][0]) / win)
	# temperatures
	print "#temperatures %s" %  (",".join(map(str,nodelist)))
	for i in range(0,steps):
		tserial=filter(lambda x:x[0]>=t0+i*win and x[0]<t0+(i+1)*win, serial)
			
		t=[]
		for n in nodelist:
			temp = map(lambda temp:temp[11], filter(lambda x:x[1]==n and x[11]<>0xffff,tserial))
			if len(temp)>0:
				t.append("%0.2f" % (0.01 * float(sum(temp))/len(temp) - 39.6))
			else:
				t.append("999")
		print ",".join(t)

	# drift ftsp
	print "#drift ftsp %s" %  (",".join(map(str,nodelist)))
	rootdrift=0
	for i in range(0,steps):
		tserial=filter(lambda x:x[0]>=t0+i*win and x[0]<t0+(i+1)*win, serial)
			
		t=[]
		for n in nodelist:
			drift = map(lambda drift:drift[6], filter(lambda x:x[1]==n,tserial))
			if len(drift)>0:
				if n==ftsproot:
					rootdrift = float(sum(drift))/len(drift)
					t.append("0")
				else:				
					t.append("%0.2f" % ((-float(sum(drift))/len(drift) + rootdrift) / (rootdrift+1) * 1e6))
			else:
				t.append("999")
		print ",".join(t)

	#drift gptio tracing
	#combine serial and gpio data
	combined=[] # ts_gpio, id, ts_serial, ts_node
	for n in nodelist:
		g=filter(lambda x:x[1]==n,gpio)
		s=filter(lambda x:x[1]==n,serial)
		num=min(len(g),len(s))
		map(lambda x,y:combined.append([x[0],x[1],y[0],y[4]]),g[:num-1],s[:num-1])

	print "#drift gpio tracing %s" %  (",".join(map(str,nodelist)))
	rootdrift=0
	for i in range(0,steps):
		tcomb=filter(lambda x:x[0]>=t0+i*win and x[0]<t0+(i+1)*win, combined)
			
		t=[]
		for n in nodelist:
			# ticks per sec
			ts = map(lambda ts:ts[3], filter(lambda x:x[1]==n,tcomb))
			t_node = map(lambda x,y:x-y,ts[1:],ts[:-1])
			ts = map(lambda ts:ts[0], filter(lambda x:x[1]==n,tcomb))
			t_obs = map(lambda x,y:x-y,ts[1:],ts[:-1])
			speed = map(lambda n,o:float(n)/o, t_node, t_obs)
			
			if len(speed)>0:
				if n==ftsproot:
					rootspeed = float(sum(speed))/len(speed)
					t.append("0")
				else:				
					t.append("%0.2f" % ((float(sum(speed))/len(speed) - rootspeed) / (rootspeed) * 1e6))
			else:
				t.append("999")
		print ",".join(t)

if __name__ == "__main__":
	main(sys.argv[1:])
