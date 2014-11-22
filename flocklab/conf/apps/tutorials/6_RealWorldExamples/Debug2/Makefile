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
CFLAGS += -DLPL_DEF_LOCAL_WAKEUP=512
CFLAGS += -DLPL_DEF_REMOTE_WAKEUP=512
CFLAGS += -DDELAY_AFTER_RECEIVE=20

CFLAGS += -I.

CFLAGS += -I$(TINYOS_OS_DIR)/lib/net \
          -I$(TINYOS_OS_DIR)/lib/net/drip \
          -I$(TINYOS_OS_DIR)/lib/net/4bitle \
          -I$(TINYOS_OS_DIR)/lib/net/ctp -DNO_DEBUG

TFLAGS += -I$(TINYOS_OS_DIR)/../apps/tests/TestDissemination \
          -I$(TINYOS_OS_DIR)/../support/sdk/c \
          -I$(TINYOS_OS_DIR)/types \
          -I.

BUILD_DEPS+=flocklab_embedded_image

TINYOS_ROOT_DIR?=/home/msz/github/tinyos
include $(TINYOS_ROOT_DIR)/Makefile.include

flocklab_embedded_image: exe
	@sed -i -n '1h;1!H;$${ g;s/<data>.*<\/data>/<data>#'"`base64 $(MAIN_EXE) | tr '\n' '#' | sed 's/\//\\\\\//g'`"'<\/data>/;s/#/\n/g;p}' FlockLab_Testconfiguration.xml

