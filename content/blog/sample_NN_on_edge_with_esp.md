+++
title = "Observing edge-ai related crashes with ESP32"
date = 2026-06-18
draft = false

[taxonomies]
categories = ["Edge-AI", "emulator"]
tags = ["blog", "TinyML", "ESP32", "QEMU", "fault-injection"]

[extra]
lang = "en"
+++

## Introduction

Good evening, its 1am and now we're gonna look at running some dummy NN code on edge (with an ESP32 which I have many of). Let's first see if ESP-IDF allows me do something like this or if someone else has already done this.

And reddit to the rescue, [this](https://www.programmingboss.com/2025/05/run-tinyml-ai-models-on-esp32-voice-recgonation-using-esp32.html#gsc.tab=0) has some insights. But its not exatly what I am looking for because firstly its an arduino project, I mean written in a slightly higher level, I can't compile that with ESP-IDF to a firmware binary to run inside the emulator (since the bootloader, partition-table etc. will be handled by arduino's framework).

Anyways, let's just try it out and we'll see if anything errors out (disclaimer, it all worked fine). Let's use the same setup as [before](https://purge12.github.io/blog/emulating-esp-firmware-on-qemu) and overwrite the hello world example code, build the code and emulate it.

### Code

Thanks to claude for the code:

```c
/*
 * Tiny on-device inference demo for the classic ESP32 (Xtensa LX6) under QEMU.
 *
 * Drop-in replacement for main/hello_world_main.c in the ESP-IDF hello_world
 * example. Keep the file name (or update SRCS in main/CMakeLists.txt) and keep
 * app_main(), and it builds with no other changes.
 *
 * What it does:
 *   1. Runs a hand-coded 2-layer MLP (4 -> 6 -> 3) on a couple of fake
 *      "sensor" windows, holding intermediate activations in a malloc'd
 *      buffer the way TFLite Micro keeps everything in one tensor arena.
 *   2. Optionally triggers one memory fault so you can watch the matching
 *      Guru Meditation panic in QEMU.
 *
 * Flip FAULT_MODE below, rebuild, re-merge, re-run.
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "esp_system.h"

static const char *TAG = "tinyml";

/* ---- fault injection selector ------------------------------------------- *
 *   FAULT_NONE           -> clean run, prints inference, then idles
 *   FAULT_NULL_DEREF     -> store through NULL      => (StoreProhibited)
 *   FAULT_ARENA_FAIL     -> malloc fails, used      => (StoreProhibited)
 *                           unchecked, mid-inference
 *   FAULT_STACK_OVERFLOW -> overrun a stack array   => corrupt return:
 *                           usually (LoadProhibited / IllegalInstruction)
 *                           or a stack-smashing abort
 * ------------------------------------------------------------------------- */
#define FAULT_NONE            0
#define FAULT_NULL_DEREF      1
#define FAULT_ARENA_FAIL      2
#define FAULT_STACK_OVERFLOW  3

#define FAULT_MODE FAULT_NONE
/* ------------------------------------------------------------------------- */

#define N_IN   4
#define N_HID  6
#define N_OUT  3

/* Illustrative weights only -- this net is NOT trained, so the predicted
 * label is arbitrary. The point is that the forward pass actually executes. */
static const float w1[N_HID][N_IN] = {
    {  1.2f, -0.3f,  0.1f,  0.0f },
    { -0.8f,  0.6f, -0.2f,  0.4f },
    {  0.3f,  0.9f, -0.5f, -0.1f },
    { -1.1f, -0.2f,  0.7f,  0.2f },
    {  0.4f,  0.1f,  0.2f, -0.9f },
    {  0.9f, -0.7f, -0.3f,  0.5f },
};
static const float b1[N_HID] = { 0.1f, -0.2f, 0.0f, 0.05f, -0.1f, 0.2f };

static const float w2[N_OUT][N_HID] = {
    { -1.0f,  0.8f,  0.2f,  1.1f, -0.3f, -0.6f },  /* class 0 */
    {  0.2f,  0.1f,  0.4f,  0.0f,  0.3f,  0.2f },  /* class 1 */
    {  1.0f, -0.7f, -0.2f, -1.0f,  0.4f,  0.7f },  /* class 2 */
};
static const float b2[N_OUT] = { 0.0f, 0.1f, 0.0f };

static const char *CLASS_NAMES[N_OUT] = { "HEAT", "IDLE", "COOL" };

/* Forward pass. arena_bytes mirrors a TFLM tensor arena: one buffer that
 * holds the hidden activations. */
static int infer(const float in[N_IN], float out[N_OUT], size_t arena_bytes)
{
    float *arena = (float *) malloc(arena_bytes);

#if FAULT_MODE == FAULT_ARENA_FAIL
    /* Deliberately skip the NULL check -- the canonical bug when the arena
     * is too big to allocate. If arena == NULL, the first store faults. */
    float *hid = arena;
    for (int j = 0; j < N_HID; j++) {
        float acc = b1[j];
        for (int i = 0; i < N_IN; i++) acc += w1[j][i] * in[i];
        hid[j] = acc > 0.0f ? acc : 0.0f;   /* <-- StoreProhibited if NULL */
    }
#else
    if (arena == NULL) {
        ESP_LOGE(TAG, "arena alloc of %u bytes failed", (unsigned) arena_bytes);
        return -1;
    }
    float *hid = arena;
    for (int j = 0; j < N_HID; j++) {
        float acc = b1[j];
        for (int i = 0; i < N_IN; i++) acc += w1[j][i] * in[i];
        hid[j] = acc > 0.0f ? acc : 0.0f;   /* ReLU */
    }
#endif

    for (int k = 0; k < N_OUT; k++) {
        float acc = b2[k];
        for (int j = 0; j < N_HID; j++) acc += w2[k][j] * hid[j];
        out[k] = acc;
    }

    free(arena);
    return 0;
}

static int argmax(const float v[N_OUT])
{
    int best = 0;
    for (int k = 1; k < N_OUT; k++) if (v[k] > v[best]) best = k;
    return best;
}

void app_main(void)
{
    ESP_LOGI(TAG, "tiny inference demo starting, free heap = %u bytes",
             (unsigned) esp_get_free_heap_size());

    /* fake sensor windows: {temp_norm, humid_norm, dT, dH} */
    static const float samples[][N_IN] = {
        {  0.9f, 0.2f,  0.10f, -0.05f },
        { -0.8f, 0.5f, -0.15f,  0.02f },
    };
    const int n_samples = sizeof(samples) / sizeof(samples[0]);

    size_t arena_bytes = N_HID * sizeof(float);   /* plenty for this model */
#if FAULT_MODE == FAULT_ARENA_FAIL
    arena_bytes = (size_t) 64 * 1024 * 1024;      /* 64 MB: malloc will fail */
#endif

    for (int s = 0; s < n_samples; s++) {
        float logits[N_OUT];
        if (infer(samples[s], logits, arena_bytes) != 0) {
            ESP_LOGE(TAG, "sample %d: inference failed", s);
            continue;
        }
        int c = argmax(logits);
        ESP_LOGI(TAG, "sample %d -> %-4s  logits: %.3f %.3f %.3f",
                 s, CLASS_NAMES[c], logits[0], logits[1], logits[2]);
    }

    ESP_LOGI(TAG, "inference done");

#if FAULT_MODE == FAULT_NULL_DEREF
    ESP_LOGW(TAG, "injecting NULL dereference...");
    volatile uintptr_t addr = 0;
    *(volatile int *) addr = 42;        /* -> Guru Meditation (StoreProhibited) */
#elif FAULT_MODE == FAULT_STACK_OVERFLOW
    ESP_LOGW(TAG, "injecting stack buffer overflow...");
    volatile float buf[4];
    volatile int n = 4096;              /* volatile defeats compile-time bounds check */
    for (int i = 0; i < n; i++) buf[i] = (float) i;   /* smash the task stack */
    ESP_LOGI(TAG, "buf[0]=%.1f", buf[0]);             /* keep the loop alive */
#endif
    /* FAULT_ARENA_FAIL already crashed inside infer() above. */

    while (1) {
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}
```

### Explaination

Here's an explanation for what's happening in this code line by line:

1. **The poisons**

```c
#define FAULT_NONE            0
#define FAULT_NULL_DEREF      1
#define FAULT_ARENA_FAIL      2
#define FAULT_STACK_OVERFLOW  3

#define FAULT_MODE FAULT_NONE
```

We're defining 3 different kinds of faults in our code and one control. The default FAULT_MODE is set to the control bit so the first run we do, should all work fine and not fault at all. Then we'll toggle this to different faults and observe the trace and see what information we get and whether emulation saved us a big deal of pain or not.

2. **Dummy weights** for a neural network simulation

```c
#define N_IN   4
#define N_HID  6
#define N_OUT  3

/* Illustrative weights only -- this net is NOT trained, so the predicted
 * label is arbitrary. The point is that the forward pass actually executes. */
static const float w1[N_HID][N_IN] = {
    {  1.2f, -0.3f,  0.1f,  0.0f },
    { -0.8f,  0.6f, -0.2f,  0.4f },
    {  0.3f,  0.9f, -0.5f, -0.1f },
    { -1.1f, -0.2f,  0.7f,  0.2f },
    {  0.4f,  0.1f,  0.2f, -0.9f },
    {  0.9f, -0.7f, -0.3f,  0.5f },
};
static const float b1[N_HID] = { 0.1f, -0.2f, 0.0f, 0.05f, -0.1f, 0.2f };

static const float w2[N_OUT][N_HID] = {
    { -1.0f,  0.8f,  0.2f,  1.1f, -0.3f, -0.6f },  /* class 0 */
    {  0.2f,  0.1f,  0.4f,  0.0f,  0.3f,  0.2f },  /* class 1 */
    {  1.0f, -0.7f, -0.2f, -1.0f,  0.4f,  0.7f },  /* class 2 */
};
static const float b2[N_OUT] = { 0.0f, 0.1f, 0.0f };

static const char *CLASS_NAMES[N_OUT] = { "HEAT", "IDLE", "COOL" };
```

This is to create a simple neural network, we have the weights and biases for an input layer and output layer. These are all arbitary numbers, but the thing is we don't care. We'll just want a simple classification NN to be there so that we can run forward passes. We don't even care about backprop right now.

3. The forward pass

```c
static int infer(const float in[N_IN], float out[N_OUT], size_t arena_bytes)
{
    float *arena = (float *) malloc(arena_bytes);

#if FAULT_MODE == FAULT_ARENA_FAIL
    /* Deliberately skip the NULL check -- the canonical bug when the arena
     * is too big to allocate. If arena == NULL, the first store faults. */
    float *hid = arena;
    for (int j = 0; j < N_HID; j++) {
        float acc = b1[j];
        for (int i = 0; i < N_IN; i++) acc += w1[j][i] * in[i];
        hid[j] = acc > 0.0f ? acc : 0.0f;   /* <-- StoreProhibited if NULL */
    }
#else
    if (arena == NULL) {
        ESP_LOGE(TAG, "arena alloc of %u bytes failed", (unsigned) arena_bytes);
        return -1;
    }
    float *hid = arena;
    for (int j = 0; j < N_HID; j++) {
        float acc = b1[j];
        for (int i = 0; i < N_IN; i++) acc += w1[j][i] * in[i];
        hid[j] = acc > 0.0f ? acc : 0.0f;   /* ReLU */
    }
#endif

    for (int k = 0; k < N_OUT; k++) {
        float acc = b2[k];
        for (int j = 0; j < N_HID; j++) acc += w2[k][j] * hid[j];
        out[k] = acc;
    }

    free(arena);
    return 0;
}

static int argmax(const float v[N_OUT])
{
    int best = 0;
    for (int k = 1; k < N_OUT; k++) if (v[k] > v[best]) best = k;
    return best;
}
```

This is a forward pass. Let's look at the individual fault modes and see how they are injected:

- FAULT_ARENA_FAIL -> The malloc not being able to malloc

The idea is that `malloc` can fail, and when it does it returns `NULL`, and this branch uses that pointer without ever checking it. A classic ESP32 has only a couple hundred of KB as the usable heap, read [this](https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/memory-types.html) documentation if you want to know more.

> The remaining 160 KB (for a total of 320 KB of DRAM) can only be allocated at runtime as heap.

And what have we done? We've written this:

```c
arena_bytes = (size_t) 64 * 1024 * 1024;
// ...
malloc(arena_bytes)
```

This is much much more than malloc can allocate so it's gonna return `NULL`. Then we do this:

```c
float *hid = arena;        // hid is now NULL
...
hid[j] = ...;              // store into the NULL pointer
```

`hid[j]` is just `*(hid + j)`, i.e. a store to address `0 + j*sizeof(float)`. On the very first iteration `(j == 0)` that's a write to address `0x00000000`. Address 0 isn't valid writable memory on the ESP32, so the CPU raises a `StoreProhibited` exception and the panic handler prints the **Guru Meditation**.

> Note where it dies: on the first store, in the middle of the hidden-layer loop, before any sample ever gets printed

That's the pain point. The allocation failed silently; the program only actually falls over later, when it touches the bad pointer.

The else part is just adding a error handler:

```c
if (arena == NULL) { ESP_LOGE(...); return -1; }
```

I'll study this under GDB later. Let's move on to the next poison:

- `FAULT_NULL_DEREF` -> Dereferencing a NULL pointer

This is a very loud bug as in, its easy to spot that something is wrong here:

```c
#if FAULT_MODE == FAULT_NULL_DEREF
    ESP_LOGW(TAG, "injecting NULL dereference...");
    volatile uintptr_t addr = 0;
    *(volatile int *) addr = 42;        /* -> Guru Meditation (StoreProhibited) */
```

We've assigned addr to 0 (NULL) and then we're trying to deference it. This is the same bug we've already inspected before. This raises the same bug as the `malloc` bug: **Guru Meditation (StoreProhibited)**

- FAULT_STACK_OVERFLOW -> Stack overflow

```c
#elif FAULT_MODE == FAULT_STACK_OVERFLOW
    ESP_LOGW(TAG, "injecting stack buffer overflow...");
    volatile float buf[4];
    volatile int n = 4096;              /* volatile defeats compile-time bounds check */
    for (int i = 0; i < n; i++) buf[i] = (float) i;   /* smash the task stack */
    ESP_LOGI(TAG, "buf[0]=%.1f", buf[0]);             /* keep the loop alive */
#endif
```

This is interesting because we know that the bug will come out very different in the logs from before (see [this](https://purge12.github.io/blog/emulating-esp-firmware-on-qemu)). I have already talked about this there and provided an explanation for why this is it.


### Emulating and observing the logs

The most subtle one is the malloc returning NULL so, let's start with that. We'll just toggle the poision to `FAULT_ARENA_FAIL` and run the steps as before:

```sh
# from the ESP-IDF root
. ./export.sh # To ensure that esp-idf is in path

# Replace the hello_world_main.c file with the code above and toggle the malloc fault
cd ./examples/get-started/hello_world
idf.py set-target esp32
idf.py build
```

Once build succeeds, we can build the qemu loadable binary:

```sh
cd build/
esptool.py --chip esp32 merge_bin --fill-flash-size 4MB -o qemu_flash.bin @flash_args
```

Then we need to run this on the qemu fork, let's do that:

```sh
# From inside your QEMU fork
./build/qemu-system-xtensa -nographic \
  -machine esp32 \
  -drive file=qemu_flash.bin,if=mtd,format=raw
```

and you'll see something like this:

```
I (1882) main_task: Started on CPU0
I (1892) main_task: Calling app_main()
I (1892) tinyml: tiny inference demo starting, free heap = 304988 bytes
Guru Meditation Error: Core  0 panic'ed (StoreProhibited). Exception was unhandled.

Core  0 register dump:
PC      : 0x400d3697  PS      : 0x00060d30  A0      : 0x800d3722  A1      : 0x3ffb4110  
A2      : 0x3f4053d0  A3      : 0x3ffb4150  A4      : 0x04000000  A5      : 0x00000764  
A6      : 0x3f402c10  A7      : 0x0004a75c  A8      : 0x00000000  A9      : 0x3f4053dc  
A10     : 0x00000000  A11     : 0x00000000  A12     : 0x3f405468  A13     : 0x0000000c  
A14     : 0x00001000  A15     : 0x00000000  SAR     : 0x00000004  EXCCAUSE: 0x0000001d  
EXCVADDR: 0x00000000  LBEG    : 0x400014fd  LEND    : 0x4000150d  LCOUNT  : 0xfffffffe  


Backtrace: 0x400d3694:0x3ffb4110 0x400d371f:0x3ffb4130 0x400db290:0x3ffb4180 0x400856f9:0x3ffb41b0
```

### Understanding and translations to real silicon

Let's understand this bug, precisely because this is something that cannot be caught by a static analyzer of a unit test!

- `EXCCAUSE: 0x0000001d` -> This is the number 29. If we look at this [post](https://esp32.com/viewtopic.php?t=5492) then this is the same memory corruption (StoreProhibited) problem. it is indeed something trying to write to non-existent memory, by e.g. dereferencing a NULL pointer.

- `EXCVADDR: 0x00000000` -> This is the address which is fucking us up, which is NULL. As expected since malloc(huge_number) gives NULL which is what we tried to store as a float here `float *hid = arena`.

- `PC: 0x400d3697` — the instruction that did it. 0x400d_xxxx is the flash-mapped code region, and that address lives inside `infer()` (the cooked function, PC means **Program Counter**). How do I know this? Well I really don't, atleast not by looking at the number itself. We'll have to cross-link this with the symbol table, which I didn't. I am stating this assumption because I know its not a RAM or a ROM problem.

This is because these addresses `0x4000_xxxx` are masked ROM and these `0x4008_xxxx` are IRAM (Instruction RAM) while `0x400D_xxxx` are the application memory. Hence I know its application memory and one function which can fuck up (I mean we deliberately set up `infer` to fuck up but still) is `infer`.

Note how much free heap we had: `free heap = 304988 bytes` that's roughly 300KB, and we tried to allocate 64MB in there so obviously it faulted. The backtrace line is four `PC:SP` pairs (SP means **stack pointer**).

So, what happens if we actually run the same wrong firmware in an actual ESP32?

> Its going to keep crashing and repeating forever!

### Why static analyzers won't work

The first party static analysis tool by espressif is `esp-clang`. let's install and run that:

```sh
idf_tools.py install esp-clang
pip install pyclang
export IDF_TOOLCHAIN=clang
idf.py clang-check
```

Once we run this (you might have to clear your build directory if it complains, just move it somewhere else for now), you'll see a lot of warnings. The few important ones are here:

```
   84 |         hid[j] = acc > 0.0f ? acc : 0.0f;   /* <-- StoreProhibited if NULL */
      |                        ^  ~
      |                           F
/home/purge/esp/esp-idf/examples/get-started/hello_world/main/hello_world_main.c:84:37: warning: floating point literal has suffix 'f', which is not uppercase [readability-uppercase-literal-suffix]
   84 |         hid[j] = acc > 0.0f ? acc : 0.0f;   /* <-- StoreProhibited if NULL */
      |                                     ^  ~
      |                                        F
/home/purge/esp/esp-idf/examples/get-started/hello_world/main/hello_world_main.c:101:40: warning: statement should be inside braces [readability-braces-around-statements]
```

Its a warning and that too not about the heap bytes itself, but about `hid[j] = NULL`! Easy to miss in the sea of warnings like these:

```
/home/purge/esp/esp-idf/examples/get-started/hello_world/main/hello_world_main.c:112:36: warning: statement should be inside braces [readability-braces-around-statements]
  112 |     for (int k = 1; k < N_OUT; k++) if (v[k] > v[best]) best = k;
      |                                    ^                             
      |                                     {
/home/purge/esp/esp-idf/examples/get-started/hello_world/main/hello_world_main.c:112:56: warning: statement should be inside braces [readability-braces-around-statements]
  112 |     for (int k = 1; k < N_OUT; k++) if (v[k] > v[best]) best = k;
      |                                                        ^         
      |                                                         {
/home/purge/esp/esp-idf/examples/get-started/hello_world/main/hello_world_main.c:116:6: warning: function 'app_main' has cognitive complexity of 95 (threshold 25) [readability-function-cognitive-complexity]
  116 | void app_main(void)
      |      ^
/home/purge/esp/esp-idf/examples/get-started/hello_world/main/hello_world_main.c:118:5: note: +1, including nesting penalty of 0, nesting level increased to 1
  118 |     ESP_LOGI(TAG, "tiny inference demo starting, free heap = %u bytes",
      |     ^
/home/purge/esp/esp-idf/components/log/include/esp_log.h:127:36: note: expanded from macro 'ESP_LOGI'
  127 | #define ESP_LOGI(tag, format, ...) do { ESP_LOG_LEVEL_LOCAL(ESP_LOG_INFO, tag, format, ##__VA_ARGS__); } while(0)
      |                                    ^
/home/purge/esp/esp-idf/examples/get-started/hello_world/main/hello_world_main.c:118:5: note: +2, including nesting penalty of 1, nesting level increased to 2
  118 |     ESP_LOGI(TAG, "tiny inference demo starting, free heap = %u bytes",
      |     ^
```

- What about `EspStackTraceDecoder.jar`? Its basically a wrapper around `xtensa-esp32-elf-addr2line`. Its a pretty printer! Its going to take the backtrace we've been seeing for all our error outputs along with the `Guru meditation` error and tell us which line fucked up in the code. Its a useful tool, but it's AFTER a problem has already happened.

- And `openocd` also will not work because its a live debugger. You'll have to RUN the actual code and attach this to the running chip and it uses GDB to set debugging points etc.

---

So anyway that concludes the on-edge crashes. You can try out the other stuff too, pretty simple to just toggle and go through the steps again, but I am calling it quits here. Gotta test out the renode emulator now.