// $Id: TestFtspAppC.nc 2375 2013-04-19 08:35:27Z walserc $
/*
 * Copyright (c) 2002, Vanderbilt University
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 * - Redistributions of source code must retain the above copyright
 *   notice, this list of conditions and the following disclaimer.
 * - Redistributions in binary form must reproduce the above copyright
 *   notice, this list of conditions and the following disclaimer in the
 *   documentation and/or other materials provided with the
 *   distribution.
 * - Neither the name of the copyright holders nor the names of
 *   its contributors may be used to endorse or promote products derived
 *   from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
 * FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL
 * THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
 * INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
 * (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
 * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
 * HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
 * STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
 * OF THE POSSIBILITY OF SUCH DAMAGE.
 *
 * @author: Miklos Maroti, Brano Kusy (kusy@isis.vanderbilt.edu)
 * Ported to T2: 3/17/08 by Brano Kusy (branislav.kusy@gmail.com)
 */

#include "TestFtsp.h"

configuration TestFtspAppC {
}

implementation {
  components MainC, TimeSync32kC as TimeSyncC;

  MainC.SoftwareInit -> TimeSyncC;
  TimeSyncC.Boot -> MainC;

  components TestFtspC as App;
  App.Boot -> MainC;

  // use serial
  components
    SerialActiveMessageC,                   // Serial messaging
    new SerialAMSenderC(AM_TEST_FTSP_MSG);   // Sends to the serial port

  App.SerialControl -> SerialActiveMessageC;
  App.AMSend -> SerialAMSenderC.AMSend;
  App.SerialPacket -> SerialAMSenderC;
  
  components ActiveMessageC;
  App.RadioControl -> ActiveMessageC;
  
  components LedsC;

  App.GlobalTime -> TimeSyncC;
  App.TimeSyncInfo -> TimeSyncC;
  App.Leds -> LedsC;
  
  components new Alarm32khz32C();
  MainC.SoftwareInit -> Alarm32khz32C;
  App.Alarm -> Alarm32khz32C;
   
  components new SensirionSht11C(), new Msp430InternalVoltageC();
  App.Temperature -> SensirionSht11C.Temperature;
  App.Voltage -> Msp430InternalVoltageC;
  
#ifdef BOARD_FLOCKLAB
#ifdef __MSP430
  components Msp430DcoCalibC;
  App.ClockCalibControl -> Msp430DcoCalibC;
#endif  
#endif  
}
