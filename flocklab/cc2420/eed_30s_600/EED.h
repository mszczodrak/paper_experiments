#ifndef __EED_H_
#define __EED_H_

#define EED_PERIOD		20

nx_struct EED_header {
	nx_uint16_t crc;
	nx_uint32_t now;
	nx_uint32_t end;
	nx_uint32_t delay;
};

nx_struct EED_footer {
	nx_uint32_t left;
};

#endif
