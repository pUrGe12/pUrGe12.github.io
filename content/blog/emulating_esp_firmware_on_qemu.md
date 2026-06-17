+++
title = "Emulating ESP32 on the QEMU fork"
date = 2026-06-17
draft = false

[taxonomies]
categories = ["Hardware", "emulator"]
tags = ["blog"]

[extra]
lang = "en"
+++

The goal is to test ESP32 firmware. I know you can flash the fucking MCU with that and run it but for safety critical situations (or in any other sane person's hands) this doesn't make sense.

## Running espressif's QEMU fork

1. Install the deps:

```sh
sudo apt install -y libgcrypt20 libglib2.0-0 libpixman-1-0 libsdl2-2.0-0 libslirp0 \
                    libgcrypt20-dev libslirp-dev build-essential git meson ninja-build
git clone https://github.com/espressif/qemu.git
```

2. Get the submodules

```sh
cd qemu
git submodule update --init --recursive
```

Since I am running this for ESP32 (that is EXtensa and not a RISC-V build), we need to run: (from the fork's [readme](https://github.com/espressif/esp-toolchain-docs/blob/main/qemu/esp32/README.md) for ESP32)

```sh
sudo apt-get install libaio-dev libbluetooth-dev libcapstone-dev libbrlapi-dev libbz2-dev -y
sudo apt-get install libcap-ng-dev libcurl4-gnutls-dev libgtk-3-dev -y
sudo apt-get install libibverbs-dev libjpeg8-dev libncurses5-dev libnuma-dev -y
sudo apt-get install librbd-dev librdmacm-dev -y
sudo apt-get install libsasl2-dev libsdl2-dev libseccomp-dev libsnappy-dev libssh-dev -y
sudo apt-get install libvde-dev libvdeplug-dev libvte-2.91-dev libxen-dev liblzo2-dev -y
sudo apt-get install valgrind xfslibs-dev -y
# The above are mentioned here at: https://wiki.qemu.org/Hosts/Linux. Note that this is around 700mb of disk space in total

./configure --target-list=xtensa-softmmu \
    --enable-gcrypt \
    --enable-slirp \
    --enable-debug \
    --enable-sdl \
    --disable-strip --disable-user \
    --disable-capstone --disable-vnc \
    --disable-gtk
```

Note that you can do this for the S2 and S3 boards too, the config command might change though. After this, we'll need to build from source to get access to the xtensa CLI:

```sh
# From the QEMU root
ninja -C build
```
This is the `qemu-system-xtensa` all done and built (inside `/build/qemu-system-xtensa`). Now we'll have to build an ESP-IDF image and create a small firmware which we can push here and run inside this emulator.

### Installing ESP-IDF

I have already covered this in a previous blog about wifi stuff, but let's go over it again:

1. Get the pre-reqs

```sh
sudo apt install -y git wget flex bison gperf python3 python3-venv python3-pip \
                    cmake ninja-build ccache libffi-dev libssl-dev dfu-util
```

2. I will go with the 5.5 release and not 6.0 (which is the latest at the time of writing). I have tried many older versions (with the hope that it will allow me to send **management frames** through their wifi adapter) and honestly I can't tell the difference, but its better to go with an older version from latest.

```sh
mkdir -p ~/esp
cd ~/esp
git clone -b release/v5.5 --recursive https://github.com/espressif/esp-idf.git
```

3. Install the toolchain for esp32. I just need to write a dummy script so doesn't matter which chip I choose. This is going to create a python env and pull the `xtensa-esp32-elf`.

```sh
cd ~/esp/esp-idf
./install.sh esp32

# Once this finishes we can activate the environment
. ./export.sh
```

### Compile a sample project

Now we can compile projects with `idf.py build`. I am just going to compile and build the sample helloworld example:

```sh
cd ~/esp/esp-idf/examples/get-started/hello_world
idf.py set-target esp32
idf.py build
```

This will populate the `build/` directory with `hello_world.elf`. So the espressif QEMU fork is kinda different from `renode`, it won't just load the firmware into memory, it's going to go through the entire boot sequence. So, we need the entire build/ directory for this, not just the elf file.

`idf.py build` compiled three binaries:

- **hello_world.bin**
- **bootloader/bootloader.bin**
- **partition_table/partition-table.bin**

To get a runnable format for QEMU, we need to do what `idf.py flash` would do on a real silicon step by step. We need to then run:

```sh
cd build
esptool.py --chip esp32 merge_bin --fill-flash-size 4MB -o qemu_flash.bin @flash_args
```

`@flash_args` feeds in that offset map so you don't hand-type addresses; `merge_bin` lays each binary at its offset into a single image and zero-fills the gaps; `--fill-flash-size 4MB` pads the whole thing out to a legal flash size (the esp32 machine only accepts 2/4/8/16 MB and rejects anything else). The result is `qemu_flash.bin`. This is what CAN go to the emulator and boot and run.

Once you do this, you just need to run this via `qemu-system-xtensa`. This will be in your qemu directory. 

```sh
# Navigate to your qemu fork directory
# Only then do this
cp ~/esp/esp-idf/examples/get-started/hello_world/build/qemu_flash.bin .
```

Then run it and witness the ESP32 running without an ESP32:

```sh
./build/qemu-system-xtensa -nographic \
  -machine esp32 \
  -drive file=qemu_flash.bin,if=mtd,format=raw
```

---

What happens if the binary was cooked? As in, the firmware we wrote was not just a vanilla hello-world but something with a big flaw.

- Replace the `hello_world_main.c` file inside the examples with this one (thanks to **claude** on this one):

```c
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_system.h"

/* ---- pick your poison: change this one line, then rebuild ---- */
#define F_NULL_DEREF     1
#define F_STACK_OVERFLOW 2
#define F_INT_WDT        3
#define F_ABORT          4
#define F_ASSERT         5
#define F_ILLEGAL_JUMP   6
#define F_DIV_ZERO       7

#define FAULT  F_NULL_DEREF
/* -------------------------------------------------------------- */

#if FAULT == F_STACK_OVERFLOW
static int recurse(int n) {
    volatile char eat[512];          /* fat frame so the stack dies fast */
    eat[0] = (char)n;
    return recurse(n + 1) + eat[0];
}
#endif

void app_main(void)
{
#if   FAULT == F_NULL_DEREF
    printf("reading through NULL...\n");
    volatile int *p = NULL;
    volatile int x = *p;             /* LoadProhibited */
    printf("unreachable: %d\n", x);

#elif FAULT == F_STACK_OVERFLOW
    printf("recursing with no base case...\n");
    recurse(0);

#elif FAULT == F_INT_WDT
    printf("interrupts off, spinning forever...\n");
    portDISABLE_INTERRUPTS();
    while (1) { }                    /* Interrupt wdt timeout */

#elif FAULT == F_ABORT
    printf("calling abort()...\n");
    abort();

#elif FAULT == F_ASSERT
    printf("failing an assert...\n");
    assert(1 == 2);

#elif FAULT == F_ILLEGAL_JUMP
    printf("jumping to garbage...\n");
    void (*boom)(void) = (void (*)(void))0xdeadbeef;
    boom();                          /* InstrFetchProhibited */

#elif FAULT == F_DIV_ZERO
    volatile int a = 10, b = 0;
    printf("dividing by zero...\n");
    printf("result: %d\n", a / b);   /* IntegerDivideByZero */
#endif
}
```

Just replace the `hello_world_main.c` with this and build again:

```sh
idf.py set-target esp32
idf.py build

# Once this finishes
cd build
esptool.py --chip esp32 merge_bin --fill-flash-size 4MB -o qemu_flash_2.bin @flash_args
```

Then we again need to run the binary from the qemu fork:

```sh
cp ~/esp/esp-idf/examples/get-started/hello_world/build/qemu_flash_2.bin .

# Then do
./build/qemu-system-xtensa -nographic \
  -machine esp32 \
  -drive file=qemu_flash.bin,if=mtd,format=raw
```

Alright, brace yourself for the incoming logs:

```
Adding SPI flash device
ets Jul 29 2019 12:21:46

rst:0x1 (POWERON_RESET),boot:0x12 (SPI_FAST_FLASH_BOOT)
configsip: 0, SPIWP:0xee
clk_drv:0x00,q_drv:0x00,d_drv:0x00,cs0_drv:0x00,hd_drv:0x00,wp_drv:0x00
mode:DIO, clock div:2
load:0x3fff0030,len:6280
load:0x40078000,len:15864
load:0x40080400,len:3920
entry 0x40080644
I (721) boot: ESP-IDF v5.5.4-1077-gdfe53e2090-dirty 2nd stage bootloader
I (723) boot: compile time Jun 17 2026 20:18:38
I (723) boot: Multicore bootloader
I (765) boot: chip revision: v0.0
I (770) boot.esp32: SPI Speed      : 40MHz
I (770) boot.esp32: SPI Mode       : DIO
I (770) boot.esp32: SPI Flash Size : 2MB
I (780) boot: Enabling RNG early entropy source...
I (794) boot: Partition Table:
I (794) boot: ## Label            Usage          Type ST Offset   Length
I (795) boot:  0 nvs              WiFi data        01 02 00009000 00006000
I (795) boot:  1 phy_init         RF data          01 01 0000f000 00001000
I (796) boot:  2 factory          factory app      00 00 00010000 00100000
I (800) boot: End of partition table
I (836) esp_image: segment 0: paddr=00010020 vaddr=3f400020 size=06bb0h ( 27568) map
I (862) esp_image: segment 1: paddr=00016bd8 vaddr=3ffb0000 size=02624h (  9764) load
I (880) esp_image: segment 2: paddr=00019204 vaddr=40080000 size=06e14h ( 28180) load
I (906) esp_image: segment 3: paddr=00020020 vaddr=400d0020 size=0b7cch ( 47052) map
I (936) esp_image: segment 4: paddr=0002b7f4 vaddr=40086e14 size=05bb4h ( 23476) load
I (962) esp_image: segment 5: paddr=000313b0 vaddr=50000000 size=00020h (    32) load
I (1024) boot: Loaded app from partition at offset 0x10000
I (1024) boot: Disabling RNG early entropy source...
I (1053) cpu_start: Multicore app
I (1806) cpu_start: GPIO 3 and 1 are used as console UART I/O pins
I (1814) cpu_start: Pro cpu start user code
I (1814) cpu_start: cpu freq: 160000000 Hz
I (1815) app_init: Application information:
I (1815) app_init: Project name:     hello_world
I (1815) app_init: App version:      v5.5.4-1077-gdfe53e2090-dirty
I (1816) app_init: Compile time:     Jun 17 2026 20:18:35
I (1816) app_init: ELF file SHA256:  2f7618cc3...
I (1817) app_init: ESP-IDF:          v5.5.4-1077-gdfe53e2090-dirty
I (1817) efuse_init: Min chip rev:     v0.0
I (1817) efuse_init: Max chip rev:     v3.99 
I (1818) efuse_init: Chip rev:         v0.0
I (1820) heap_init: Initializing. RAM available for dynamic allocation:
I (1822) heap_init: At 3FFAE6E0 len 00001920 (6 KiB): DRAM
I (1823) heap_init: At 3FFB2E88 len 0002D178 (180 KiB): DRAM
I (1824) heap_init: At 3FFE0440 len 00003AE0 (14 KiB): D/IRAM
I (1824) heap_init: At 3FFE4350 len 0001BCB0 (111 KiB): D/IRAM
I (1824) heap_init: At 4008C9C8 len 00013638 (77 KiB): IRAM
I (1864) spi_flash: detected chip: gd
I (1871) spi_flash: flash io: dio
W (1876) spi_flash: Detected size(4096k) larger than the size in the binary image header(2048k). Using the size in the binary image header.
I (1893) main_task: Started on CPU0
I (1903) main_task: Calling app_main()
reading through NULL...
Guru Meditation Error: Core  0 panic'ed (LoadProhibited). Exception was unhandled.

Core  0 register dump:
PC      : 0x400d3603  PS      : 0x00060130  A0      : 0x800db153  A1      : 0x3ffb4150  
A2      : 0x00000003  A3      : 0x3f401dfc  A4      : 0x3f401e70  A5      : 0x0000076f  
A6      : 0x3f401dfc  A7      : 0x3ffb4180  A8      : 0x00000000  A9      : 0x3ffb4130  
A10     : 0x0000000a  A11     : 0x3ffb4160  A12     : 0x3ffb4140  A13     : 0x0000000c  
A14     : 0x400817d4  A15     : 0x00000002  SAR     : 0x00000004  EXCCAUSE: 0x0000001c  
EXCVADDR: 0x00000000  LBEG    : 0x400014fd  LEND    : 0x4000150d  LCOUNT  : 0xfffffffa  


Backtrace: 0x400d3600:0x3ffb4150 0x400db150:0x3ffb4180 0x400856f9:0x3ffb41b0
```

These are the logs for the `NULL_DEREF`. The `EXCCAUSE: 0x1c` is the integer `28` which is Xtensa's `LoadProhibitedCause`. This means the CPU tried to read from an address that is not allowed. And `EXCVADDR: 0x00000000` is the address it faulted on.

`Guru Meditation Error: Core  0 panic'ed (LoadProhibited). Exception was unhandled.
`. What's a **Guru Meditation Error**? Well it has a funny [origin story](https://en.wikipedia.org/wiki/Guru_Meditation), but it basically means a hard system crash.

So, because of this unhandled error, the system crashed hard.

### Lessons from the stack overflow

If we toggle the poison to `F_STACK_OVERFLOW` and observe the crash:

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

Now while this looks similar, its something very different. The basics are the same:

- `EXCCAUSE: 0x1d` -> Value 19 -> `StoreProhibited`
- `EXCVADDR: 0xbb2e7d50` -> The address of the fault. Note that `A2` also holds the same value. In this case its probably a garbage value (cause we'll see why).

The backtrace is more interesting, there is pattern to this: `0x0006001e:0xa5a5a5a5 |<-CORRUPTED`. The `0xa5a5a5a5` is FreeRTOS's [stack fill pattern](https://forums.freertos.org/t/measuring-stack-usage/4097). When a stack is created it is filled with 0xa5 - so there is already a known pattern in the stack. 
Seeing `0xa5a5a5a5` where a saved SP should be is the proof of overflow: the stack pointer ran off the end of its allocated region into the virgin fill bytes.

The interesting thing to note here is that the stack overflow happened at `Core 1` and not `Core 0` (the previous fault, NULL address reading was on `Core 0`).

### Explanation

This is getting too long, so head over to [understanding-buffer-overflows-with-FreeRTOS](https://purge12.github.io/blog/understanding-buffer-overflows-with-FreeRTOS/)