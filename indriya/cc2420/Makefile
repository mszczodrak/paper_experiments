CCLS=`find -L ./ccl* -prune`
CFRS=`find -L ./cfr* -prune`
RSSIS=`find -L ./rssi* -prune`
ONES=`find -L ./one* -prune`
DEEP=`find -L ./deep* -prune`
DEST=`find -L ./dest* -prune`
LLL=`find -L ./lll* -prune`
EED=`find -L ./eed* -prune`
RANDOM=`find -L ./random_r* -prune`
MERGE=`find -L ./merge_* -prune`
DATA=`find -L ./data_* -prune`
SYNC=`find -L ./sync* -prune`
CE=`find -L ./ce* -prune`
V=`find -L ./v* -prune`
DIRS=$(CCLS) $(CFRS) $(RSSIS) $(ONES) $(DEEP) $(LLL) $(EED) $(DEST) $(DATA) $(SYNC) $(CE) $(V) 

MAKE=make

all: ccl_tests
	echo 'Nothing to make'

ccl_tests:
	for d in $(CCLS); do (cd $$d; $(MAKE) deep-clean; $(MAKE); cd ..); done

cfr_tests:
	for d in $(CFRS); do (cd $$d; $(MAKE) deep-clean; $(MAKE); cd ..); done

deep_tests:
	for d in $(DEEP); do (cd $$d; $(MAKE) deep-clean; $(MAKE); cd ..); done

lll_tests:
	for d in $(LLL); do (cd $$d; $(MAKE) deep-clean; $(MAKE); cd ..); done

ones_tests:
	for d in $(ONES); do (cd $$d; $(MAKE) deep-clean; $(MAKE); cd ..); done

data_random:
	for d in $(DATA); do (cd $$d; $(MAKE) deep-clean; $(MAKE); cd ..); done

sync_delay:
	for d in $(SYNC); do (cd $$d; $(MAKE) deep-clean; $(MAKE); cd ..); done

eed_sync:
	for d in $(EED); do (cd $$d; $(MAKE) deep-clean; $(MAKE); cd ..); done

random:
	for d in $(RANDOM); do (cd $$d; $(MAKE) deep-clean; $(MAKE); cd ..); done

merge:
	for d in $(MERGE); do (cd $$d; $(MAKE) deep-clean; $(MAKE); cd ..); done

clean: 
	for d in $(DIRS); do (cd $$d; $(MAKE) clean; cd ..); done

deep-clean: clean
	for d in $(DIRS); do (cd $$d; $(MAKE) deep-clean; cd ..); done
