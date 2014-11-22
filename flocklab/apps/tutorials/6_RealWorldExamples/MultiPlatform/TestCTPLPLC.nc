// $Id: TestCTPLPLC.nc 2368 2013-04-18 12:11:28Z walserc $
/**
 * @author Roman Lim <lim@tik.ee.ethz.ch>
 *
 * @section LICENSE
 *
 * Copyright (c) 2013 ETH Zurich.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 * 3. Neither the name of the copyright holders nor the names of
 *    contributors may be used to endorse or promote products derived
 *    from this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS `AS IS'
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR CONTRIBUTORS
 * BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, LOSS OF USE, DATA,
 * OR PROFITS) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
 * THE POSSIBILITY OF SUCH DAMAGE.
 *
 */

#include "Timer.h"
#include "TestCTPLPL.h"

module TestCTPLPLC @safe(){
  uses {
    // Interfaces for initialization:
    interface Boot;
    interface SplitControl as RadioControl;
    interface SplitControl as SerialControl;
    interface StdControl as RoutingControl;
    
    // Interfaces for communication, multihop and serial:
    interface Send;
    interface Receive;
    interface AMSend as SerialSend;
    interface CollectionPacket;
    interface RootControl;
    interface SystemLowPowerListening;

    interface Queue<message_t *> as UARTQueue;
    interface Pool<message_t> as UARTMessagePool;

    // Miscalleny:
    interface Timer<TMilli>;
    interface Leds;
    interface Random;
    
#ifdef BOARD_FLOCKLAB
    interface GeneralIO as FLOCKLAB_INT1;
    interface GeneralIO as FLOCKLAB_INT2;
    interface GpioInterrupt as FLOCKLAB_SIG1INT;
    interface GpioInterrupt as FLOCKLAB_SIG2INT;
#ifdef __MSP430
    interface StdControl as ClockCalibControl;
#endif
#endif
  }
}

