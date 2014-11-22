# $Id: Makefile 2368 2013-04-18 12:11:28Z walserc $
# Copyright (c) 2013 ETH Zurich 
# All rights reserved.
#
COMPONENT=TestCTPLPLAppC
CFLAGS += -I$(TOSDIR)/lib/net/ -I$(TOSDIR)/lib/net/ctp  -I$(TOSDIR)/lib/net/4bitle
SENSORBOARD=flocklab
PFLAGS+=-board=$(SENSORBOARD) -I ../../../../tos/sensorboards/$(SENSORBOARD)

#LPL options
CFLAGS += -DLOW_POWER_LISTENING
CFLAGS += -DLPL_DEF_LOCAL_WAKEUP=1000
CFLAGS += -DLPL_DEF_REMOTE_WAKEUP=1000

#Platform specific
#TinyNode184 radio options
CFLAGS += -DSX1211_RECEIVE_ALL
#Tmote Sky
#Write serial messages on UART0 (this is used to disable USB for power measurements)
PFLAGS+=-I$(PLATFORM)
BUILD_DEPS+=flocklab_embedded_image
FLOCKLAB_PLATFORM=${shell echo $(PLATFORM) | sed 's/telosb/tmote/;s/tinynode184/tinynode/'}
FLOCKLAB_BAUDRATE=${shell echo $(PLATFORM) | sed 's/telosb/115200/;s/tinynode184/57600/;s/iris/57600/;s/opal/115200/'}
include $(MAKERULES)

flocklab_embedded_image: exe
	@sed -i -n '1h;1!H;$${ g;s/<platform>.*<\/platform>/<platform>$(FLOCKLAB_PLATFORM)<\/platform>/;s/<baudrate>.*<\/baudrate>/<baudrate>$(FLOCKLAB_BAUDRATE)<\/baudrate>/;s/<data>.*<\/data>/<data>#'"`base64 $(MAIN_EXE) | tr '\n' '#' | sed 's/\//\\\\\//g'`"'<\/data>/;s/#/\n/g;p}' FlockLab_Testconfiguration.xml
