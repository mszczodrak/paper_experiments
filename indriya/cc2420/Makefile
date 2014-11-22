CCLS=`find -L ./ccl* -prune`
CFRS=`find -L ./cfr* -prune`
RSSIS=`find -L ./rssi* -prune`
ONES=`find -L ./one* -prune`
DEEP=`find -L ./deep* -prune`
DEST=`find -L ./dest* -prune`
LLL=`find -L ./lll* -prune`
EED=`find -L ./eed* -prune`
DATA=`find -L ./data* -prune`
DIRS=$(CCLS) $(CFRS) $(RSSIS) $(ONES) $(DEEP) $(LLL) $(EED) $(DEST) $(DATA)

MAKE=make

all: ccl_tests cfr_tests
	echo 'Nothing to make'

ccl_tests: CCLS
	for d in $(CCLS); do (cd $$d; $(MAKE) deep-clean; $(MAKE); cd ..); done

cfr_tests: CFRS
	for d in $(CFRS); do (cd $$d; $(MAKE) deep-clean; $(MAKE); cd ..); done

clean: 
	for d in $(DIRS); do (cd $$d; $(MAKE) clean; cd ..); done

deep-clean: clean
	for d in $(DIRS); do (cd $$d; $(MAKE) deep-clean; cd ..); done
