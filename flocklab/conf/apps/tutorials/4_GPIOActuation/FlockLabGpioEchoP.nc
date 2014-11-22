// $Id: FlockLabGpioEchoP.nc 2368 2013-04-18 12:11:28Z walserc $
/* Copyright (c) 2013 ETH Zurich.
*  All rights reserved.
*
*  Redistribution and use in source and binary forms, with or without
*  modification, are permitted provided that the following conditions
*  are met:
*
*  1. Redistributions of source code must retain the above copyright
*     notice, this list of conditions and the following disclaimer.
*  2. Redistributions in binary form must reproduce the above copyright
*     notice, this list of conditions and the following disclaimer in the
*     documentation and/or other materials provided with the distribution.
*  3. Neither the name of the copyright holders nor the names of
*     contributors may be used to endorse or promote products derived
*     from this software without specific prior written permission.
*
*  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS `AS IS'
*  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
*  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
*  ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR CONTRIBUTORS
*  BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
*  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, LOSS OF USE, DATA,
*  OR PROFITS) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
*  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
*  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
*  THE POSSIBILITY OF SUCH DAMAGE.
*
* 
* 
*
*  @author: Christoph Walser <walserc@tik.ee.ethz.ch>
*
*/

module FlockLabGpioEchoP {
	uses {
		interface Boot;
		interface GpioInterrupt as SIG1INT;
		interface GpioInterrupt as SIG2INT;
		interface GeneralIO as SIG1;
		interface GeneralIO as SIG2;
		interface GeneralIO as FLOCKLAB_INT1;
		interface GeneralIO as FLOCKLAB_INT2;
	}
}
implementation {	
	event void Boot.booted() {
		if (call SIG1.get())
			call SIG1INT.enableFallingEdge();
		else
			call SIG1INT.enableRisingEdge();
		if (call SIG2.get())
			call SIG2INT.enableFallingEdge();
		else
			call SIG2INT.enableRisingEdge();
	}

	async event void SIG1INT.fired() {
		if (call SIG1.get()) {
			call SIG1INT.enableFallingEdge();
			call FLOCKLAB_INT1.set();
		}
		else {
			call SIG1INT.enableRisingEdge();
			call FLOCKLAB_INT1.clr();
		}
	}

	async event void SIG2INT.fired() {
		if (call SIG2.get()) {
			call SIG2INT.enableFallingEdge();
			call FLOCKLAB_INT2.set();
		}
		else {
			call SIG2INT.enableRisingEdge();
			call FLOCKLAB_INT2.clr();
		}
	}
	
}
