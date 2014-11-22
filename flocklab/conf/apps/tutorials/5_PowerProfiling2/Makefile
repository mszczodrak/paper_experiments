# $Id: Makefile 2368 2013-04-18 12:11:28Z walserc $
# Copyright (c) 2013 ETH Zurich 
# All rights reserved.
#
COMPONENT=FlockLabPowerBlinkC
SENSORBOARD=flocklab
PFLAGS+=-board=$(SENSORBOARD) -I ../../../tos/sensorboards/$(SENSORBOARD)
BUILD_DEPS+=flocklab_embedded_image
TINYOS_ROOT_DIR?=/home/msz/github/tinyos
include $(TINYOS_ROOT_DIR)/Makefile.include

flocklab_embedded_image: exe
	@sed -i -n '1h;1!H;$${ g;s/<data>.*<\/data>/<data>#'"`base64 $(MAIN_EXE) | tr '\n' '#' | sed 's/\//\\\\\//g'`"'<\/data>/;s/#/\n/g;p}' FlockLab_Testconfiguration.xml
