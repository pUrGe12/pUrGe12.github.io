+++
title = "Running an emulator with Renode"
date = 2026-06-18
draft = false

[taxonomies]
categories = ["Hardware", "emulator"]
tags = ["blog"]

[extra]
lang = "en"
+++

This blog is to try out emulating a board in renode. We'll pick a sample board, go over the entire process of emulation end-to-end which includes peripherals and see how things work, exactly.

### Setup

I already explained the renode setup here at [this blog](https://purge12.github.io/blog/setting_up_renode), so you can follow that to reach the stage where I am right now.

### Runing renode

I am the following the documentation over [here](https://renode.readthedocs.io/en/latest/basic/machines.html). So, let's launch the terminal:

```sh
renode
```

Now in there we can create an empty machine:

```sh
# Typed inside the monitor
mach create "stm32f4-discovery-test"
```

You should see the `<Timestamp> [INFO] System bus created.` being logged in your terminal. This is the machine creating just the `sysbus` and it has no other peripherals, not even the CPU or memory. So, let's get that first:

```sh
machine LoadPlatformDescription @platforms/cpus/stm32f4.repl
```

This loads the CPU and peripherals for `stm32f4`. You can verify that by running `peripherals`. It should have a bunch of stuff other than `sysbus`. We can inspect the memory:

```sh
peripherals memory
sysbus.sram Size
sysbus.sram ZeroAll
```

Now we have to load the binary, this can be done via `LoadELF`:

```sh
sysbus LoadELF @firmware.elf
```

The question is, what is this firmware? Well we'll have to come up with something that can be run on an `stm32f4`.

To do this I am using [this repo](https://github.com/fcayci/stm32f4-assembly) here. This is a sample project for educational purposes. I am also installing the [GNU Arm embedded toolchain](https://developer.arm.com/downloads/-/arm-gnu-toolchain-downloads) for this. Or if you're confused like I am, just do this:

```sh
sudo apt-get install gcc-arm-none-eabi
```

Once this is installed, you can do this and get the firmware:

```sh
cd stm32f4-assembly
make
ls # Should see a template.elf there
```

Then in the renode CLI you need to do:

```sh
sysbus LoadELF @template.elf
start
```

---

Not impressed? I agree, this makes for a shitty demo. I need to find a better firmware which is more chattier so we can talk over UART or something. The easiest to verify is:

```sh
start @scripts/single-node/stm32f4_discovery.resc
```

And you can observe it do a bunch of stuff.
