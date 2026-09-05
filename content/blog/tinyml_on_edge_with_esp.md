+++
title = "TinyML on edge with ESP"
date = 2026-06-19
draft = false

[taxonomies]
categories = ["Edge-AI", "emulator"]
tags = ["blog", "TinyML", "ESP32", "QEMU", "quantization"]

[extra]
lang = "en"
+++

## Idea for the demo on TinyML on edge

> Done via emulating via espressif's QEMU fork and injecting faults.

We'll be using the `esp-tflite-micro` **sine model** real TFLM - TensorFlow LiteMicro, runs clean under the QEMU fork and is tiny. This also makes the correctness gate possible.

## Boot a real TFLM model in QEMU, then build 3-4 flash images that each freeze one failure

1. Have a malloc (tensor arena too small) errors with `AllocateTensors()` ignored which will lead to a panic.
2. A quantization drift which gives wrong outputs and doesn't crash! -> This is very important

We could try **stack overflows** also which is a real problem but not for this case we're running a `sine tracker` and that has 0 preprocessing so can't do a hard stack crash.

## Setup and build

For the basic setup details look at [this](https://purge12.github.io/blog/emulating-esp-firmware-on-qemu) blog post. Then come back!

We'll build the `HelloWorld` of `esp-tflite-micro`:

```sh
cd ~/esp/esp-idf
. ./export.sh
cd ..
git clone https://github.com/espressif/esp-tflite-micro.git
cd esp-tflite-micro/examples/hello_world
idf.py set-target esp32
idf.py build
```

I faced a lot of errors here. The problem with me was I was using clang (from the earlier posts where I was trying to see if the clang frontend's static checks will catch the malloc issues) but this toolchain is build for GCC!

If your trace shows something like "unrecognized options" for the compiler then you've hit the same bug and you should do something like this:

```sh
unset IDF_TOOLCHAIN

cd ~/esp/esp-idf
. ./export.sh

cd ~/esp/esp-tflite-micro/examples/hello_world
idf.py fullclean
idf.py build
```

Then it worked!

So, let's create the QEMUable binary:

```sh
cd build
esptool.py --chip esp32 merge_bin --fill-flash-size 4MB -o qemu_flash_clean.bin @flash_args
```

Run it using:

```sh
./build/qemu-system-xtensa -nographic \
  -machine esp32 \
  -drive file=qemu_flash_clean.bin,if=mtd,format=raw
```

Then we we try to run this on QEMU, BOOM HAPPENS:

```
mode:DIO, clock div:1
...
...
I (1959) heap_init: Initializing. RAM available for dynamic allocation:
I (1960) heap_init: At 3FFAE6E0 len 00001920 (6 KiB): DRAM
I (1961) heap_init: At 3FFB3A00 len 0002C600 (177 KiB): DRAM
I (1961) heap_init: At 3FFE0440 len 00003AE0 (14 KiB): D/IRAM
I (1962) heap_init: At 3FFE4350 len 0001BCB0 (111 KiB): D/IRAM
I (1962) heap_init: At 4008BDAC len 00014254 (80 KiB): IRAM
I (2007) spi_flash: detected chip: gd
I (2013) spi_flash: flash io: qio

assert failed: __esp_system_init_fn_init_flash startup_funcs.c:118 (flash_ret == ESP_OK)


Backtrace: 0x40084c2d:0x3ffe3a80 0x40084bf9:0x3ffe3aa0 0x4008a2f5:0x3ffe3ac0 0x400d1257:0x3ffe3be0 0x400d1834:0x3ffe3c00 0x400d1875:0x3ffe3c30 0x400811fa:0x3ffe3c60 0x40079922:0x3ffe3c90 |<-CORRUPTED
```

What happened is the `clock div: 1`. The earlier tests we ran on QEMU all were `clock div: 2` which means a **QIO flash mode @ 40 MHz**, while the `div: 2` is **80 MHz** thus this can be potential reason why shit broke.

```sh
cd ~/esp/esp-tflite-micro/examples/hello_world/
printf '\nCONFIG_ESPTOOLPY_FLASHMODE_DIO=y\nCONFIG_ESPTOOLPY_FLASHFREQ_40M=y\n' >> sdkconfig.defaults
rm -f sdkconfig
idf.py build
cd build
esptool.py --chip esp32 merge_bin --fill-flash-size 4MB -o qemu_flash_clean.bin @flash_args
```

Now if we run QEMU it's gonna work beautiful and we'll see something like this:

```
x_value: 0.000000, y_value: 0.000000
x_value: 0.314159, y_value: 0.372770
x_value: 0.628319, y_value: 0.559154
x_value: 0.942478, y_value: 0.838731
x_value: 1.256637, y_value: 0.965812
x_value: 1.570796, y_value: 1.042060
x_value: 1.884956, y_value: 0.957340
x_value: 2.199115, y_value: 0.821787
x_value: 2.513274, y_value: 0.533738
x_value: 2.827433, y_value: 0.237217
```

This is the happy path build (note how its tracking `y=sin(x)` approximately with `x` in radians). Now what happens if there is a problem in the tensor arena and its too small?

### Tensor arena too small

The `constexpr int kTensorArenaSize = 2000`, let's shrink that to 200 and completely ignore that failure.

```c
  if (allocate_status != kTfLiteOk) {
    MicroPrintf("AllocateTensors() failed -- IGNORING (part of the bug)");
    // return; <-- Real devs comment this out and ship it
  }
```

Now we'll build the binary again and let's name is `qemu_flash_arena.bin`. (remember to `rm -rf build` otherwise it might just not do it)

```sh
esptool.py --chip esp32 merge_bin --fill-flash-size 4MB -o qemu_flash_arena.bin @flash_args
```

and we run it:

```sh
./build/qemu-system-xtensa -nographic \
  -machine esp32 \
  -drive file=qemu_flash_arena.bin,if=mtd,format=raw
```

And as expected, we hit this error:

```
I (1946) main_task: Calling app_main()
Failed to resize buffer. Requested: 144, available 76, missing: 68
Failed starting model allocation.

AllocateTensors() failed -- IGNORING (part of the bug)
Guru Meditation Error: Core  0 panic'ed (LoadProhibited). Exception was unhandled.

Core  0 register dump:
PC      : 0x400d62a3  PS      : 0x00060f30  A0      : 0x800d609d  A1      : 0x3ffb4590  
A2      : 0x3ffb2d00  A3      : 0x00000000  A4      : 0x3ffb2c78  A5      : 0x3ffb2d70  
A6      : 0x3ffb2c88  A7      : 0x3ffb2d00  A8      : 0x00000000  A9      : 0x000000e0  
A10     : 0x0000000e  A11     : 0x00000008  A12     : 0x00000001  A13     : 0x00000004  
A14     : 0x00000000  A15     : 0x3ffb2e64  SAR     : 0x00000004  EXCCAUSE: 0x0000001c  
EXCVADDR: 0x00000000  LBEG    : 0x400d61b9  LEND    : 0x400d61bd  LCOUNT  : 0x00000000  


Backtrace: 0x400d62a0:0x3ffb4590 0x400d609a:0x3ffb45b0 0x400d5f03:0x3ffb4600 0x400e3294:0x3ffb4620
```

`EXCVADDR: 0x00000000` --> Means that it faults reading the quantized params of a tensor that were NEVER ALLOCATED.

> Note how this could not be caught by a static analyzer or unit tests! Reasons:

1. This is completely valid code -> So no static-analyzer will flag it
2. The unittest **will** fail but point at something completely different.

The reason unittests will fail is because its a static arena (not a malloc, a malloc won't fail on the host and if we change the code to a malloc, which is very plausible, then unittests will pass too!) and hence we'll be dereferencing a NULL input tensor. The host will therefore `segfault`!

> It'll be a generic SIGSEGV at best

This is bad because it tells you nothing about what went wrong! But with the emulator, we get to know exactly.

### Quantization drift -> Wrong answers

This is the part where the quantization really messes up the model and it really starts giving wrong answers. The main problem here is the scale of quantization which is something you need to decide.

These are the previous values we got for the happy path:

```
x_value: 0.000000, y_value: 0.000000
x_value: 0.314159, y_value: 0.372770
x_value: 0.628319, y_value: 0.559154
x_value: 0.942478, y_value: 0.838731
x_value: 1.256637, y_value: 0.965812
x_value: 1.570796, y_value: 1.042060
x_value: 1.884956, y_value: 0.957340
x_value: 2.199115, y_value: 0.821787
x_value: 2.513274, y_value: 0.533738
x_value: 2.827433, y_value: 0.237217
```

Error from `y = sin(x)` is 

Now if we change the quantization scale (which can drift after the model was re-exported but never updated!) in the code:

```c
// from int8_t x_quantized = x / input->params.scale + input->params.zero_point;
// to
float in_scale = input->params.scale * 1.4f // 40% wrong so any wrong value drifts it
int8_t x_quantized = x / in_scale + input->params.zero_point;
```

Then we can build and observe the logs for this one. These are a few initial values.

```
x_value: 0.000000, y_value: 0.000000
x_value: 0.314159, y_value: 0.296521
x_value: 0.628319, y_value: 0.449018
x_value: 0.942478, y_value: 0.609986
x_value: 1.256637, y_value: 0.830259
x_value: 1.570796, y_value: 0.931924
x_value: 1.884956, y_value: 0.982756
x_value: 2.199115, y_value: 1.042060
x_value: 2.513274, y_value: 0.957340
x_value: 2.827433, y_value: 0.906508
```

You can probably just eyeball this and see that it has really drifted quite a lot from the original one!


But in a lot of cases we won't have the real mathematical ground truth so we'll have to rather compare this with a trusted model (which in my case happens to be the first run I made). So, let's compare these two assuming the actual `y = sin(x)` is the first one and we can see just how badly we drift.

Let's just use this simple script to compare when the model drifted off beyond recovery (such a script will directly go in CI/CD!)

```py
import sys, re
TOL = 0.05   # clean-vs-clean is ~0 (deterministic), so anything real trips this
def load(path):
    text = open(path).read()
    xs = [float(v) for v in re.findall(r'x_value:\s*(-?[\d.]+)', text)]
    ys = [float(v) for v in re.findall(r'y_value:\s*(-?[\d.]+)', text)]
    return list(zip(xs, ys))

clean, test = load(sys.argv[1]), load(sys.argv[2])

if not clean or not test:
    sys.exit("ERROR: no x_value/y_value pairs parsed — check the log/regex")

n = min(len(clean), len(test))
worst = (0.0, 0.0)          # (max |Δy|, x where it happened)
first_break = None
bad = 0

for i in range(n):
    (cx, cy), (tx, ty) = clean[i], test[i]
    if abs(cx - tx) > 1e-3:
        print(f"WARN: x misaligned at idx {i}: clean={cx} test={tx} (logs not from same boot?)")
    d = abs(ty - cy)
    if d > worst[0]:
        worst = (d, cx)
    if d > TOL:
        bad += 1
        if first_break is None:
            first_break = (cx, cy, ty, d)

print(f"compared {n} samples, tol={TOL}")
print(f"max |Δy| = {worst[0]:.4f} at x={worst[1]:.4f}")
if first_break:
    x, cy, ty, d = first_break
    print(f"first divergence at x={x:.4f}: clean y={cy:.4f}  test y={ty:.4f}  Δ={d:.4f}")
print(f"{bad}/{n} samples beyond tolerance")
sys.exit(1 if bad else 0)  # Depending on this, we can display a CI fall or fail!
```

And when I run this on our clean and drift versions of the log:

```
compared 94 samples, tol=0.05
max |Δy| = 0.9743 at x=3.7699
first divergence at x=0.3142: clean y=0.3728  test y=0.2965  Δ=0.0762
84/94 samples beyond tolerance
exit=1
```

This is awesome because now we are catching drifts, before they actually happen, in CI! We can store one reference implementation as the ground truth and speed up the computations (since they are happening in the host, they're already faster) and quickly compare how much drift happens.

---
