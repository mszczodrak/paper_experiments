// $Id: TestCTPLPLAppC.nc 2368 2013-04-18 12:11:28Z walserc $
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

configuration TestCTPLPLAppC { }
implementation {
  components MainC, TestCTPLPLC, NoLedsC as LedsC, new TimerMilliC();

  TestCTPLPLC.Boot -> MainC;
  TestCTPLPLC.Timer -> TimerMilliC;
  TestCTPLPLC.Leds -> LedsC;

  // Communication components.  These are documented in TEP 113:
  // Serial Communication, and TEP 119: Collection.
  //
  components CollectionC as Collector,  // Collection layer
    ActiveMessageC,                         // AM layer
    new CollectionSenderC(AM_TESTDATA), // Sends multihop RF
    SerialActiveMessageC,                   // Serial messaging
    new SerialAMSenderC(AM_TESTDATA);   // Sends to the serial port

  TestCTPLPLC.RadioControl -> ActiveMessageC;
  TestCTPLPLC.SerialControl -> SerialActiveMessageC;
  TestCTPLPLC.RoutingControl -> Collector;

  TestCTPLPLC.Send -> CollectionSenderC;
  TestCTPLPLC.SerialSend -> SerialAMSenderC.AMSend;
  TestCTPLPLC.Receive -> Collector.Receive[AM_TESTDATA];
  TestCTPLPLC.RootControl -> Collector;

  components new PoolC(message_t, 10) as UARTMessagePoolP,
    new QueueC(message_t*, 10) as UARTQueueP;

  TestCTPLPLC.UARTMessagePool -> UARTMessagePoolP;
  TestCTPLPLC.UARTQueue -> UARTQueueP;
  
  components RandomC;
  TestCTPLPLC.Random -> RandomC;
  
  components SystemLowPowerListeningC;
  TestCTPLPLC.SystemLowPowerListening -> SystemLowPowerListeningC;
  
#ifdef CTPDEBUG
  components new PoolC(message_t, 20) as DebugMessagePool,
    new QueueC(message_t*, 20) as DebugSendQueue,
    new SerialAMSenderC(AM_CTP_DEBUG) as DebugSerialSender,
    UARTDebugSenderP as DebugSender;

  DebugSender.Boot -> MainC;
  DebugSender.UARTSend -> DebugSerialSender;
  DebugSender.MessagePool -> DebugMessagePool;
  DebugSender.SendQueue -> DebugSendQueue;
  Collector.CollectionDebug -> DebugSender;
#endif  

#ifdef BOARD_FLOCKLAB
  components FlockLabGpioC;
  TestCTPLPLC.FLOCKLAB_INT1 -> FlockLabGpioC.FLOCKLAB_INT1;
  TestCTPLPLC.FLOCKLAB_INT2 -> FlockLabGpioC.FLOCKLAB_INT2;
  TestCTPLPLC.FLOCKLAB_SIG1INT -> FlockLabGpioC.SIG1INT;
  TestCTPLPLC.FLOCKLAB_SIG2INT -> FlockLabGpioC.SIG2INT;
#ifdef __MSP430
  components Msp430DcoCalibC;
  TestCTPLPLC.ClockCalibControl -> Msp430DcoCalibC;
#endif  
#endif
}
