CCLS=`find -L ./ccl* -prune`
EX=`find -L ./ex* -prune`
CFRS=`find -L ./cfr* -prune`
RSSIS=`find -L ./rssi* -prune`
ONES=`find -L ./one* -prune`
DEEP=`find -L ./deep* -prune`
DEST=`find -L ./dest* -prune`
LEED=`find -L ./leed* -prune`
LPL=`find -L ./lpl* -prune`
EED=`find -L ./eeed* -prune`
CE=`find -L ./ce* -prune`
DATA=`find -L ./data* -prune`
DIRS=$(CCLS) $(CFRS) $(RSSIS) $(ONES) $(DEEP) $(LEED) $(EED) $(DEST) $(DATA) $(EX) $(LPL) $(CE)


MAKE=make

all: ccl_tests
	echo 'Nothing to make'

ccl_tests:
	for d in $(CCLS); do (cd $$d; $(MAKE) deep-clean; $(MAKE); cd ..); done

deep_tests:
	for d in $(DEEP); do (cd $$d; $(MAKE) deep-clean; $(MAKE); cd ..); done

lpl_tests:
	for d in $(LPL); do (cd $$d; $(MAKE) deep-clean; $(MAKE); cd ..); done

ones_tests:
	for d in $(ONES); do (cd $$d; $(MAKE) deep-clean; $(MAKE); cd ..); done

eed_sync:
	for d in $(EED); do (cd $$d; $(MAKE) deep-clean; $(MAKE); cd ..); done

ce:
	for d in $(CE); do (cd $$d; $(MAKE) deep-clean; $(MAKE); cd ..); done



clean: 
	
	for d in $(DIRS); do (cd $$d; $(MAKE) clean; cd ..); done

deep-clean:
	for d in $(DIRS); do (cd $$d; $(MAKE) deep-clean; cd ..); done

	
