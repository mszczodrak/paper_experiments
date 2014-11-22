// $Id: TestFtspC.nc 2375 2013-04-19 08:35:27Z walserc $
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

module TestFtspC
{
  uses
  {
    interface GlobalTime<T32khz>;
    interface TimeSyncInfo;
    interface AMSend;
    interface Packet as SerialPacket;
    interface Leds;
    interface Boot;
    interface SplitControl as RadioControl;
    interface SplitControl as SerialControl;
    interface Read<uint16_t> as Temperature;
    interface Read<uint16_t> as Voltage;
    interface Alarm<T32khz,uint32_t>;
#ifdef BOARD_FLOCKLAB
#ifdef __MSP430
    interface StdControl as ClockCalibControl;
#endif
#endif
  }
}

implementation
{
  message_t msg;
  bool locked = FALSE;
  uint16_t counter;
  
  uint32_t rxTimestamp;
  uint16_t temp;
  uint16_t volt;
  
  void do_report();

  event void Boot.booted() {
    call RadioControl.start();
    call Alarm.start(16384U);
#ifdef BOARD_FLOCKLAB
#ifdef __MSP430
    call ClockCalibControl.start();
#endif
#endif
  }
    
  task void timerTask() {
    if ((counter % 2) ==0) {
      call Voltage.read();
    }
    else {
      temp = 0xffff;
      volt = 0xffff;
      do_report();
    }
  }

  async event void Alarm.fired() {
    // toggle pin
    call Leds.led0Toggle();
    rxTimestamp = call GlobalTime.getLocalTime();
    post timerTask();
    // toggle pin every 1000 ms
    call Alarm.startAt(call Alarm.getAlarm(), 16384U);
  }
  
  void do_report() {
    uint32_t rx;
    
    test_ftsp_msg_t* report;
    float skew = call TimeSyncInfo.getSkew();
    
    // send serial message
    report = (test_ftsp_msg_t*)call SerialPacket.getPayload(&msg, sizeof(test_ftsp_msg_t));
    report->counter = counter++;;
    atomic {
      rx = rxTimestamp;
    }
    report->local_rx_timestamp = rx;
    report->is_synced = call GlobalTime.local2Global(&rx);
    report->global_rx_timestamp = rx;
    memcpy(&(report->skew), (void *)&skew, 4);
    report->ftsp_root_addr = call TimeSyncInfo.getRootID();
    report->ftsp_seq = call TimeSyncInfo.getSeqNum();
    report->ftsp_table_entries = call TimeSyncInfo.getNumEntries();
    report->temp = temp;
    report->voltage = volt;
    
    if (call SerialControl.start()==SUCCESS)
      locked = TRUE;
  }

  event void SerialControl.startDone(error_t err) {
    call AMSend.send(AM_BROADCAST_ADDR, &msg, sizeof(test_ftsp_msg_t));
  }

  event void Voltage.readDone(error_t res, uint16_t val) {
    volt = (res==SUCCESS?val:0xffff);
    call Temperature.read();
  }

  event void Temperature.readDone(error_t res, uint16_t val) {
    temp = (res==SUCCESS?val:0xffff);
    do_report();
  }

  event void AMSend.sendDone(message_t* ptr, error_t success) {
    call SerialControl.stop();
    return;
  }

  event void SerialControl.stopDone(error_t error){
    locked = FALSE;
  }
  
  event void RadioControl.startDone(error_t err) {}
  event void RadioControl.stopDone(error_t error){}
  
}
