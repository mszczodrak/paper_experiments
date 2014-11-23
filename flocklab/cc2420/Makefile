CCLS=`find -L ./ccl* -prune`
EX=`find -L ./ex* -prune`
CFRS=`find -L ./cfr* -prune`
RSSIS=`find -L ./rssi* -prune`
ONES=`find -L ./one* -prune`
DEEP=`find -L ./deep* -prune`
DEST=`find -L ./dest* -prune`
LLL=`find -L ./lll* -prune`
LPL=`find -L ./lpl* -prune`
EED=`find -L ./eed* -prune`
DATA=`find -L ./data* -prune`
DIRS=$(CCLS) $(CFRS) $(RSSIS) $(ONES) $(DEEP) $(LLL) $(EED) $(DEST) $(DATA) $(EX) $(LPL)


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



clean: 
	
	for d in $(DIRS); do (cd $$d; $(MAKE) clean; cd ..); done

deep-clean:
	for d in $(DIRS); do (cd $$d; $(MAKE) deep-clean; cd ..); done

	
