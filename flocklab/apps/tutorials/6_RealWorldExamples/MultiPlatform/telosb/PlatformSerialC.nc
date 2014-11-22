// $Id: PlatformSerialC.nc 2375 2013-04-19 08:35:27Z walserc $
configuration PlatformSerialC {
  
  provides interface SplitControl;
  provides interface UartStream;
  provides interface UartByte;
  
}

implementation {
  
  components new Msp430Uart0C() as UartC;
  UartStream = UartC;  
  UartByte = UartC;
  
  components TelosSerialP;
  SplitControl = TelosSerialP;
  TelosSerialP.Msp430UartConfigure <- UartC.Msp430UartConfigure;
  TelosSerialP.Resource -> UartC.Resource;
  
}
