# $Id: Makefile 2375 2013-04-19 08:35:27Z walserc $
# Copyright (c) 2013 ETH Zurich 
# All rights reserved.
#
COMPONENT=../MultiPlatform/TestCTPLPLAppC
CFLAGS += -I../MultiPlatform
CFLAGS += -I$(TOSDIR)/lib/net/ -I$(TOSDIR)/lib/net/ctp  -I$(TOSDIR)/lib/net/4bitle
SENSORBOARD=flocklab
PFLAGS+=-board=$(SENSORBOARD) -I ../../../../tos/sensorboards/$(SENSORBOARD)

#LPL options
CFLAGS += -DLOW_POWER_LISTENING
CFLAGS += -DLPL_DEF_LOCAL_WAKEUP=1000
CFLAGS += -DLPL_DEF_REMOTE_WAKEUP=1000

BUILD_DEPS+=flocklab_embedded_image
include $(MAKERULES)

flocklab_embedded_image: exe
	@sed -i -n '1h;1!H;$${ g;s/<data>.*<\/data>/<data>#'"`base64 $(MAIN_EXE) | tr '\n' '#' | sed 's/\//\\\\\//g'`"'<\/data>/;s/#/\n/g;p}' FlockLab_Testconfiguration.xml
