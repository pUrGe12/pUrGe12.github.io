+++
title = "Writing STM32 firmware"
date = 2026-06-21
draft = false

[taxonomies]
categories = ["firmware", "Hardware"]
tags = ["blog"]

[extra]
lang = "en"
+++

## The details and explanations

TLDR; If you already know about how STM32 works, skip this. This is me trying to learn.

To write firmware for STM32 we need to know the memory layout and that is present in the datasheets. ST doesn't let us change that at all.

```
high addresses
┌───────────────────────────┐ 0x20020000  <- top of RAM
│  STACK  (grows downward ↓)│
│            ...            │
│  .bss / .data (variables) │
└───────────────────────────┘ 0x20000000  <- RAM starts (128 KB)
             ...
┌───────────────────────────┐
│  your code: main, uart…   │   (.text)
├───────────────────────────┤ 0x08000040  <- Reset_Handler lives here
│  VECTOR TABLE             │
│   word[1] = 0x08000041 ───┼──> "start running here"
│   word[0] = 0x20020000 ───┼──> "set stack pointer here"
└───────────────────────────┘ 0x08000000  <- FLASH starts (your program)
low addresses
```

`FLASH` (starts at **0x08000000**) is permanent storage and this is where our program will live and survive shut-downs. RAM starts at **0x20000000** and I am working with a chip having 128KB of RAM.

- At startup, the chip is going to read the very first 4-byte number sitting at **0x08000000** (the flash) and load it into the **stack pointer**.

- Then it reads the next 4-byte number (at **0x08000004**) and treats it as "the address where my program begins," and jumps there. This address points at the `Reset_Handler` and that's the first code that runs.

These two numbers are part of the `vector table` which also contains a bunch of other things (for what to do when something goes wrong). The vector table is at the start of the **flash** because the silicon reads from there.

### Compilation

The compilation happens via the `arm-none-eabi-gcc` compiler and that doesn't include any addresses in the machine code beacuse the compiler doesn't know yet where everything will go inside the chip.

Here the `linker` plays a very important role because that's the one telling the compiler where `flash` and `RAM` and that it should put the vector table first and all.

- The `linker` decides main goes at **0x080001ae**, `Reset_Handler` at **0x08000040**, and so on, then goes back and fills in all the blanks with those real addresses. This is the `firmware.elf` file, something that we can emulate or run on the chip.

### What's inside the Reset_Handler

So, to get the objdump for the blog, I compiled and linked (followed the above process) a sample code, and this is how the objdump looks like:

```
08000040 <Reset_Handler>:
8000040:	b580      	push	{r7, lr}
8000042:	b084      	sub	sp, #16
8000044:	af00      	add	r7, sp, #0
8000046:	4b10      	ldr	r3, [pc, #64]	; (8000088 <Reset_Handler+0x48>)
8000048:	60fb      	str	r3, [r7, #12]
800004a:	4b10      	ldr	r3, [pc, #64]	; (800008c <Reset_Handler+0x4c>)
800004c:	60bb      	str	r3, [r7, #8]
800004e:	e007      	b.n	8000060 <Reset_Handler+0x20>
8000050:	68fa      	ldr	r2, [r7, #12]
8000052:	1d13      	adds	r3, r2, #4
8000054:	60fb      	str	r3, [r7, #12]
8000056:	68bb      	ldr	r3, [r7, #8]
8000058:	1d19      	adds	r1, r3, #4
800005a:	60b9      	str	r1, [r7, #8]
800005c:	6812      	ldr	r2, [r2, #0]
800005e:	601a      	str	r2, [r3, #0]
8000060:	68bb      	ldr	r3, [r7, #8]
8000062:	4a0b      	ldr	r2, [pc, #44]	; (8000090 <Reset_Handler+0x50>)
8000064:	4293      	cmp	r3, r2
8000066:	d3f3      	bcc.n	8000050 <Reset_Handler+0x10>
8000068:	4b0a      	ldr	r3, [pc, #40]	; (8000094 <Reset_Handler+0x54>)
800006a:	607b      	str	r3, [r7, #4]
800006c:	e004      	b.n	8000078 <Reset_Handler+0x38>
800006e:	687b      	ldr	r3, [r7, #4]
8000070:	1d1a      	adds	r2, r3, #4
8000072:	607a      	str	r2, [r7, #4]
8000074:	2200      	movs	r2, #0
8000076:	601a      	str	r2, [r3, #0]
8000078:	687b      	ldr	r3, [r7, #4]
800007a:	4a07      	ldr	r2, [pc, #28]	; (8000098 <Reset_Handler+0x58>)
800007c:	4293      	cmp	r3, r2
800007e:	d3f6      	bcc.n	800006e <Reset_Handler+0x2e>
8000080:	f000 f895 	bl	80001ae <main>
8000084:	e7fe      	b.n	8000084 <Reset_Handler+0x44>
8000086:	bf00      	nop
8000088:	080001e8 	.word	0x080001e8
800008c:	20000000 	.word	0x20000000
8000090:	20000000 	.word	0x20000000
8000094:	20000000 	.word	0x20000000
8000098:	20000000 	.word	0x20000000
```

> This is where the analysis is supposed to go when I am free enough.


### Installing TFlite-micro

We need to install tflite-micro and cross compile it for `Cortex-M4`:

```sh
make -f tensorflow/lite/micro/tools/make/Makefile \
  TARGET=cortex_m_generic TARGET_ARCH=cortex-m4+fp \
  TARGET_TOOLCHAIN_ROOT=/usr/bin/ \
  microlite -j$(nproc)
```

- IN this case the failure is not a `Guru-meditation`!!! Its a `AllocateTensor failed`, damn. That's cool.

I didn't know renode has a `--disable-gui` option. This saves my life I thiought we'll be doing docker all along. But we'll still have to do docker though in the CI/CD 