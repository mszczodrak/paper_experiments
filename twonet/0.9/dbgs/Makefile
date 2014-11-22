# Makefile to open twonet log and send to
# Fennec to process SerialDbgs messages
#
# Author: Marcin K Szczodrak
# Updated: 4/24/2014

COMBINED_LOG="log.dat"
COMBINE_SCRIPT=../../scripts/combine_twonet_logs.py
THIS_DIR=`pwd`
SUB_DIR="result"

all:
	tar -xf *.tgz
	$(COMBINE_SCRIPT) $(THIS_DIR)/$(SUB_DIR) $(THIS_DIR)/$(COMBINED_LOG)
	$(FENNEC_FOX_LIB)/support/sdk/python/parse_dbgs_twonet.py *.dat > result.txt

clean:
	rm $(COMBINED_LOG)
	rm -rf $(SUB_DIR)
	rm result.txt

deep-clean:
	make clean
	rm *.tgz