implementation {
  task void uartSendTask();
  static void fatal_problem();
  static void report_problem();
  static void report_sent();
  static void report_received();

  uint8_t uartlen;
  message_t sendbuf;
  message_t uartbuf;
  bool sendbusy=FALSE, uartbusy=FALSE;
  
  enum {
	  SERIAL_STOPPED,
	  SERIAL_STARTING,
	  SERIAL_STARTED,
	  SERIAL_STOPPING,
  };
  uint8_t serialstate = SERIAL_STOPPED;

  /* Current local state - interval, version and accumulated readings */
  testdata_t local;

  void startTimer() {
      uint32_t interval = (call Random.rand16() % DEFAULT_INTERVAL) + DEFAULT_INTERVAL/2;
      call Timer.startOneShot(interval);
      
  }
  // 
  // On bootup, initialize radio and serial communications, and our
  // own state variables.
  //
  event void Boot.booted() {
    local.id = TOS_NODE_ID;
    local.counter = 0;

    // Beginning our initialization phases:
#if PLATFORM_TINYNODE184
    call SystemLowPowerListening.setDelayAfterReceive(36);
#else
    call SystemLowPowerListening.setDelayAfterReceive(20);
#endif
#ifdef BOARD_FLOCKLAB
#ifdef __MSP430
    call ClockCalibControl.start();
#endif
#endif
     if (call RadioControl.start() != SUCCESS)
            fatal_problem();
  }

  event void RadioControl.startDone(error_t error) {
    if (error != SUCCESS)
      fatal_problem();

    if (sizeof(local) > call Send.maxPayloadLength())
      fatal_problem();
    
    // This is how to set yourself as a root to the collection layer:
    if (local.id % 500 == 0)
        call RootControl.setRoot();
    
    if (call RoutingControl.start() != SUCCESS)
       fatal_problem();

    startTimer();
  }

  event void SerialControl.startDone(error_t error) {
    if (error != SUCCESS)
      fatal_problem();
    serialstate=SERIAL_STARTED;
    post uartSendTask();
  }

  event void RadioControl.stopDone(error_t error) { }
  event void SerialControl.stopDone(error_t error) { 
    serialstate=SERIAL_STOPPED;
  }

  //
  // Only the root will receive messages from this interface; its job
  // is to forward them to the serial uart for processing on the pc
  // connected to the sensor network.
  //
  task void reset_rx_pin() {
#ifdef BOARD_FLOCKLAB
    call FLOCKLAB_INT1.clr();
#endif
  }
  
  event message_t*
  Receive.receive(message_t* msg, void *payload, uint8_t len) {
    testdata_t* in = (testdata_t*)payload;
    testdata_t* out;
#ifdef BOARD_FLOCKLAB
    call FLOCKLAB_INT1.set();
#endif
    post reset_rx_pin();
    if (uartbusy == FALSE) {
      out = (testdata_t*)call SerialSend.getPayload(&uartbuf, sizeof(testdata_t));
      if (len != sizeof(testdata_t) || out == NULL) {
        return msg;
      }
      else {
        memcpy(out, in, sizeof(testdata_t));
      }
      uartlen = sizeof(testdata_t);
      post uartSendTask();
    } else {
      // The UART is busy; queue up messages and service them when the
      // UART becomes free.
      message_t *newmsg = call UARTMessagePool.get();
      if (newmsg == NULL) {
        // drop the message on the floor if we run out of queue space.
        report_problem();
        return msg;
      }

      //Serial port busy, so enqueue.
      out = (testdata_t*)call SerialSend.getPayload(newmsg, sizeof(testdata_t));
      if (out == NULL) {
        return msg;
      }
      memcpy(out, in, sizeof(testdata_t));

      if (call UARTQueue.enqueue(newmsg) != SUCCESS) {
        // drop the message on the floor and hang if we run out of
        // queue space without running out of queue space first (this
        // should not occur).
        call UARTMessagePool.put(newmsg);
        fatal_problem();
        return msg;
      }
    }

    return msg;
  }

  task void uartSendTask() {
    if (serialstate==SERIAL_STOPPED) {
      serialstate=SERIAL_STARTING;
      call SerialControl.start();
      return;
    }
    if (serialstate!=SERIAL_STARTED) {
      if (serialstate==SERIAL_STOPPING)
        post uartSendTask();
      return;
    }
    if (call SerialSend.send(0xffff, &uartbuf, uartlen) != SUCCESS) {
      report_problem();
    } else {
      uartbusy = TRUE;
    }
  }

  event void SerialSend.sendDone(message_t *msg, error_t error) {
    uartbusy = FALSE;
    if (call UARTQueue.empty() == FALSE) {
      // We just finished a UART send, and the uart queue is
      // non-empty.  Let's start a new one.
      message_t *queuemsg = call UARTQueue.dequeue();
      if (queuemsg == NULL) {
        fatal_problem();
        return;
      }
      memcpy(&uartbuf, queuemsg, sizeof(message_t));
      if (call UARTMessagePool.put(queuemsg) != SUCCESS) {
        fatal_problem();
        return;
      }
      post uartSendTask();
    }
    else {
      serialstate=SERIAL_STOPPING;
      call SerialControl.stop();
    }
  }

  /* At each sample period:
     - if local sample buffer is full, send accumulated samples
     - read next sample
  */
  task void clearLed() {
#ifdef BOARD_FLOCKLAB
    call FLOCKLAB_INT2.clr();
#endif
  }
  
  event void Timer.fired() {
#ifdef BOARD_FLOCKLAB
    call FLOCKLAB_INT2.set();
#endif    
    if (local.counter+1 < NUM_DATA)
      startTimer();
    if (!sendbusy) {
      testdata_t *o = (testdata_t *)call Send.getPayload(&sendbuf, sizeof(testdata_t));
      if (o == NULL) {
        fatal_problem();
        return;
      }
      memcpy(o, &local, sizeof(local));
      if (call Send.send(&sendbuf, sizeof(local)) == SUCCESS)
        sendbusy = TRUE;
      else
        report_problem();	
    }
    local.counter++;
    post clearLed();
  }

  event void Send.sendDone(message_t* msg, error_t error) {
    if (error == SUCCESS)
      report_sent();
    else
      report_problem();
    
    sendbusy = FALSE;
  }

  // Use LEDs to report various status issues.
  static void fatal_problem() { 
    call Leds.led0On(); 
    call Leds.led1On();
    call Leds.led2On();
    call Timer.stop();
  }

  static void report_problem() { call Leds.led0Toggle(); }
  static void report_sent() { call Leds.led1Toggle(); }
  static void report_received() { call Leds.led2Toggle(); }
  
#ifdef BOARD_FLOCKLAB
  async event void FLOCKLAB_SIG1INT.fired() {}
  async event void FLOCKLAB_SIG2INT.fired() {}
#endif
}
