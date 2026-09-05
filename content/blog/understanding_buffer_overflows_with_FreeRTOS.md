+++
title = "understanding-buffer-overflows-with-FreeRTOS"
date = 2026-06-17
draft = false

[taxonomies]
categories = ["Hardware", "emulator"]
tags = ["blog"]

[extra]
lang = "en"
+++

Last time we wrote some buggy code and had the emulator crash out. This was the buggy code for reference:

```c
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_system.h"

static int recurse(int n) {
    volatile char eat[512];          /* fat frame so the stack dies fast */
    eat[0] = (char)n;
    return recurse(n + 1) + eat[0];
}

void app_main(void)
{
    printf("recursing with no base case...\n");
    recurse(0);

}
```

And when we emulate this on QEMU (details [here](https://purge12.github.io/blog/emulating-esp-firmware-on-qemu/)), we got this trace:

```
recursing with no base case...
Guru Meditation Error: Core  1 panic'ed (StoreProhibited). Exception was unhandled.

Core  1 register dump:
PC      : 0x40085cda  PS      : 0x00050033  A0      : 0x40085b87  A1      : 0x3ffb47e0  
A2      : 0xbb2e7d50  A3      : 0x00000000  A4      : 0x00010d32  A5      : 0x3ffb1480  
A6      : 0x00000001  A7      : 0x00000000  A8      : 0x400829ae  A9      : 0x3ffaf550  
A10     : 0x00000001  A11     : 0x00000000  A12     : 0x80085e95  A13     : 0x3ffb1470  
A14     : 0x3ffb2b94  A15     : 0x00000001  SAR     : 0x00000000  EXCCAUSE: 0x0000001d  
EXCVADDR: 0xbb2e7d50  LBEG    : 0x00000000  LEND    : 0x00000000  LCOUNT  : 0x00000000  


Backtrace: 0x40085cd7:0x3ffb47e0 0x40085b84:0x3ffb47f0 0x0006001e:0xa5a5a5a5 |<-CORRUPTED
```

FINSIH THIS

References:

- [x] https://www.freertos.org/Documentation/02-Kernel/02-Kernel-features/09-Memory-management/02-Stack-usage-and-stack-overflow-checking

- [x] https://en.wikipedia.org/wiki/Guru_Meditation
