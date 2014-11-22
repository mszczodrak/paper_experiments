RSSI_DIRS=rssi*
COUNTER_DIRS=counter*
MAKE=make

all:
	echo 'Nothing to make'


clean: clean-counter clean-rssi


clean-counter:
	for d in $(RSSI_DIRS); do (cd $$d; $(MAKE) clean; cd ..); done


clean-rssi:
	for d in $(COUNTER_DIRS); do (cd $$d; $(MAKE) clean; cd ..); done
